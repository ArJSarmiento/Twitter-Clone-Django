# Generated by Django 3.2.3 on 2021-07-30 05:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210729_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='my_followers',
        ),
        migrations.AddField(
            model_name='followers',
            name='my_following',
            field=models.ManyToManyField(blank=True, related_name='my_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
