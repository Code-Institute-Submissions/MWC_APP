# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse

from expenses.models import Expenses

class ExpensesList(LoginRequiredMixin, ListView):
    model = Expenses
    template_name = 'expenses_list.html'

class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expenses
    fields = ['category', 'date', 'amount', 'notes', 'user']
    template_name = 'expenses_add.html'
    success_url = "/expenses"  
    # def form_invalid(self, form):
    #     return JsonResponse(form.errors, status=400)
    def form_valid(self, form):
        return super(ExpenseCreate, self).form_valid(form)

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = ['category', 'date', 'amount', 'notes']

class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expenses
    success_url = '/'
