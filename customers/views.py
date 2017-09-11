# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
from models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "CustomerList.html"
