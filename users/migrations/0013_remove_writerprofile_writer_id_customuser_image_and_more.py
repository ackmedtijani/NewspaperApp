# Generated by Django 4.1.1 on 2022-10-08 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writerprofile',
            name='writer_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(max_length=264, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='writerprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='writerprofile',
            name='education',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
