from django.conf.urls import url
from worksheets.views import WSView
from django.conf import settings
from worksheets.views import JobCreate, JobUpdate, JobDelete

from . import views

urlpatterns = [
    url(r'^$', WSView.as_view()),
    url(r'new/(?P<customer>\d+)/$', JobCreate.as_view(), name='job_add'),
    url(r'(?P<pk>[0-9]+)/$', JobUpdate.as_view(), name='job_update'),
    url(r'(?P<pk>[0-9]+)/delete/$', JobDelete.as_view(), name='job_delete'),
]

#some change