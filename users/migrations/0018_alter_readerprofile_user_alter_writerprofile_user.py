# Generated by Django 4.1.1 on 2022-10-24 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_writerprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.reader'),
        ),
        migrations.AlterField(
            model_name='writerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.writer'),
        ),
    ]
