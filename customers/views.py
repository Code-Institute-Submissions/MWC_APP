# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from customers.models import Customer
from worksheets.models import Jobs
from accounts.models import User

class CustomersList(LoginRequiredMixin, ListView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type','frequency', 'franchise'
    ]
    template_name = 'customer_list.html'
    paginate_by = 10
    def get_queryset(self):
        franchise = self.request.user.franchise
        queryset = Customer.objects.filter(franchise=franchise)
        return queryset

class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type', 'franchise', 'frequency'
    ]
    template_name = 'customer_add.html'
    success_url = "/customers/"
    
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)    
    def form_valid(self, form):        
        return super(CustomerCreate, self).form_valid(form)

    def get_initial(self):
        #https://djangosnippets.org/snippets/2987/
        initials = super(CustomerCreate, self).get_initial()
        initials['franchise'] = self.request.user.franchise
        initials['frequency'] = '4'
        return initials

class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type', 'franchise', 'frequency'
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
    template_name = 'customer_job_list.html'
    paginate_by = 10
    def get_queryset(self):
        franchise = self.request.user.franchise
        queryset = Customer.objects.filter(franchise=franchise)
        return queryset
