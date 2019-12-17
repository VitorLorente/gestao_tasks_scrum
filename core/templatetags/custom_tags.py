from django import template

from core.models import StorySprint, Sprint


register = template.Library()

@register.simple_tag(name='extended')
def status_story_extended(combine_story_sprint, sprint_pk):
    sprint = Sprint.objects.get(pk=sprint_pk)
    combines = StorySprint.objects.filter(
        story=combine_story_sprint.story,
        sprint__start_date__gt=sprint.start_date
    )

    if combines.count() > 0:
        return "Sim"
    return "Não"

@register.simple_tag(name='completed')
def status_story_completed(combine_story_sprint, sprint_pk):
    if not combine_story_sprint.story.completed:
        return 'Não'

    sprint = Sprint.objects.get(pk=sprint_pk)

    combines = StorySprint.objects.filter(
        story=combine_story_sprint.story
    ).order_by('sprint__number')

    last_sprint = combines.last().sprint

    if combine_story_sprint.story.completed and sprint == last_sprint:
        return 'Sim'

    return 'Não'
