# Generated by Django 4.1.1 on 2022-11-14 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/'),
        ),
    ]