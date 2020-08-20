# Generated by Django 3.1 on 2020-08-18 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_devicestate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicestate',
            name='device',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='devices.device'),
        ),
    ]