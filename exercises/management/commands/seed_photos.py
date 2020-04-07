# CMD click for BaseCommand Details
# class BaseCommand is at /Users/noopy/.local/share/virtualenvs/django-airbnb-clone-AcLC9Tzu/lib/python3.8/site-packages/django/core/management/base.py
from django.core.management.base import BaseCommand
from exercises.models import Exercise, Photo
from users.models import User

import pandas as pd
import numpy as np

import os

admin_username = os.environ.get("ADMIN_ID")
exercise_data = os.environ.get("EXERCISE_DATA")


class Command(BaseCommand):

    help = "This command creates photo in exercises"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:
            # image url from database
            df_django = pd.read_csv(exercise_data)
            # print(df_django.head())

            image_urls = df_django["photo_url"].to_list()
            names = df_django["exercise_name_web"].to_list()

            for n in range(0, len(image_urls)):
                one_exercise = Exercise.objects.get(name=names[n])
                # print(vars(one_exercise))

                Photo.objects.create(
                    caption="", image_url=image_urls[n], exercise=one_exercise,
                )

            # stand out
            self.stdout.write(
                self.style.SUCCESS("Initial Seeding - Exercise photos Created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Not initial seeding -- Superuser exists")
            )
