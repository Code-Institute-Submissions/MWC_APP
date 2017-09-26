# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from customers.models import Customer
from braces.views import GroupRequiredMixin


class CustomersList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes',
        'property_type', 'frequency', 'franchise'
    ]
    template_name = 'customer_list.html'
    paginate_by = 10

    def get_queryset(self):
        franchise = self.request.user.franchise
        queryset = Customer.objects.filter(franchise=franchise)
        return queryset

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes', 'property_type', 'franchise',
        'frequency', 'url', 'latitude', 'longitude'

    ]
    template_name = 'customer_add.html'
    success_url = "/customers/"

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        return super(CustomerCreate, self).form_valid(form)

    def get_initial(self):
        # https://djangosnippets.org/snippets/2987/
        initials = super(CustomerCreate, self).get_initial()
        initials['franchise'] = self.request.user.franchise
        initials['frequency'] = '4'
        return initials

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    fields = [
        'title', 'first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'address_line_2',
        'address_line_3', 'city', 'county', 'postcode', 'customer_notes',
        'property_type', 'franchise', 'frequency', 'url', 'latitude', 'longitude'
    ]
    template_name = 'customer_add.html'
    success_url = "/customers/"

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        return super(CustomerUpdate, self).form_valid(form)

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = "/customers/"

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerJobList(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customer_job_list.html'
    paginate_by = 10

    def get_queryset(self):
        franchise = self.request.user.franchise
        queryset = Customer.objects.filter(franchise=franchise)
        return queryset

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerMap(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customer_map.html'
    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]
