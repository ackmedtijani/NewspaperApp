# Generated by Django 4.1.1 on 2022-11-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_remove_customuser_nationality_and_more'),
        ('articles', '0014_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(to='users.writer'),
        ),
    ]
