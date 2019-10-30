from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sprint(models.Model):
    number = models.PositiveSmallIntegerField(_('Número da sprint'))
    start_date = models.DateField(_('Data de início da sprint'))
    end_date = models.DateField(_('Data de finalização da sprint'))
    active = models.BooleanField(_('Sprint ativa?'))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['number'], name='number'),
            models.UniqueConstraint(fields=['active'], name='active')
        ]

    def __str__(self):
        active = 'Finalizada'
        if self.active:
            active = 'Ativa'
        return f'Sprint {self.number}: {self.start_date} - {self.end_date} ({active})'


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
    points = models.PositiveSmallIntegerField(_('Pontos da história'))
    duration = models.DurationField(_('Duração'))
    sprint = models.ForeignKey('Sprint', on_delete=models.PROTECT)
    responsible = models.ForeignKey('Developer', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.code} - {self.points}'


class StoryTaskType(models.Model):
    story = models.ForeignKey('Story', on_delete=models.PROTECT)
    task_type = models.ForeignKey('TaskType', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.story.code} - {self.task_type.title}'