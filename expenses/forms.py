from django.forms import ModelForm
from models import Expenses
from django import forms

class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ['category', 'amount', 'date', 'notes']
        
