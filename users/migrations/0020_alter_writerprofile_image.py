# Generated by Django 4.1.1 on 2022-11-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_writerprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writerprofile',
            name='image',
            field=models.ImageField(blank=True, default='666201.png', upload_to='images/'),
        ),
    ]