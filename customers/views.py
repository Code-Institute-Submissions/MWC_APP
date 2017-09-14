# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from customers.models import Customer
from worksheets.models import Jobs

class CustomersList(LoginRequiredMixin, ListView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type'
    ]
    template_name = 'customer_list.html'

class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type', 'franchise'
    ]
    template_name = 'customer_add.html'
    success_url = "/customers/"
    # def form_invalid(self, form):
    #     return JsonResponse(form.errors, status=400)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CustomerCreate, self).form_valid(form)

class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type', 'franchise'
    ]
    template_name = 'customer_add.html'
    success_url = "/customers/"
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
    def form_valid(self, form):
        return super(CustomerUpdate, self).form_valid(form)

class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = "/customers/"

class CustomerJobList(LoginRequiredMixin, DetailView):
    model = Customer

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(CustomerJobList, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['job_list'] = Job.objects.all()
    #     return context

    template_name = 'customer_job_list.html'