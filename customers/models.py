# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from franchises.models import Franchise

class Property_type(models.Model):
    property_type = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return self.property_type

TITLE_CHOICES = (
    ('Mr', 'Mr'),
    ('Ms', 'Ms'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Dr', 'Dr')
)

FREQUENCY_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8),
        (12, 12),
        (16, 16),
        (20, 20),
        (24, 24),
        (26, 26),
        (52, 52)
    )
    
class Customer(models.Model):
    title = models.CharField(max_length=4, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # phone_regex = RegexValidator(regex=r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(max_length=16, blank=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    address_line_3 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=False)
    customer_notes = models.TextField(blank=True, null=True)
    property_type = models.ForeignKey(
        Property_type, blank=False, null=False, on_delete=models.PROTECT
    )
    franchise = models.ForeignKey(
        Franchise, null=False, blank=False, on_delete=models.PROTECT
    )
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES, null=False)
    url = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    #don't forget to add new fields to views
    def __str__(self):
        return self.address_line_1
