# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Property_type(models.Model):
    property_type = models.CharField(max_length=255, blank=False)

class Customer(models.Model):
    title = models.CharField(max_length=4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # phone_regex = RegexValidator(regex=r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(max_length=16, blank=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    address_line_3 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    customer_notes = models.TextField(blank=True)
    property_type = models.ForeignKey(Property_type, blank=True)
