from django.core.management.base import BaseCommand
from exercises.models import Exercise
from categories.models import Category
from users.models import User

import pandas as pd
import numpy as np
import os

admin_username = os.environ.get("ADMIN_ID")
exercise_data = os.environ.get("EXERCISE_DATA")


class Command(BaseCommand):

    help = "This command edits values in exercises"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:

            # get all exercise objects
            # you should not do this in real life! We only have 50 users
            # all_exercises = Exercise.objects.all()
            # print(all_exercises)

            df_django = pd.read_csv(exercise_data)

            short_names = df_django["exercise_category_short_name"].to_list()
            names = df_django["exercise_name_web"].to_list()

            for n in range(0, len(names)):
                one_exercise = Exercise.objects.filter(name=names[n])
                one_category = Category.objects.filter(short_name=short_names[n])

                # print(one_exercise)
                # print(one_category)
                # print(vars(one_exercise))
                # print(dir(one_exercise))
                # update with values: https://docs.djangoproject.com/en/2.2/ref/models/querysets/#values
                one_exercise.update(category=one_category.values("id"))

            self.stdout.write(
                self.style.SUCCESS("Initial Seeding - Categories matched to exercises")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Not initial seeding -- Superuser exists")
            )
