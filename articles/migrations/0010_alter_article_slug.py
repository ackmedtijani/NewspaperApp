# Generated by Django 4.1.1 on 2022-11-15 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True),
        ),
    ]
