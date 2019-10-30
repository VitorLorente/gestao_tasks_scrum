from django.shortcuts import render
from django.views.generic import ListView

from core.models import Story


class StoriesList(ListView):
    model = Story
    template_name = 'stories_list.html'

    def get_queryset(self):
        points_filter = self.request.GET.get('points', None)
        if points_filter:
            return Story.objects.filter(
                points=points_filter
            ).order_by('creation_date')
        return Story.objects.all()