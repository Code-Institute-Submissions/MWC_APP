# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from worksheets.models import Jobs
from django.db import connection


class WorkSheet(GroupRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "worksheet.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price'
        , 'job_notes'
    ]
    context_object_name = 'jobs'
    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.filter(window_cleaner=user, job_status='1')
        return queryset
    group_required = u"window_cleaner"

class JobCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    success_url = 'customer_job_list'
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

    group_required = u"window_cleaner"

class JobUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price'
        , 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    success_url = "/customers/"

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        return super(JobUpdate, self).form_valid(form)

    group_required = u"window_cleaner"

class JobDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Jobs
    success_url = "/customers/"
    group_required = u"window_cleaner"

class JobCheckIn(GroupRequiredMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            if request.POST['payment_status'] == 'paid':
                payment_status = 1
            else:
                payment_status = 2
            params = (int(request.POST['jobid']), payment_status)
            try:
                cursor.execute('{CALL dbo.sp_complete_job (%d,%d)}' % params)
                return HttpResponse(status=201)
            except Exception as e:
                return HttpResponse(status=500)

    group_required = u"window_cleaner"

class Invoice(GroupRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "invoices.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price'
        , 'job_notes'
    ]
    context_object_name = 'invoices'
    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.filter(window_cleaner=user, job_status='2')
        return queryset
    group_required = u"window_cleaner"
  
