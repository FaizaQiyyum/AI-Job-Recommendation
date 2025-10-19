from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, JobPosting, Profile


# ✅ Registration Form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Enter your username", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email", "class": "form-control"}),
        }


# ✅ Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))


# ✅ Job Posting Form (Admin or User can post jobs)
class JobForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            "title",
            "description",
            "company",
            "location",
            "salary",
            "job_type",
            "experience_level",
            "employment_type",
            "remote_option",
            "skills_required",
            "deadline",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Job title", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Job description", "class": "form-control"}),
            "company": forms.TextInput(attrs={"placeholder": "Company name", "class": "form-control"}),
            "location": forms.TextInput(attrs={"placeholder": "Job location", "class": "form-control"}),
            "salary": forms.TextInput(attrs={"placeholder": "e.g. $50,000 - $70,000", "class": "form-control"}),
            "skills_required": forms.Textarea(attrs={"rows": 3, "placeholder": "List required skills", "class": "form-control"}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "experience_level": forms.Select(attrs={"class": "form-select"}),
            "employment_type": forms.Select(attrs={"class": "form-select"}),
        }


# ✅ User Profile Update Form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


# ✅ Detailed Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "location",
            "address",
            "education",
            "certificates",
            "projects",
            "extracurriculars",
            "hackathons",
            "skills",
            "experience",
            "resume",
            "profile_picture",
        ]
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "Enter your phone number", "class": "form-control"}),
            "location": forms.TextInput(attrs={"placeholder": "Your city or country", "class": "form-control"}),
            "address": forms.Textarea(attrs={"rows": 2, "placeholder": "Your full address", "class": "form-control"}),
            "education": forms.Textarea(attrs={"rows": 2, "placeholder": "Add your education details", "class": "form-control"}),
            "certificates": forms.Textarea(attrs={"rows": 2, "placeholder": "Add your certificates", "class": "form-control"}),
            "projects": forms.Textarea(attrs={"rows": 2, "placeholder": "Add your projects", "class": "form-control"}),
            "extracurriculars": forms.Textarea(attrs={"rows": 2, "placeholder": "Add extracurricular activities", "class": "form-control"}),
            "hackathons": forms.Textarea(attrs={"rows": 2, "placeholder": "Add hackathon details", "class": "form-control"}),
            "skills": forms.Textarea(attrs={"rows": 2, "placeholder": "List your skills", "class": "form-control"}),
            "experience": forms.TextInput(attrs={"placeholder": "e.g. 2 years in Python", "class": "form-control"}),
        }
