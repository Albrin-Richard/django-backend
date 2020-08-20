# Generated by Django 3.1 on 2020-08-20 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0004_auto_20200819_1307'),
        ('rules', '0003_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='buildings.building'),
        ),
    ]