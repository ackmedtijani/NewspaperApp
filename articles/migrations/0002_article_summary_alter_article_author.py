# Generated by Django 4.1.1 on 2022-09-28 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_first_name_and_more'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.CharField(default='The person is coming here', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.writer'),
        ),
    ]