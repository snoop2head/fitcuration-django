#!/bin/bash
# python ./manage.py flush --no-input
python ./manage.py collectstatic --no-input
python ./manage.py makemigrations
python ./manage.py migrate
# python ./manage.py compilemessages
python ./manage.py seed_exercises
python ./manage.py seed_photos
python ./manage.py seed_videos
python ./manage.py seed_categories
python ./manage.py match_exercises_to_categories
python ./manage.py seed_category_images
python ./manage.py createsu
python ./manage.py runserver 0.0.0.0:5000