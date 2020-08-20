# Generated by Django 3.1 on 2020-08-16 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
        ('devices', '0004_device_power'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='rooms.room'),
        ),
    ]