from datetime import timedelta

from django import forms
from core.models import Sprint, Story, StorySprint

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['start_date', 'end_date']

    def save(self, commit=True):
        last_sprint = Sprint.objects.all().order_by(
            'number'
        ).last()
        if last_sprint:
            number_new_sprint = last_sprint.number + 1
            last_sprint.active = False
            last_sprint.save()
        else:
            number_new_sprint = 1

        new_sprint = Sprint(
            number=number_new_sprint,
            start_date=self.cleaned_data['start_date'],
            end_date=self.cleaned_data['end_date']
        )

        if commit:
            new_sprint.save()

        return new_sprint

class StoryForm(forms.ModelForm):
    sprint_pk = int()

    def __init__(self, *args, **kwargs):
        self.sprint_pk = kwargs.pop('sprint_pk')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Story
        exclude = ('completed', 'endpoints', 'duration',)
    
    def save(self, commit=True):
        story_sprint = Sprint.objects.get(pk=self.sprint_pk)
        new_story = Story(
            code=self.cleaned_data['code'],
            description=self.cleaned_data['description'],
            creation_date=self.cleaned_data['creation_date'],
            initial_points=self.cleaned_data['initial_points'],
            endpoints=self.cleaned_data['initial_points'],
            duration=timedelta(minutes=0),
            responsible=self.cleaned_data['responsible'],
            completed=False
        )

        if commit:
            new_story.save()

        StorySprint.objects.create(
            story=new_story,
            sprint=story_sprint
        )
        return new_story