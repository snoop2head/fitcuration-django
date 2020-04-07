# CMD click for BaseCommand Details
# class BaseCommand is at /Users/noopy/.local/share/virtualenvs/django-airbnb-clone-AcLC9Tzu/lib/python3.8/site-packages/django/core/management/base.py
from django.core.management.base import BaseCommand
from categories.models import Photo, Category
from users.models import User

import pandas as pd
import numpy as np
import os

admin_username = os.environ.get("ADMIN_ID")
category_data = os.environ.get("CATEGORY_DATA")


class Command(BaseCommand):

    help = "This command creates photo in exercises"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:
            df_django = pd.read_csv(category_data)

            image_urls = df_django["image_url"].to_list()
            names = df_django["category_name"].to_list()

            for n in range(0, len(names)):
                one_category = Category.objects.get(name=names[n])
                Photo.objects.create(
                    category=one_category, image_url=image_urls[n],
                )

            # stand out
            self.stdout.write(
                self.style.SUCCESS("Initial Seeding - Category photos Created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Not initial seeding -- Superuser exists")
            )
