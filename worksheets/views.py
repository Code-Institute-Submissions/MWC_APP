# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from worksheets.models import Jobs
from customers.models import Customer
from django.http import JsonResponse

class WSView(LoginRequiredMixin, TemplateView):
    template_name = "WS.html"

class JobCreate(LoginRequiredMixin, CreateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'frequency', 'job_status', 'payment_status', 'job_notes', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    success_url = "/customers/"
    #TODO do a redirect to the customer job list
    initial = {'frequency': '4', 'job_status': '1'}

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def form_valid(self, form):
        return super(JobCreate, self).form_valid(form)

    def get_initial(self):
        #get customer id from kwargs and update 'initial' https://djangosnippets.org/snippets/2987/
        initials = super(JobCreate, self).get_initial()
        initials['customer'] = self.kwargs['customer']
        return initials

    def __init__(self, *args, **kwargs):
        super(JobCreate, self).__init__(*args, **kwargs)

class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Jobs
    fields = [
        'customer','scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'frequency', 'job_status', 'payment_status', 'job_notes', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    success_url = "/customers/"

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def form_valid(self, form):
        return super(JobUpdate, self).form_valid(form)

class JobDelete(LoginRequiredMixin, DeleteView):
    model = Jobs
    success_url = "/customers/"
