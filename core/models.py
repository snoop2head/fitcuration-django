from django.db import models

# This is to skip repeating calling Django model.
# This will be used in all the other apps, except for Users app.
# Because User app already uses AbstractUser as model.


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(
        auto_now_add=True
    )  # get time and date when the model is created
    updated = models.DateTimeField(
        auto_now=True
    )  # get time and date whenever I update model

    # prevents saving time stamp model on database
    class Meta:
        abstract = True
