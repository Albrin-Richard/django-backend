# Generated by Django 3.1 on 2020-09-16 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_auto_20200903_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='time',
        ),
        migrations.AddField(
            model_name='schedule',
            name='trigger_time',
            field=models.DateTimeField(null=True),
        ),
    ]
