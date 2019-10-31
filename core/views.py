from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Avg

from core.models import Story


class StoriesList(ListView):
    model = Story
    template_name = 'stories_list.html'

    def get_queryset(self):
        points_filter = self.request.GET.get('points', None)
        if points_filter and int(points_filter) > 0:
            return Story.objects.filter(
                points=points_filter
            ).order_by('creation_date')
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        points_filter = self.request.GET.get('points', None)
        data['duration_average'] = None
        data['points'] = None
        if points_filter and int(points_filter) > 0:
            duration_average = Story.objects.filter(
                points=points_filter
            ).aggregate(Avg('duration'))['duration__avg']
            data['duration_average'] = duration_average
            data['points'] = points_filter
        return data