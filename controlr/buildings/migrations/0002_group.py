# Generated by Django 3.1 on 2020-08-18 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0008_auto_20200818_1210'),
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('devices', models.ManyToManyField(to='devices.Device')),
            ],
        ),
    ]