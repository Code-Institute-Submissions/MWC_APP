from django.conf.urls import url
from expenses.views import ExpensesList, ExpenseCreate, ExpenseDelete, ExpenseUpdate
from django.conf import settings

from . import views


urlpatterns = [
    url(r'^$', ExpensesList.as_view()),
    url(r'add/$', ExpenseCreate.as_view(), name='expenses-add'),
    url(r'(?P<pk>[0-9]+)/$', ExpenseUpdate.as_view(), name='expenses-update'),
    url(r'(?P<pk>[0-9]+)/delete/$', ExpenseDelete.as_view(), name='expenses-delete'),
]
