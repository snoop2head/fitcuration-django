# Generated by Django 3.0.3 on 2020-02-25 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='exercise_photos'),
        ),
    ]
