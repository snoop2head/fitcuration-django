# Generated by Django 3.0.3 on 2020-03-24 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_remove_category_exercises'),
        ('exercises', '0019_auto_20200324_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='exercise_category',
        ),
        migrations.AddField(
            model_name='exercise',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exercises', to='categories.Category'),
        ),
        migrations.DeleteModel(
            name='ExerciseCategory',
        ),
    ]
