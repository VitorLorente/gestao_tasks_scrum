"""scrum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from core.views import (
    StoriesList,
    StoryDetail,
    SprintsList,
    SprintDetail,
    StoryRepoint,
    Home,
    CloseSprint,
    ExtendSprint
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('story/', StoriesList.as_view(), name='stories-list'),
    path('story/<int:pk>/', StoryDetail.as_view(), name='story-detail'),
    path('sprint/', SprintsList.as_view(), name='sprints-list'),
    path('sprint/<int:pk>/', SprintDetail.as_view(), name='sprint-detail'),
    path('story/<int:pk>/repoint/', StoryRepoint.as_view(), name='sprint-repoint'),
    path('sprint/<int:pk>/close/', CloseSprint.as_view(), name='close-sprint'),
    path('extend-sprint/', ExtendSprint.as_view(), name='extend-sprint'),
]
