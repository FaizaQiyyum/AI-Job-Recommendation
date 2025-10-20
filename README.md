🧠 AccessJobs (AI-Powered Job Board)

A modern Job Portal System built with Django, Bootstrap, and an integrated AI Recommendation Engine.
Unlike basic login–logout job boards, AccessJobs uses Artificial Intelligence (AI) to recommend the most relevant jobs to users based on their skills and profile information.

🚀 Features

🧩 User Authentication: Register, login, logout, and profile management.
👩‍💼 Admin Dashboard: Add, edit, delete, and manage job postings.
💼 Job Management: Apply, bookmark, and view job details.
🔐 Secure Login System: Password reset via email & 5-digit verification code.

🌟 AI Recommendation System:

Suggests jobs by analyzing user skills from their profile.
Matches keywords between user skills and job descriptions.
Calculates a match score and displays matched skills for transparency.
📄 Resume Upload Option: Users can upload resumes for profile completion (future upgrade: automatic skill extraction).

🧠 How the AI Recommendation Works

The system compares your skills (entered in your profile) with all job descriptions in the database.
For each match:
The more matched skills, the higher your recommendation score (up to 100).
Jobs are ranked by score and shown with a “matched skills” explanation.
This makes the system semi-intelligent — not just showing all jobs but showing personalized jobs first.

⚙️ Quickstart Guide
# 1️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run database migrations
python manage.py migrate

# 4️⃣ Create admin account
python manage.py createsuperuser

# 5️⃣ Start the server
python manage.py runserver

Visit:
Run the project locally:
1. Clone the repository
2. Install dependencies
3. Run: python manage.py runserver
4. Access the site at http://localhost:8000


🗄️ Project Structure
core/
 ┣ views.py               # Contains all main logic (AI system, login, CRUD, etc.)
 ┣ models.py              # User, JobPosting, Application, Bookmark, Profile
 ┣ forms.py               # User registration, job posting, and profile update forms
 ┣ templates/core/        # HTML templates (Bootstrap 5)
 ┣ static/core/css/       # Custom CSS
 ┗ ...

🧰 Tools & Technologies Used
Category	Tools
Framework	Django (Backend)
Frontend	HTML, CSS, Bootstrap 5
Database	SQLite
API	Django REST Framework (DRF)
Authentication	JWT + Django Auth System
AI Recommendation	Python-based keyword matching (skill-to-description)
Email System	Django send_mail with verification codes
Version Control	Git & GitHub

💡 Future Improvements

🤖 Advanced AI Matching: Use NLP or ML models for smarter recommendations.
📄 Resume Parsing: Automatically extract skills from uploaded resumes.
📬 Job Alerts: Send email notifications for new relevant job posts.
🧑‍💻 User Analytics: Track application trends and skill insights.


👩‍💻 Developer

Developed by: Faiza Qiyyum
University: Virtual University of Pakistan (VU)
Project Type: Final Year Project
Tools Used: Django, DRF, Bootstrap


🏁 Summary

AccessJobs is more than just a typical Django job portal —
it demonstrates how AI can enhance user experience by providing personalized job recommendations.
It’s simple enough for beginners to understand, yet powerful enough to inspire further research and development.
Thanks for your time.
