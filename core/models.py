from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db.models import Sum, Q


class Sprint(models.Model):
    number = models.PositiveSmallIntegerField(_('Número da sprint'))
    start_date = models.DateField(_('Data de início da sprint'))
    end_date = models.DateField(_('Data de finalização da sprint'))
    active = models.BooleanField(_('Sprint ativa?'), default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['number'], name='number'),
            models.UniqueConstraint(fields=['active'], condition=Q(active=True), name='active')
        ]

    def __str__(self):
        active = 'Finalizada'
        if self.active:
            active = 'Ativa'
        return f'Sprint {self.number}: {self.start_date} - {self.end_date} ({active})'

    @property
    def get_absolute_url(self):
        return reverse(
            'sprint-detail',
            args=[self.pk]
        )

    @property
    def is_active(self):
        active = 'Finalizada'
        if self.active:
            active = 'Ativa'
        return active

    def calculate_completed_points(self):
        points_sum = Story.objects.filter(
            sprint=self,
            completed=True
        ).aggregate(Sum('endpoints')).get('endpoints__sum')
        if points_sum:
            return points_sum
        return 0

    def calculate_open_points(self):
        points_sum = Story.objects.filter(
            sprint=self,
            completed=False
        ).aggregate(Sum('endpoints')).get('endpoints__sum')
        if points_sum:
            return points_sum
        return 0 


class Developer(models.Model):
    SENIORITY_CHOICE_SENIOR = ('senior', _('Sênior'))
    SENIORITY_CHOICE_PLENO = ('pleno', _('Pleno'))
    SENIORITY_CHOICE_JUNIOR = ('junior', _('Junior'))
    SENIORITY_CHOICES = (
        SENIORITY_CHOICE_SENIOR,
        SENIORITY_CHOICE_PLENO,
        SENIORITY_CHOICE_JUNIOR
    )

    name = models.CharField(_('Nome'), max_length=30)
    seniority = models.CharField(
        _('Senioridade'),
        choices=SENIORITY_CHOICES,
        max_length=7
    )

    def __str__(self):
        return self.name


class TaskType(models.Model):
    AREA_CHOICE_FRONT = ('front', _('Front'))
    AREA_CHOICE_BACK = ('back', _('Back'))
    AREA_CHOICE_HIBRIDO = ('hibrido', _('Hibrido'))
    AREA_CHOICES = (
        AREA_CHOICE_FRONT,
        AREA_CHOICE_BACK,
        AREA_CHOICE_HIBRIDO
    )

    title = models.CharField(_('Título'), max_length=50)
    description = models.TextField(_('Descrição'))
    development_area = models.CharField(
        _('Área de desenvolvimento'),
        max_length=10,
        choices=AREA_CHOICES
    )

    def __str__(self):
        return f'{self.title} - {self.get_development_area_display()}'


class Story(models.Model):
    code = models.CharField(_('Código no Jira'), max_length=7)
    description = models.TextField(_('Descrição'))
    creation_date = models.DateField(_('Data de criação'))
    initial_points = models.PositiveSmallIntegerField(_('Pontos iniciais da história'))
    endpoints = models.PositiveSmallIntegerField(_('Pontos finais da história'))
    duration = models.DurationField(_('Duração'))
    responsible = models.ForeignKey('Developer', on_delete=models.PROTECT)
    completed = models.BooleanField(_('História concluída?'))

    def __str__(self):
        return f'{self.code} - {self.endpoints}'

    @property
    def get_absolute_url(self):
        return reverse(
            'story-detail',
            args=[self.pk]
        )

    @property
    def is_completed(self):
        completed = 'Não'
        if self.completed:
            completed = 'Sim'
        return completed

    @property
    def creation_sprint(self):
        story_sprint = StorySprint.objects.filter(
            story=self
        ).select_related(
            'sprint'
        ).order_by('sprint__start_date').first()

        return story_sprint.sprint

    @property
    def end_sprint(self):
        story_sprint = StorySprint.objects.filter(
            story=self
        ).select_related(
            'sprint'
        ).order_by('sprint__start_date').last()

        return story_sprint.sprint

    @property
    def count_sprints(self):
        story_sprint_count = StorySprint.objects.filter(
            story=self
        ).select_related(
            'sprint'
        ).count()

        return story_sprint_count


class StorySprint(models.Model):
    story = models.ForeignKey(
        'Story',
        on_delete=models.PROTECT,
        related_name='story_storysprint'
    )
    sprint = models.ForeignKey(
        'Sprint',
        on_delete=models.PROTECT,
        related_name='sprint_storysprint'
    )


class StoryTaskType(models.Model):
    story = models.ForeignKey('Story', on_delete=models.PROTECT)
    task_type = models.ForeignKey('TaskType', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.story.code} - {self.task_type.title}'


class Impedment(models.Model):
    description = models.TextField(_('Descrição'))
    sprint = models.ForeignKey(
        'Sprint',
        on_delete=models.PROTECT,
        related_name='sprint_impedment'
    )
    date = models.DateField(_('Data'))
    reporter = models.ForeignKey(
        'Developer',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'Impedimento da sprint {self.sprint.number} em {self.date} relatado por {self.reporter.name}'


class BugTask(models.Model):
    description = models.TextField(_('Descrição'))
    sprint = models.ForeignKey(
        'Sprint',
        on_delete=models.PROTECT,
        related_name='sprint_bug'
    )
    creation_date = models.DateField(_('Data de criação'))
    responsible = models.ForeignKey(
        'Developer',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    duration = models.DurationField(_('Duração'), null=True, blank=True)
    code = models.CharField(_('Código no Jira'), max_length=7)

    def __str__(self):
        return f'Bug {self.code} - Sprint {self.sprint.number}'
