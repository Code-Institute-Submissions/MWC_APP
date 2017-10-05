# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from franchises.models import Franchise
from customers.models import Customer, Property_type
from accounts.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import Client
from customers.views import CustomerCreate
from django.contrib.auth import authenticate
from worksheets.models import Jobs, Job_status, Payment_status


# views test

class WorksheetModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create 2 franchises
        f1 = Franchise.objects.create(franchise='franchise_1')
        # create groups:
        Group.objects.create(name='office_admin')
        # create a user:
        user1 = User.objects.create_user(
            username='testuser1',
            password='1a2b3c4d5e',
            franchise=f1
        )
        # add user to groups
        group = Group.objects.get(name='office_admin')
        group.user_set.add(user1)
        # create property_types:
        pt = Property_type.objects.create(property_type='House')
        # create a customer
        cust1 = Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Brown',
            email='jb@jb.com',
            address_line_1='1 Brown Avenue',
            city='Brown City',
            postcode='BN1 6JB',
            franchise=f1,
            frequency=4,
            property_type=pt
        )

    def test_job_status_name_returns_description(self):
        status = Job_status.objects.create(job_status_description='Due')
        self.assertEquals(status.__str__(), status.job_status_description)

    def test_payment_status_name_returns_description(self):
        status = Payment_status.objects.create(
            payment_status_description='Due')
        self.assertEquals(status.__str__(), status.payment_status_description)
