# Generated by Django 4.1.1 on 2022-10-01 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_summary_alter_article_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('articles.article',),
        ),
        migrations.CreateModel(
            name='Politics',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('articles.article',),
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[('OPINION', 'opinion'), ('POLITICS', 'politics')], default='Type', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
