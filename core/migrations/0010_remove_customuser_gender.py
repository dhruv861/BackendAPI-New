# Generated by Django 4.2 on 2023-05-31 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_customuser_trainer_customuser_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
    ]
