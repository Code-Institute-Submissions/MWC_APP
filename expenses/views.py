# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Expenses
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

class ExpensesList(LoginRequiredMixin, ListView):
    model = Expenses
    template_name = 'expenses_list.html'

class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expenses
    fields = ['category', 'date', 'amount', 'notes', 'user']
    template_name = 'expenses_add.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExpenseCreate, self).form_valid(form)

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = ['category', 'date', 'amount', 'notes']

class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expenses
    success_url = '/'
