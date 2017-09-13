# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Jobs
from django.views.generic import ListView

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class WSView(LoginRequiredMixin, ListView):
    template_name = "WS.html"
    model = Jobs