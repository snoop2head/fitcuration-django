# django app
from django import forms

# my python files
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(initial="모든 운동")
