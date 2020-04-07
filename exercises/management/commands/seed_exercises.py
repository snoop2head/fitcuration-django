# CMD click for BaseCommand Details
# class BaseCommand is at /Users/noopy/.local/share/virtualenvs/django-airbnb-clone-AcLC9Tzu/lib/python3.8/site-packages/django/core/management/base.py
from django.core.management.base import BaseCommand
from exercises.models import Exercise
from users.models import User

import pandas as pd
import numpy as np
import os

admin_username = os.environ.get("ADMIN_ID")
exercise_data = os.environ.get("EXERCISE_DATA")


class Command(BaseCommand):

    help = "This command creates exercises"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:
            df_django = pd.read_csv(exercise_data)

            print(df_django.head())

            names = df_django["exercise_name_web"].to_list()
            summaries = df_django["summary"].to_list()
            descriptions = df_django["description"].to_list()

            for n in range(0, len(names)):
                Exercise.objects.create(
                    name=names[n], summary=summaries[n], description=descriptions[n],
                )
            # stand out
            self.stdout.write(
                self.style.SUCCESS("Initial seeding -- exercises created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Not initial seeding -- Superuser exists")
            )
