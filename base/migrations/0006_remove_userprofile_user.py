# Generated by Django 4.1.2 on 2022-11-21 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]
