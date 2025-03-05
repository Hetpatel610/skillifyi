from django.db import migrations

def assign_default_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Blog = apps.get_model('users', 'Blog')
    Resource = apps.get_model('users', 'Resource')
    Event = apps.get_model('users', 'Event')

    # Get a default user to assign (you can customize this to your needs)
    default_user = User.objects.first()

    # Assign the default user to existing blog entries
    if default_user:
        for blog in Blog.objects.all():
            blog.user = default_user
            blog.save()

        for resource in Resource.objects.all():
            resource.user = default_user
            resource.save()

        for event in Event.objects.all():
            event.user = default_user
            event.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_blog_event'),  # Make sure this is the correct previous migration name
    ]

    operations = [
        migrations.RunPython(assign_default_user),
    ]