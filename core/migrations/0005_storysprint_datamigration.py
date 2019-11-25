from django.db import migrations

def story_sprint_migrate(apps, schema_editor):
    Story = apps.get_model('core', 'Story')
    StorySprint = apps.get_model('core', 'StorySprint')
    list_storysprint = list()
    for story in Story.objects.all().select_related('sprint'):
        new_story_sprint = StorySprint(
            story=story,
            sprint=story.sprint
        )
        list_storysprint.append(new_story_sprint)
    StorySprint.objects.bulk_create(list_storysprint)
    
        
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_storysprint'),
    ]

    operations = [
        migrations.RunPython(story_sprint_migrate),
    ]