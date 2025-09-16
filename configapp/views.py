from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *




from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

from configapp.models import Person, Skill, Experience, Education, Project

def split_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

@login_required(login_url='login')
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Background
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    y = height - 50

    # Person ma'lumotlari (faqat bitta Person mavjud deb faraz qilamiz)
    about = Person.objects.first()
    if not about:
        about = Person(full_name="No Name", about_me="No information available.")

    # Name and Contact
    p.setFont("Helvetica-Bold", 26)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, about.full_name)
    y -= 30

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#93C5FD"))
    contact_info = f"Email: {about.email}"
    if about.phone:
        contact_info += f" | Phone: {about.phone}"
    p.drawString(40, y, contact_info)
    y -= 40

    # About Me / Summary
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#cfeef4"))
    for line in split_text(about.about_me or "", 100):
        p.drawString(40, y, line)
        y -= 15

    y -= 20

    # Skills
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Skills")
    y -= 20

    skills = Skill.objects.all()
    skill_list = []
    for skill in skills:
        if skill.level:
            skill_list.append(f"{skill.name} ({skill.level})")
        else:
            skill_list.append(skill.name)

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    skill_line = " • ".join(skill_list)
    for line in split_text(skill_line, 100):
        p.drawString(50, y, line)
        y -= 15

    y -= 20

    # Experience
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Experience")
    y -= 20

    experiences = Experience.objects.order_by('-start_date')
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for exp in experiences:
        start = exp.start_date.strftime("%Y")
        end = exp.end_date.strftime("%Y") if exp.end_date else "Present"
        p.drawString(50, y, f"{start} — {end} | {exp.title} at {exp.company}")
        y -= 15
        for line in split_text(exp.description, 100):
            p.drawString(60, y, f"• {line}")
            y -= 15
        y -= 5
        if y < 100:
            p.showPage()
            y = height - 50

    y -= 10

    # Education
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Education")
    y -= 20

    educations = Education.objects.order_by('-start_date')
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for edu in educations:
        start = edu.start_date.strftime("%Y")
        end = edu.end_date.strftime("%Y") if edu.end_date else "Present"
        p.drawString(50, y, f"{start} — {end} | {edu.degree} — {edu.institution}")
        y -= 20
        if y < 100:
            p.showPage()
            y = height - 50

    # Projects
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Portfolio Projects")
    y -= 20

    projects = Project.objects.all()
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for proj in projects:
        p.drawString(50, y, f"{proj.title}:")
        y -= 15
        for line in split_text(proj.description, 100):
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


@login_required(login_url='login')
def index(request):
    about = Person.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    projects = Project.objects.all()
    context = {
        'about':about,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects
    }
    return render(request, 'index.html', context=context)




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

