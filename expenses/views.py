# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Expenses

class ExpensesList(ListView):
    model = Expenses
    template_name = 'expenses_list.html'

class ExpenseCreate(CreateView):
    model = Expenses
    fields = ['category', 'user', 'date', 'amount', 'notes']

class ExpenseUpdate(UpdateView):
    model = Expenses
    fields = ['category', 'user', 'date', 'amount', 'notes']

class ExpenseDelete(DeleteView):
    model = Expenses
    success_url = '/'
