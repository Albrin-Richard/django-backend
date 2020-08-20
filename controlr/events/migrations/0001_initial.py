# Generated by Django 3.1 on 2020-08-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField(choices=[(100, 'Device Created'), (101, 'Room Created'), (102, 'Group Created'), (103, 'Room Group Created'), (104, 'Timer Created'), (105, 'Schedule Created'), (200, 'Device On'), (201, 'Device Off'), (202, 'Device On Timer'), (203, 'Device Off Timer'), (204, 'Device On Schedule'), (205, 'Device Off Schedule'), (300, 'Scene Triggered')], null=True)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('state_change', models.BooleanField(blank=True)),
            ],
        ),
    ]