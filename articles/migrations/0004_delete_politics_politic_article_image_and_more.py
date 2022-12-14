# Generated by Django 4.1.1 on 2022-10-08 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_opinion_politics_article_type_article_updated'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Politics',
        ),
        migrations.CreateModel(
            name='Politic',
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
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[('OPINION', 'opinion'), ('POLITICS', 'politics')], max_length=255, verbose_name='Type'),
        ),
    ]
