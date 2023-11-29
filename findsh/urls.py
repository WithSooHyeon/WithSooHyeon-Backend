from django.urls import include, path
from .views import *

urlpatterns = [
    path("", FindSHList.as_view()),
    path("<int:pk>", FindSHDetail.as_view()),
    path("search", FindSHSearch.as_view()),
]