# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import UpdateView, DeleteView, CreateView, ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.db import connection, DatabaseError
from django.urls import reverse
from braces.views import GroupRequiredMixin, JSONResponseMixin
from worksheets.models import Jobs, Payment_status
from datetime import datetime, timedelta
import stripe


class WorkSheet(GroupRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "worksheet.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price', 'job_notes'
    ]
    context_object_name = 'jobs'

    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.all().filter(window_cleaner=user, job_status='1', allocated_date__isnull=False)
        #jobs must be allocatedand due before being checked in
        return queryset
    group_required = u"window_cleaner"


class JobCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price', 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
    ]
    template_name = 'job_add.html'
    initial = {'frequency': '4', 'job_status': '1'}  # 1 = 'due'

    def get_success_url(self):
        print self.kwargs['customer']
        return reverse('customer_job_list', kwargs={
                       'pk': self.kwargs['customer']})

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        return super(JobCreate, self).form_valid(form)

    def get_initial(self):
        # https://djangosnippets.org/snippets/2987/
        initials = super(JobCreate, self).get_initial()
        initials['customer'] = self.kwargs['customer']
        return initials

    def __init__(self, *args, **kwargs):
        super(JobCreate, self).__init__(*args, **kwargs)

    group_required = u"window_cleaner"


class JobUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Jobs
    fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price', 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
    ]
    template_name = 'job_add.html'

    def get_success_url(self):
        return reverse('customer_job_list', kwargs={'pk': id})

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
            except DatabaseError as e:
                print e
                return HttpResponse(status=500)
            finally:
                cursor.close()

    group_required = u"window_cleaner"


class Invoice(GroupRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "invoice.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price', 'job_notes'
    ]
    context_object_name = 'invoices'

    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.filter(
            window_cleaner=user,
            job_status__job_status_description='completed',
            invoiced=False,
            scheduled_date__gt=(datetime.today() - timedelta(weeks=12))
            # TODO: temporary 12 week filter as jobs have not been invoiced
        )
        return queryset
    group_required = u"window_cleaner"

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    title = "TITLE"


class JobDetails(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    model = Jobs
    template_name = "job_details.html"
    group_required = u"window_cleaner"


class Payment(GroupRequiredMixin, LoginRequiredMixin, View):
    group_required = u"window_cleaner"

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        amount = int(request.POST['amount'])
        print amount
        charge = stripe.Charge.create(
            amount=amount,
            currency='gbp',
            description="Window Cleaner Commission Payment",
            source=token,
        )
        return redirect('invoices')
        # TODO: return charge etc.


class Owings(GroupRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "owings.html"
    model = Jobs
    fields = [
        'customer', 'allocated_date', 'price', 'job_notes'
    ]
    context_object_name = 'jobs'

    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.filter(
            window_cleaner=user,
            payment_status__payment_status_description='owed',
            job_status__job_status_description='completed')
        return queryset

    group_required = u"window_cleaner"


class OwingPaid(JSONResponseMixin, GroupRequiredMixin,
                LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        job = Jobs.objects.get(pk=self.kwargs['pk'])
        paid_status = Payment_status.objects.get(
                payment_status_description='paid')
        job.payment_status = paid_status
        try:            
            job.save()
            json_dict = {
                'message': "Job has been checked in as paid",
                'result': "success"

            }
        except DatabaseError as e:
            json_dict = {
                'message': "There was an error saving the record (" + e.message + ")",
                'result': "failure"
            }
        return self.render_json_response(json_dict)

    group_required = u"window_cleaner"
