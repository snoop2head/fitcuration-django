from django.core.management.base import BaseCommand
from exercises.models import Video, Exercise
from users.models import User

import pandas as pd
import numpy as np
import os

admin_username = os.environ.get("ADMIN_ID")
exercise_data = os.environ.get("EXERCISE_DATA")


class Command(BaseCommand):

    help = "This command creates videos in exercises"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:

            df_django = pd.read_csv(exercise_data)

            # print(df_django.head())
            names = df_django["exercise_name_web"].to_list()
            video_urls = df_django["video_url"].to_list()

            for n in range(0, len(names)):
                one_exercise = Exercise.objects.get(name=names[n])
                Video.objects.create(
                    video_caption="", video_url=video_urls[n], exercise=one_exercise,
                )

            self.stdout.write(
                self.style.SUCCESS("Initial Seeding - Exercise Videos Created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Not initial seeding -- Superuser exists")
            )
