# Generated by Django 3.1 on 2020-08-20 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0011_device_created_ts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_change', models.BooleanField(default=True)),
                ('time_delta', models.DurationField()),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timers', to='devices.device')),
            ],
        ),
    ]