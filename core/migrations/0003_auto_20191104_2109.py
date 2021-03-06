# Generated by Django 2.2.6 on 2019-11-04 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_bugtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugtask',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Duração'),
        ),
        migrations.AlterField(
            model_name='bugtask',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Developer'),
        ),
    ]
