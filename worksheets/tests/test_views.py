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
import datetime

 
#views test

class WorksheetMViewsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # create 2 franchises
        f1 = Franchise.objects.create(franchise='franchise_1')
        f2 = Franchise.objects.create(franchise='franchise_2')
        f3 = Franchise.objects.create(franchise='franchise_3')
        #create groups:
        Group.objects.create(name='office_admin')
        Group.objects.create(name='window_cleaner')
        #create a user:
        user1 = User.objects.create_user(
            username='testuser1',
            password='1a2b3c4d5e',
            franchise=f1
            )
        user2 = User.objects.create_user(
            username='testuser2',
            password='1a2b3c4d5e',
            franchise=f1
            )
        user3 = User.objects.create_user(
            username='testuser3',
            password='1a2b3c4d5e',
            franchise=f2
            )
        user4 = User.objects.create_user(
            username='testuser4',
            password='1a2b3c4d5e',
            franchise=f3
            )
        #add users to groups
        group = Group.objects.get(name='office_admin')
        group.user_set.add(user1)
        group = Group.objects.get(name='window_cleaner')
        group.user_set.add(user2)
        group = Group.objects.get(name='office_admin')
        group.user_set.add(user3)
        group = Group.objects.get(name='office_admin')
        group.user_set.add(user4)
        #create property_types:
        pt = Property_type.objects.create(property_type='House')
        #create some customers
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
        cust2 = Customer.objects.create(
            title="Mrs.",
            first_name='Gemma',
            last_name='Brown',
            email='gb@gb.com',
            address_line_1='2 Brown Avenue',
            city='Brown City',
            postcode='BN2 6JB',
            franchise=f2,
            frequency=4,
            property_type=pt
            )
        Customer.objects.create(
            title="Ms.",
            first_name='David',
            last_name='White',
            email='dw@dw.com',
            address_line_1='22 White Road',
            city='London',
            postcode='N2',
            franchise=f1,
            frequency=4,
            property_type=pt
            )
        due = Job_status.objects.create(job_status_description='Due')
        Jobs.objects.create(
            customer=cust1,
            scheduled_date=datetime.datetime.now(),
            allocated_date=datetime.datetime.now(),
            price=99,
            job_status=due
        )
        Jobs.objects.create(
            customer=cust1,
            scheduled_date=datetime.datetime.now(),
            allocated_date=datetime.datetime.now(),
            price=199,
            job_status=due
        )

    def test_worksheets_call_view_denies_anonymous(self):
        response = self.client.get(reverse('worksheets'))
        self.assertRedirects(response, '/login/?next=/worksheets/')
        response = self.client.get(reverse('job_add', kwargs={'customer': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/new/1/')
        response = self.client.get(reverse('job_update', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/edit/')
        response = self.client.get(reverse('job_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/delete/')
        response = self.client.get(reverse('job_check_in', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/check_in/')
        response = self.client.get(reverse('invoices'))
        self.assertRedirects(response, '/login/?next=/worksheets/invoices/')
        response = self.client.get(reverse('job_details', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/details/')
        response = self.client.get(reverse('payment'))
        self.assertRedirects(response, '/login/?next=/worksheets/payment/')
        response = self.client.get(reverse('owings'))
        self.assertRedirects(response, '/login/?next=/worksheets/owings/')
        response = self.client.get(reverse('job_paid', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/job_paid/')

    def test_worksheets_call_view_denies_for_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('worksheets'))
        self.assertRedirects(response, '/login/?next=/worksheets/')        
        response = self.client.get(reverse('job_check_in', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/check_in/')
        response = self.client.get(reverse('invoices'))
        self.assertRedirects(response, '/login/?next=/worksheets/invoices/')
        response = self.client.get(reverse('job_details', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/details/')
        response = self.client.get(reverse('payment'))
        self.assertRedirects(response, '/login/?next=/worksheets/payment/')
        response = self.client.get(reverse('owings'))
        self.assertRedirects(response, '/login/?next=/worksheets/owings/')
        response = self.client.get(reverse('job_paid', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/job_paid/')

    def test_worksheets_call_view_denies_for_window_cleaner(self):
        #TODO: test fails but still allows in browser:#####################
        response = self.client.get(reverse('job_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/delete/')
        response = self.client.get(reverse('job_add', kwargs={'customer': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/new/1/')
        response = self.client.get(reverse('job_update', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/worksheets/1/edit/')
    
    def test_job_delete_view_loads_for_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.post(reverse('job_delete', kwargs={'pk': 2}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/customers/')
        count = Jobs.objects.filter(pk=2).count()
        self.assertEqual(count, 0)

    def test_job_update_view_loads_for_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('job_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_add.html')
        
        #update a job:
        job = Jobs.objects.get(pk=1)
        customer =  Customer.objects.get(address_line_1 = getattr(job, 'customer'))
        scheduled_date =  getattr(job, 'scheduled_date')
        allocated_date = getattr(job, 'allocated_date')
        completed_date =  getattr(job, 'completed_date')
        price =  getattr(job, 'price')
        job_notes =  getattr(job, 'job_notes')
        job_status = getattr(job, 'job_status')
        payment_status = getattr(job, 'payment_status')
        window_cleaner = getattr(job, 'window_cleaner')
        if allocated_date == None:
            new_date=datetime.datetime.now() + datetime.timedelta(days=30)
        else:
            new_date=allocated_date + datetime.timedelta(days=30)
        data_valid = {
            customer: customer,
            scheduled_date: scheduled_date,
            allocated_date: new_date,
            completed_date: completed_date,
            price: price,
            job_notes: job_notes,
            job_status: job_status,
            payment_status: payment_status,
            window_cleaner: window_cleaner
        }
        response = self.client.post(reverse('job_update', kwargs={'pk': 1}), data_valid)
        allocated_date = getattr(job,'allocated_date')
        # self.assertEqual(allocated_date, new_date)
        #todo: figure out how to post from here    

    def test_job_add_view_loads_for_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('job_add', kwargs={'customer': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_add.html')
        #create a job:
        job = Jobs.objects.get(pk=1)
        customer =  getattr(job, 'customer')
        scheduled_date =  datetime.datetime.now()
        allocated_date = getattr(job, 'allocated_date')
        completed_date =  getattr(job, 'completed_date')
        price =  getattr(job, 'price')
        job_notes =  getattr(job, 'job_notes')
        job_status = getattr(job, 'job_status')
        payment_status = getattr(job, 'payment_status')
        window_cleaner = getattr(job, 'window_cleaner')
        data_valid = {
            customer: customer,
            scheduled_date: scheduled_date,
            allocated_date: allocated_date,
            completed_date: completed_date,
            price: price,
            job_notes: job_notes,
            job_status: job_status,
            payment_status: payment_status,
            window_cleaner: window_cleaner
        }
        print customer
        response = self.client.post(reverse('job_add',  kwargs={'customer': 1}), data_valid)     
        # self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/customers/1/jobs/') 
        # self.assertEqual(cust.email, 'acc@clarke.com')
        #with 'title' missing:
        # data_invalid = {
        #     customer: customer,
        #     scheduled_date: scheduled_date,
        #     allocated_date: allocated_date,
        #     completed_date: completed_date,
        #     price: price,
        #     job_notes: job_notes,
        #     job_status: job_status,
        #     payment_status: payment_status,
        #     window_cleaner: window_cleaner
        # }
        # response = self.client.post(reverse('customer_add'), data_invalid)     
        # self.assertEqual(response.status_code, 200)
        # #check no customer was created:
        # count = Customer.objects.filter(pk=6).count()
        # self.assertEqual(count, 0)

    def test_worksheet_view_loads_for_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('worksheets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'worksheet.html')
        
    def test_job_checkin_view_loads_for_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')        
        response = self.client.post(reverse('job_check_in', kwargs={'pk': 1}), {
            'payment_status': 'paid',
            'jobid': '1' 
        })
        self.assertEqual(response.status_code, 500)
        # TODO fails because stored procedure is not created
        response = self.client.get(reverse('invoices'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('invoices'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoice.html')

        response = self.client.get(reverse('job_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_details.html')
        # TODO: needs to be done in-browser
        # response = self.client.post(reverse('payment'))
        # self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('owings'))
        self.assertEqual(response.status_code, 200)
        Payment_status.objects.create(payment_status_description="paid")
        self.assertTemplateUsed(response, 'owings.html')
        response = self.client.post(reverse('job_paid', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
