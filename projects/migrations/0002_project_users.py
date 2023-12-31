# Generated by Django 4.2.3 on 2023-07-18 21:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="users",
            field=models.ManyToManyField(
                related_name="projects", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
