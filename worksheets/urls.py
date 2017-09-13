from django.conf.urls import url
from worksheets.views import WSView
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', WSView.as_view()),
]

#some change