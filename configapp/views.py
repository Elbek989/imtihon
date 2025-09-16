from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *




from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from io import BytesIO
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Background
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    y = height - 50

    # Name and Title
    p.setFont("Helvetica-Bold", 26)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, "Elbek Nuraliyev")
    y -= 30

    p.setFont("Helvetica", 14)
    p.setFillColor(HexColor("#93C5FD"))
    p.drawString(40, y, "Python/Django Backend Developer")
    y -= 40

    # Summary
    summary = (
        "Energetic and detail-oriented backend developer with solid experience in building "
        "robust, scalable web applications using Python, Django, and PostgreSQL. Passionate about clean code, "
        "system design, and creating seamless user experiences. Strong background in REST APIs, Celery, and Docker."
    )
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#cfeef4"))
    for line in split_text(summary, 100):
        p.drawString(40, y, line)
        y -= 15

    y -= 20

    # Skills
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Skills")
    y -= 20

    skills = [
        "Python", "Django", "Django Rest Framework", "PostgreSQL", "Celery",
        "Redis", "Docker", "HTML5", "CSS3", "Git", "GitHub", "Linux", "API Development"
    ]
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))

    skill_line = " • ".join(skills)
    for line in split_text(skill_line, 100):
        p.drawString(50, y, line)
        y -= 15

    y -= 20

    # Experience
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Experience")
    y -= 20

    experiences = [
        ("2025 — Present", "Backend Developer — Acme Tech", "Developed scalable APIs, worked with Celery for async tasks, and managed PostgreSQL databases."),
        ("2024 — 2025", "Freelance Developer", "Delivered custom Django-based web solutions for clients in e-commerce and education."),
        ("2023 — 2024", "Junior Developer — CodeLab", "Assisted in development and deployment of internal CRM systems.")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for date, role, desc in experiences:
        p.drawString(50, y, f"{date} | {role}")
        y -= 15
        for line in split_text(desc, 100):
            p.drawString(60, y, f"• {line}")
            y -= 15
        y -= 5

    y -= 10

    # Education
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Education")
    y -= 20

    educations = [
        ("2024 — 2025", "Najot Ta'lim", "Backend Development (Python/Django)"),
        ("2022 — 2024", "High School", "Major in Mathematics and Computer Science")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for date, place, field in educations:
        p.drawString(50, y, f"{date} | {place}")
        y -= 15
        p.drawString(60, y, f"• {field}")
        y -= 20

    # Projects
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Portfolio Projects")
    y -= 20

    projects = [
        ("Shoply E-commerce", "Full-featured online store with cart, checkout, and admin panel (Django, DRF, PostgreSQL)."),
        ("Taxi Dispatcher", "System to manage taxi fleets, drivers, and trips with rating system (Django, Celery)."),
        ("Headless Blog CMS", "API-first blog with markdown support and headless architecture."),
        ("Task Manager", "To-do app with deadlines, tags, and user authentication.")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for title, desc in projects:
        p.drawString(50, y, f"{title}:")
        y -= 15
        for line in split_text(desc, 100):
            p.drawString(60, y, f"• {line}")
            y -= 15
        y -= 5

        if y < 100:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="elbek_nuraliyev_cv.pdf")



def split_text(text, max_chars):
    """
    Splits a long text into lines with max_chars characters
    """
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= max_chars:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines


@login_required(login_url='login')
def index(request):
    personalinfo = Person.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    projects = Project.objects.all()
    context = {
        'personalinfo': personalinfo,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects
    }
    return render(request, 'index.html',context=context)


@login_required(login_url='login')
def contact_message(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            ContactMessage.objects.create(name = name,email = email,message = message)
            messages.success(request, "Message sent successfully!")
            return redirect('index')
    else:
        form = ContactForm()

    return render(request,'contact.html',{'form':form})

def login_views(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect("index")
        else:
            messages.error(request, "Login yoki parol xato!")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("login")

