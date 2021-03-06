from django.contrib import admin
from django.urls import path, include

from core.views import (
    CloseSprint,
    ExtendSprint,
    Home,
    SprintCreate,
    SprintDetail,
    SprintsList,
    StoryDetail,
    StoriesList,
    StoryRepoint,
    story_create,
    complete_story
)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('story/', StoriesList.as_view(), name='stories-list'),
    path('story/<int:pk>/', StoryDetail.as_view(), name='story-detail'),
    path('story/<int:pk>/repoint/', StoryRepoint.as_view(), name='sprint-repoint'),
    path('extend-story/', ExtendSprint.as_view(), name='extend-story'),
    path('story/complete/', complete_story, name='complete-story'),
    path('sprint/', SprintsList.as_view(), name='sprints-list'),
    path('sprint/create/', SprintCreate.as_view(), name='sprint-create'),
    path('sprint/<int:pk>/', SprintDetail.as_view(), name='sprint-detail'),
    path('sprint/<int:pk>/close/', CloseSprint.as_view(), name='close-sprint'),
    path('sprint/<int:pk>/story/create/', story_create, name='create-story'),
]
