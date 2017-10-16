# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import Expense
from braces.views import GroupRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class ExpensesList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """ returns a list of expenses for current user (window cleaners only) """
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expenses_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user)
        return queryset
    group_required = u"window_cleaner"


class ExpenseCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    """ creates new expense """
    model = Expense
    fields = ['category', 'date', 'amount', 'notes']
    template_name = 'expenses_add.html'
    success_url = "/expenses/"

    # for debugging:
    # def form_invalid(self, form):
    #     return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExpenseCreate, self).form_valid(form)

    def get_initial(self):
        # https://djangosnippets.org/snippets/2987/
        initials = super(ExpenseCreate, self).get_initial()
        initials['user'] = self.request.user
        return initials
    group_required = u"window_cleaner"


class ExpenseUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    """ modify existing expense record """
    model = Expense
    fields = ['category', 'date', 'amount', 'notes']
    template_name = 'expenses_add.html'
    success_url = "/expenses/"

    def form_valid(self, form):
        return super(ExpenseUpdate, self).form_valid(form)

    # for debugging:
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    group_required = u"window_cleaner"


class ExpenseDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    """ delete existing expense record """
    model = Expense
    success_url = "/expenses/"
    group_required = u"window_cleaner"
