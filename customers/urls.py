from django.conf.urls import url
from customers.views import CustomerListView
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', CustomerListView.as_view()),
]