# Generated by Django 4.1.1 on 2022-11-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_readerprofile_user_alter_writerprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writerprofile',
            name='image',
            field=models.ImageField(blank=True, default='default_user.png', upload_to='images/'),
        ),
    ]
