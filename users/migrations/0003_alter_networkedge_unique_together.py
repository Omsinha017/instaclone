# Generated by Django 5.0.4 on 2024-04-26 13:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_user_networkedge'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='networkedge',
            unique_together={('from_user', 'to_user')},
        ),
    ]