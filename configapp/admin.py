from django.contrib import admin
from django.contrib import admin
from .models import Person, Skill, Experience, Education, Project, ContactMessage

admin.site.register(Person)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(ContactMessage)

# Register your models here.
