# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from worksheets.models import Jobs
from customers.models import Customer
from django.http import JsonResponse
from django.db.models import Sum


class WorkSheet(LoginRequiredMixin, ListView):
    template_name = "worksheet.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price'
        , 'job_notes'
    ]
    context_object_name='jobs'
    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.filter(window_cleaner=user, job_status='1')
        return queryset
    
class JobCreate(LoginRequiredMixin, CreateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    success_url = "/customers/"
    #TODO do a redirect to the customer job list
    initial = {'frequency': '4', 'job_status': '1'} #1 = 'due'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    
    def form_valid(self, form):
        return super(JobCreate, self).form_valid(form)

    def get_initial(self):
        #https://djangosnippets.org/snippets/2987/
        initials = super(JobCreate, self).get_initial()
        initials['customer'] = self.kwargs['customer']
        return initials

    def __init__(self, *args, **kwargs):
        super(JobCreate, self).__init__(*args, **kwargs)

class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Jobs
    fields = [
        'customer','scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
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
