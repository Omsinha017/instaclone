# Generated by Django 5.0.4 on 2024-04-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='caption_text',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
