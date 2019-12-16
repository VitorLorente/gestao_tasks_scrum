from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
from django.db.models import Avg, Subquery, OuterRef, Sum
from django.http import Http404, HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
    CreateView,
)

from core.models import (
    Story,
    Sprint,
    Impedment,
    TaskType,
    StoryTaskType,
    BugTask,
    StorySprint,
)

from core.forms import (
    SprintForm,
    StoryForm,
)

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class StoryDetail(DetailView):
    model = Story
    template_name = 'story_detail.html'

    def get_object(self):
        obj = get_object_or_404(
            Story.objects.select_related(
                'responsible'
            ),
            pk=self.kwargs['pk'] 
        )
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        task_types = StoryTaskType.objects.filter(
            story=self.object
        ).select_related('task_type')



        sprints_to_extend = Sprint.objects.filter(
            end_date__gt=self.object.end_sprint.end_date
        ).order_by('number')

        data['sprints_to_extend'] = sprints_to_extend
        data['story_task_types'] = task_types
        data['page_active'] = 'story_detail'
        return data


@method_decorator(login_required, name='dispatch')
class SprintsList(ListView):
    model = Sprint
    template_name = 'sprints_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        sprints_count = Sprint.objects.count()

        form = SprintForm()
        
        sprints = Sprint.objects.all()
        next_sprint_number = 1

        if sprints:
            next_sprint_number = sprints.order_by(
                'number'
            ).last().number + 1

        data['next_sprint_number'] = next_sprint_number
        data['form'] = form
        data['sprints_count'] = sprints_count
        data['page_active'] = 'sprints_list'
        return data

    def get_queryset(self):
        queryset = Sprint.objects.annotate(
            total_points=Sum('sprint_storysprint__story__endpoints')
        ).all().order_by('-number')

        return queryset


@method_decorator(login_required, name='dispatch')
class SprintDetail(DetailView):
    model = Sprint
    template_name = 'sprint_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        stories = StorySprint.objects.filter(
            sprint=self.object
        ).select_related('story', 'sprint', 'story__responsible')

        impedments = Impedment.objects.filter(
            sprint=self.object
        ).select_related('reporter').order_by('-date')

        bugs = BugTask.objects.filter(
            sprint=self.object
        ).select_related('responsible').order_by('-creation_date')

        story_form = StoryForm(sprint_pk=self.object.pk)

        data['story_form'] = story_form
        data['sprint_stories'] = stories
        data['sprint_impedments'] = impedments
        data['sprint_bugs'] = bugs
        data['page_active'] = 'sprint_detail'
        return data

    def get_object(self):
        try:
            obj = Sprint.objects.annotate(
                total_points=Sum('sprint_storysprint__story__endpoints')
            ).get(pk=self.kwargs['pk'])
        except Sprint.DoesNotExist:
            raise Http404("A sprint não existe.")
        return obj


@method_decorator(login_required, name='dispatch')
class StoryRepoint(UpdateView):
    model = Story
    fields = ['endpoints']

    def get_success_url(self):
        return reverse(
            'story-detail',
            kwargs={'pk': self.kwargs['pk']}
        )


@method_decorator(login_required, name='dispatch')
class CloseSprint(UpdateView):
    model = Sprint
    fields = ['active']

    def get_success_url(self):
        return reverse(
            'sprint-detail',
            kwargs={'pk': self.kwargs['pk']}
        )


@method_decorator(login_required, name='dispatch')
class ExtendSprint(CreateView):
    model = StorySprint
    fields = ['story', 'sprint']

    def get_success_url(self):
        story_pk = self.request.POST['story']
        return reverse(
            'story-detail',
            kwargs={'pk': story_pk}
        )


@method_decorator(login_required, name='dispatch')
class SprintCreate(CreateView):
    model = Sprint
    form_class = SprintForm

    def get_success_url(self):
        return reverse(
            'sprints-list'
        )


@login_required
def story_create(request, pk):
    if request.POST:
        form = StoryForm(request.POST, sprint_pk=pk)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(
        reverse(
            'sprint-detail',
            kwargs={'pk': pk}
        )
    )
        
