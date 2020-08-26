# Generated by Django 3.1 on 2020-08-21 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0012_auto_20200821_0426'),
        ('events', '0007_auto_20200820_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.device'),
        ),
    ]