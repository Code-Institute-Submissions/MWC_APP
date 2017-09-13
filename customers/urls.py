from django.conf.urls import url
from customers.views import CustomersList, CustomerCreate, CustomerUpdate, CustomerDelete
#from django.conf import settings


#from . import views

urlpatterns = [
    url(r'^$', CustomersList.as_view()),
    url(r'new/$', CustomerCreate.as_view(), name='customers_add'),
    url(r'(?P<pk>[0-9]+)/$', CustomerUpdate.as_view(), name='customers_update'),
    url(r'(?P<pk>[0-9]+)/delete/$', CustomerDelete.as_view(), name='customers_delete'),
]