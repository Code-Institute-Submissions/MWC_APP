# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models


class expense_categories(models.Model):
    category = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.category


class Expenses(models.Model):
    category = models.ForeignKey(expense_categories, null=False, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
        null=False
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    date = models.DateField(null=False)
    notes = models.TextField(null=True, blank=True)
