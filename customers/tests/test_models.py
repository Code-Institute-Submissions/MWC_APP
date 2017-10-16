# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from franchises.models import Franchise
from customers.models import Customer, PropertyType
from accounts.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import Client

# models test


class CustomerModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # create a franchise
        f1 = Franchise.objects.create(franchise='franchise_1')
        # create a property_type:
        pt = PropertyType.objects.create(property_type='House')
        return Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Brown',
            email='jb@jb.com',
            address_line_1='1 Brown Avenue',
            city='Brown City',
            postcode='BN1 6JB',
            franchise=f1,
            frequency=4,
            property_type=pt)

    def test_customer_get_absolute_url(self):
        customer = Customer.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(customer.get_absolute_url(), '/customers/1/jobs/')

    def test_customer_get_address(self):
        customer = Customer.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(customer.__str__(), customer.address_line_1)
