# Generated by Django 5.1.3 on 2024-11-23 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_delete_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='photo',
        ),
    ]