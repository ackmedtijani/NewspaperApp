# Generated by Django 4.1.1 on 2022-09-30 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminprofile',
            name='is_staff',
        ),
    ]
