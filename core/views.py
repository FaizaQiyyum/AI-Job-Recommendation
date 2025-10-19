from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from .forms import RegisterForm, JobForm, UserUpdateForm, ProfileForm
from .models import User, JobPosting, Application, Profile, Bookmark
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetCode
from django.utils import timezone

# --------------------------------------------------
# Helper: Check if user is admin
# --------------------------------------------------
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# --------------------------------------------------
# Home Page
# --------------------------------------------------
def home(request):
    jobs = JobPosting.objects.all().order_by('-created_at')[:5]

    applied_ids = []
    if request.user.is_authenticated and not request.user.is_staff:
        applied_ids = Application.objects.filter(user=request.user).values_list("job_id", flat=True)

    return render(request, "core/home.html", {"jobs": jobs, "applied_ids": applied_ids})

# --------------------------------------------------
# Register
# --------------------------------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})

# --------------------------------------------------
# Login View
# --------------------------------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_superuser or user.is_staff:
                return redirect("admin_dashboard")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

# --------------------------------------------------
# Logout
# --------------------------------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")

# --------------------------------------------------
# Admin Login Redirect
# --------------------------------------------------
def admin_login(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect("admin_dashboard")
    return redirect("login")

# --------------------------------------------------
# Admin Dashboard
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_jobs = JobPosting.objects.count()
    total_applications = Application.objects.count()

    app_status_counts = Application.objects.values("status").annotate(count=Count("id"))
    applications = Application.objects.select_related("user", "job").order_by("-applied_at")

    context = {
        "total_users": total_users,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "app_status_counts": app_status_counts,
        "applications": applications,
    }
    return render(request, "core/admin_dashboard.html", context)

# --------------------------------------------------
# Admin – Manage Jobs
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_jobs(request):
    jobs = JobPosting.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "core/admin_jobs.html", {"jobs": jobs})

# --------------------------------------------------
# Admin – Add Job
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, "Job added successfully!")
            return redirect("admin_jobs")
    else:
        form = JobForm()
    return render(request, "core/add_job.html", {"form": form})

# --------------------------------------------------
# Admin – Edit Job
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def edit_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, created_by=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("admin_jobs")
    else:
        form = JobForm(instance=job)
    return render(request, "core/edit_job.html", {"form": form})

# --------------------------------------------------
# Admin – Delete Job
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def delete_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, created_by=request.user)
    job.delete()
    messages.warning(request, f"Job '{job.title}' deleted.")
    return redirect("admin_jobs")

# --------------------------------------------------
# Admin – Manage Users
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, "core/admin_users.html", {"users": users})

# --------------------------------------------------
# Job List (for all users) with search
# --------------------------------------------------
def job_list(request):
    query = request.GET.get("q", "")
    location = request.GET.get("location", "")
    company = request.GET.get("company", "")

    jobs = JobPosting.objects.all()

    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if company:
        jobs = jobs.filter(company__icontains=company)

    jobs = jobs.order_by("-created_at")

    applied_ids = []
    if request.user.is_authenticated and not request.user.is_staff:
        applied_ids = Application.objects.filter(user=request.user).values_list("job_id", flat=True)

    return render(request, "core/job_list.html", {
        "jobs": jobs,
        "query": query,
        "location": location,
        "company": company,
        "applied_ids": applied_ids,
    })

# --------------------------------------------------
# Apply for Job
# --------------------------------------------------
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    if Application.objects.filter(job=job, user=request.user).exists():
        messages.info(request, "You have already applied for this job.")
    else:
        Application.objects.create(job=job, user=request.user)
        messages.success(request, "Your application has been submitted.")
    return redirect("job_list")

# --------------------------------------------------
# Admin – Update Application Status
# --------------------------------------------------
@login_required
@user_passes_test(is_admin)
def update_application_status(request, app_id, status):
    app = get_object_or_404(Application, id=app_id)
    if status in ["accepted", "declined", "pending"]:
        app.status = status
        app.save()
        messages.success(request, f"Application marked as {status.capitalize()}.")
    return redirect("admin_dashboard")

