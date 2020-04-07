# django views, urls modules
from django.views.generic import DetailView

# my python files
from . import models


# Create your views here.

# class based views
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/
class CategoryDetail(DetailView):

    """" CategoryDetail Definition """

    model = models.Category
    # pk_url_kwarg = "pk" # primary key as query is the default
