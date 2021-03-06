# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from customers.models import Customer
from braces.views import GroupRequiredMixin
from django.db.models import Q


class CustomersList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """ lists customers, with a filter """

    model = Customer
    context_object_name = 'customers'
    fields = [
        'title',
        'first_name',
        'last_name',
        'email',
        'mobile',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'city',
        'county',
        'postcode',
        'customer_notes',
        'property_type',
        'frequency',
        'franchise']
    template_name = 'customer_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        """ office_admin can only see customers from the same franchise """
        franchise = self.request.user.franchise
        self.queryset = Customer.objects.filter(franchise=franchise)
        return super(CustomersList, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ filtered results """
        franchise = self.request.user.franchise
        try:
            if request.POST['action'] == 'filter':
                txt = request.POST['input_search']
                self.queryset = Customer.objects.filter(
                    Q(address_line_1__icontains=txt) |
                    Q(first_name__icontains=txt) |
                    Q(last_name__icontains=txt) |
                    Q(title__icontains=txt),
                    franchise=franchise
                )
            else:
                self.queryset = Customer.objects.filter(franchise=franchise)
        except KeyError:
            # empty or incomplete POST key dict: return all records
            self.queryset = Customer.objects.filter(franchise=franchise)
        return super(CustomersList, self).get(request, *args, **kwargs)

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    """ view to create a new customer """

    model = Customer
    fields = [
        'title',
        'first_name',
        'last_name',
        'email',
        'mobile',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'city',
        'county',
        'postcode',
        'customer_notes',
        'property_type',
        'franchise',
        'frequency',
        'url',
        'latitude',
        'longitude']
    template_name = 'customer_add.html'

    # used for debugging:
    # def form_invalid(self, form):
    #     return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        return super(CustomerCreate, self).form_valid(form)

    def get_initial(self):
        # https://djangosnippets.org/snippets/2987/
        initials = super(CustomerCreate, self).get_initial()
        initials['franchise'] = self.request.user.franchise  # hidden input
        initials['frequency'] = '4'     # default frequency in weeks
        return initials

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    """ view to update existing customers """

    model = Customer
    fields = [
        'title',
        'first_name',
        'last_name',
        'email',
        'mobile',
        'address_line_1',
        'address_line_2',
        'address_line_3',
        'city',
        'county',
        'postcode',
        'customer_notes',
        'property_type',
        'franchise',
        'frequency',
        'url',
        'latitude',
        'longitude']
    template_name = 'customer_add.html'

    # for debugging:
    # def form_valid(self, form):
    #     return super(CustomerUpdate, self).form_valid(form)

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    """ view to delete existing customers """

    model = Customer
    success_url = "/customers/"

    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]


class CustomerJobList(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    """ view to list jobs for each customer """

    model = Customer
    template_name = 'customer_job_list.html'
    # paginate_by = 10    #pagination doesn't work on DetailView

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
    """ view to display a map of a customer address
        Relies on lat long from the Google autocomplete widget.
    """

    model = Customer
    template_name = 'customer_map.html'
    group_required = [
        u"office_staff",
        u"office_admin",
        u"super_admin",
        u"franchise_admin"]
