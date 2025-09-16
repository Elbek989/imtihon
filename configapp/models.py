from django.db import models

class Person(models.Model):

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.full_name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50, blank=True, null=True)  # Masalan, Beginner, Intermediate, Expert

    def __str__(self):
        return self.name


class Experience(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
