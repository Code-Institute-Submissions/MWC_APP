from django.conf.urls import url
from worksheets.views import WorkSheet
from django.conf import settings
from worksheets.views import JobCreate, JobUpdate, JobDelete, JobCheckIn, Invoice, JobDetails, Payment

from . import views

urlpatterns = [
    url(r'^$', WorkSheet.as_view(), name='worksheets'),
    url(r'new/(?P<customer>\d+)/$', JobCreate.as_view(), name='job_add'),
    url(r'(?P<pk>[0-9]+)/edit/$', JobUpdate.as_view(), name='job_update'),
    url(r'(?P<pk>[0-9]+)/delete/$', JobDelete.as_view(), name='job_delete'),
    url(r'(?P<pk>[0-9]+)/check_in/$', JobCheckIn.as_view(), name='job_check_in'),
    url(r'invoices/$', Invoice.as_view(), name='invoices'),
    url(r'(?P<pk>[0-9]+)/details/$', JobDetails.as_view(), name='job_check_in'),
    url(r'payment/$', Payment.as_view(), name='payment'),
]
