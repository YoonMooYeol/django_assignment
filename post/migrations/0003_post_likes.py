# Generated by Django 4.2 on 2025-01-20 08:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="like_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
