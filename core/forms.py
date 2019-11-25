from django import forms
from core.models import Sprint

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['start_date', 'end_date']

    def save(self, commit=True):
        last_sprint = Sprint.objects.all().order_by(
            'number'
        ).last()

        number_new_sprint = last_sprint.number + 1
        last_sprint.active = False
        last_sprint.save()

        new_sprint = Sprint(
            number=number_new_sprint,
            start_date=self.cleaned_data['start_date'],
            end_date=self.cleaned_data['end_date']
        )

        if commit:
            new_sprint.save()

        return new_sprint