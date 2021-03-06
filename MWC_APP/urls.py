"""MWC_APP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
import debug_toolbar
from views import LoginSuccess
from django.http import HttpResponseRedirect


urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect('/login/')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^worksheets/', include('worksheets.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^customers/', include('customers.urls')),
    url(r'^expenses/', include('expenses.urls')),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/login/'}, name='logout'),
    url(r'login_success/$', LoginSuccess.as_view(), name='login_success')
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
# necessary to collect static files from app/static directories
