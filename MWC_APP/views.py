# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View


class LoginSuccess(View):
    """ redirects to different urls depending on user group """
    def get(self, request):
        groups = request.user.groups.all().values_list('name', flat=True)
        if 'window_cleaner' in groups:
            return redirect("worksheets")
        else:
            return redirect("customers")
        # TODO: other user groups
