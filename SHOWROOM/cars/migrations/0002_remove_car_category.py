# Generated by Django 5.1.3 on 2024-11-21 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='category',
        ),
    ]
