from django.forms import ModelForm
from models import Expenses

class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ['category', 'user', 'amount', 'date', 'notes']