# --------------------------------------------------
# AI-Powered Job Recommendations
# --------------------------------------------------
@login_required
def recommendations(request):
    user = request.user
    profile = getattr(user, "profile", None)
    if not profile or not profile.skills:
        return render(request, "core/recommendations.html", {
            "recommendations": [],
            "applied_ids": [],
            "bookmarked_ids": [],
        })

    skills = [s.strip().lower() for s in profile.skills.split(",") if s.strip()]
    if not skills:
        return render(request, "core/recommendations.html", {
            "recommendations": [],
            "applied_ids": [],
            "bookmarked_ids": [],
        })

    recommendations = []
    all_jobs = JobPosting.objects.all()

    for job in all_jobs:
        job_desc = job.description.lower() if job.description else ""
        matched_skills = [skill for skill in skills if skill in job_desc]
        if matched_skills:
            score = min(100, 50 + 10 * len(matched_skills))
            explanation = "Matched skills: " + ", ".join([s.capitalize() for s in matched_skills])
            recommendations.append({
                "job": job,
                "score": score,
                "explanation": explanation,
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    applied_ids = Application.objects.filter(user=user).values_list("job_id", flat=True)
    bookmarked_ids = Bookmark.objects.filter(user=user).values_list("job_id", flat=True)

    return render(request, "core/recommendations.html", {
        "recommendations": recommendations,
        "applied_ids": applied_ids,
        "bookmarked_ids": bookmarked_ids,
    })

# --------------------------------------------------
# User Profile
# --------------------------------------------------
@login_required
def profile(request):
    profile = getattr(request.user, "profile", None)
    skills = profile.skills.split(",") if profile and profile.skills else []
    return render(request, "core/profile.html", {"profile": profile, "skills": skills})

# --------------------------------------------------
# Edit Profile
# --------------------------------------------------
@login_required
def edit_profile(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "core/profile_edit.html", {"user_form": user_form, "profile_form": profile_form})

# --------------------------------------------------
# My Applications
# --------------------------------------------------
@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related("job")
    return render(request, "core/my_applications.html", {"applications": applications})

# --------------------------------------------------
# My Bookmarks
# --------------------------------------------------
@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("job")
    applied_ids = Application.objects.filter(user=request.user).values_list("job_id", flat=True)
    return render(request, "core/my_bookmarks.html", {"bookmarks": bookmarks, "applied_ids": applied_ids})

# --------------------------------------------------
# Bookmark / Unbookmark Job
# --------------------------------------------------
@login_required
def bookmark_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, job=job)
    if not created:
        bookmark.delete()
        messages.info(request, f"Removed bookmark for '{job.title}'.")
    else:
        messages.success(request, f"Bookmarked '{job.title}' successfully!")
    return redirect('job_list')

from django.contrib.auth.decorators import login_required

def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    applied_ids = []
    if request.user.is_authenticated:
        applied_ids = Application.objects.filter(user=request.user).values_list('job_id', flat=True)
    return render(request, "core/job_detail.html", {"job": job, "applied_ids": applied_ids})

# --------------------------------------------------
# Forgot Password - send 5-digit code
# --------------------------------------------------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            code = f"{random.randint(10000, 99999)}"
            PasswordResetCode.objects.create(user=user, code=code)

            # Send email
            send_mail(
                "Your Password Reset Code",
                f"Your 5-digit password reset code is: {code}\nIt will expire in 10 minutes.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            request.session['reset_user_id'] = user.id
            messages.success(request, "A 5-digit code has been sent to your email.")
            return redirect("verify_code")
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
    return render(request, "core/registration/forgot_password.html")


# --------------------------------------------------
# Verify Code
# --------------------------------------------------
def verify_code(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Please enter your email first.")
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        code_input = request.POST.get("code")
        try:
            prc = PasswordResetCode.objects.filter(user=user).latest('created_at')
            if prc.is_expired():
                prc.delete()
                messages.error(request, "Code expired. Please request a new one.")
                return redirect("forgot_password")

            if code_input == prc.code:
                prc.delete()
                request.session['verified_user_id'] = user.id
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid code.")
        except PasswordResetCode.DoesNotExist:
            messages.error(request, "No code found. Please request a new one.")
            return redirect("forgot_password")

    return render(request, "core/registration/verify_code.html")


# --------------------------------------------------
# Reset Password
# --------------------------------------------------
def reset_password(request):
    user_id = request.session.get('verified_user_id')
    if not user_id:
        messages.error(request, "You must verify your code first.")
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            user.set_password(password1)
            user.save()
            messages.success(request, "Password reset successful! You can now log in.")
            request.session.pop('verified_user_id', None)
            request.session.pop('reset_user_id', None)
            return redirect("login")

    return render(request, "core/registration/reset_password.html")

