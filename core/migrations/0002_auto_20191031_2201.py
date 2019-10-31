# Generated by Django 2.2.6 on 2019-10-31 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='sprint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sprint_story', to='core.Sprint'),
        ),
    ]
