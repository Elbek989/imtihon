"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config import settings
from configapp import views
from configapp.views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_views, name='login'),
    path('add_project/', views.edit_projects, name='add_project'),
    path('edit_projects/', views.edit_projects, name='edit_projects'),
    path('send-message/', views.send_message, name='send_message'),

    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls,name='admin'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('contact/', views.contact_message, name='contact'),
    path('download-cv/', views.download_cv, name='download_cv')


]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)