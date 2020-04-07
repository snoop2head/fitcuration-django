# Using Listview
# https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/#listview-working-with-many-django-objects
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/

from . import models, forms
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator

# my python files for search engine
# from .recommender.word2vec_srch import yield_vector_list
from .recommender.tfidf_srch import TFIDFSearch

# importing Korean spell checker
# from chatspace import ChatSpace


def spellchecker(text):
    origin_text = text
    return origin_text


# proceed with errors
class HomeView(ListView):

    """ HomeView Definition """

    # programming class based views (not function based views)
    model = models.Exercise
    paginate_by = 12
    paginate_orphans = 3
    ordering = "?"
    page_kwarg = "page"
    # changing object_list into exercises
    context_object_name = "exercises"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# class based views
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/
class ExerciseDetail(DetailView):

    """" ExerciseDetail Definition """

    model = models.Exercise
    # pk_url_kwarg = "pk" # primary key as query is the default
    pass


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):
        name = request.GET.get("name")
        if name:
            # give form with user's GET request
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                filter_args = {}

                if name != "모든 운동":
                    # name is NOT exercise name, but search phrase input from user.
                    # spelling correction using: https://github.com/pingpong-ai/chatspace
                    name = spellchecker(name)

                    # Django filter search
                    # filter_args["name__contains"] = name

                    # Word2vec search
                    # yield_vector_list(models.Exercise.objects.all().values_list("name", flat=True), name)

                    # TFIDF search
                    tfidf_recommend_list = TFIDFSearch.tfidf_srch(name)
                    print(tfidf_recommend_list)

                    # multiple entries as __in
                    # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
                    filter_args["name__in"] = tfidf_recommend_list

                exercises_qs = models.Exercise.objects.filter(**filter_args).order_by(
                    "-created"
                )
                # print(exercises_qs)

                # Paginating Search Result
                paginator = Paginator(exercises_qs, 8, orphans=3)
                page = request.GET.get("page", 1)
                exercises = paginator.get_page(page)

                get_copy = request.GET.copy()
                parameters = get_copy.pop("page", True) and get_copy.urlencode()

                return render(
                    request,
                    "exercises/search.html",
                    {
                        "form": form,
                        "exercises": exercises,
                        "parameters": parameters,
                        "search_name": name,
                    },
                )
        else:
            # empty form without validation
            form = forms.SearchForm()

        # precautionary measure when people modify url queries  without using search bar
        return render(request, "exercises/search.html", context={"form": form})

    pass
