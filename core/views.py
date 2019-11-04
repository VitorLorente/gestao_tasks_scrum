from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.db.models import Avg, Subquery, OuterRef, Sum
from django.http import Http404

from core.models import Story, Sprint, Impedment, TaskType, StoryTaskType


class Home(TemplateView):
    template_name = 'home.html'


class StoriesList(ListView):
    model = Story
    template_name = 'stories_list.html'

    def get_queryset(self):
        points_filter = self.request.GET.get('points', None)
        if points_filter and int(points_filter) > 0:
            return Story.objects.filter(
                endpoints=points_filter
            ).order_by('creation_date')
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        points_filter = self.request.GET.get('points', None)
        data['duration_average'] = None
        data['points'] = None
        if points_filter and int(points_filter) > 0:
            duration_average = Story.objects.filter(
                endpoints=points_filter
            ).aggregate(Avg('duration'))['duration__avg']
            data['duration_average'] = duration_average
            data['points'] = points_filter
        data['page_active'] = 'stories_list'
        return data


class StoryDetail(DetailView):
    model = Story
    template_name = 'story_detail.html'

    def get_object(self):
        obj = get_object_or_404(
            Story.objects.select_related(
                'sprint', 'responsible'
            ),
            pk=self.kwargs['pk'] 
        )
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        task_types = StoryTaskType.objects.filter(
            story=self.object
        ).select_related('task_type')

        data['story_task_types'] = task_types
        data['page_active'] = 'story_detail'
        return data


class SprintsList(ListView):
    model = Sprint
    template_name = 'sprints_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        sprints_count = Sprint.objects.count()
        data['sprints_count'] = sprints_count
        data['page_active'] = 'sprints_list'
        return data

    def get_queryset(self):
        queryset = Sprint.objects.annotate(
            total_points=Sum('sprint_story__endpoints')
        ).all().order_by('-number')

        return queryset

class SprintDetail(DetailView):
    model = Sprint
    template_name = 'sprint_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        stories = Story.objects.filter(
            sprint=self.object
        ).select_related('responsible')

        impedments = Impedment.objects.filter(
            sprint=self.object
        ).select_related('reporter')

        data['sprint_stories'] = stories
        data['sprint_impedments'] = impedments
        data['page_active'] = 'sprint_detail'
        return data

    def get_object(self):
        try:
            obj = Sprint.objects.annotate(
                total_points=Sum('sprint_story__endpoints')
            ).get(pk=self.kwargs['pk'])
        except Sprint.DoesNotExist:
            raise Http404("A sprint não existe.")
        return obj

class StoryRepoint(UpdateView):
    model = Story
    fields = ['endpoints']

    def get_success_url(self):
        return reverse(
            'story-detail',
            kwargs={'pk': self.kwargs['pk']}
        )