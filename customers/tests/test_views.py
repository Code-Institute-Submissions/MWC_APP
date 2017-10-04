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

 
#views test

class CustomerViewsTest(TestCase):
    
    @classmethod
    def setUpTestData(self):
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
        Customer.objects.create(
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
        Customer.objects.create(
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

    #https://stackoverflow.com/questions/11885211/how-to-write-a-unit-test-for-a-django-view

    def test_customerviews_call_view_denies_anonymous(self):
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')
        response = self.client.get(reverse('customer_add'))
        self.assertRedirects(response, '/login/?next=/customers/new/')
        response = self.client.get(reverse('customer_update', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/')
        response = self.client.get(reverse('customer_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/delete/')
        response = self.client.get(reverse('customer_job_list', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/jobs/')
        response = self.client.get(reverse('customer_map', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/map/')


    def test_customerslist_call_view_denies_for_window_cleaner(self):
        #for franchise 1 user:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')
        #for franchise 2 user:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')

    def test_customerslist_call_view_loads_for_office_admin(self):
        #for franchise 1 user:
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        #should return 1 customer only:
        self.assertTrue( len(response.context['customers']) == 2)
        self.assertContains(response, '1 Brown Avenue')
        self.assertContains(response, '22 White Road')
        #for franchise 2 user:
        self.client.login(username='testuser3', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        #should return 1 customer only:
        self.assertTrue( len(response.context['customers']) == 1)
        self.assertContains(response, '2 Brown Avenue')
        #for franchise 3 user:
        self.client.login(username='testuser4', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        #should return 0 customers:
        self.assertTrue( len(response.context['customers']) == 0)
        
    def test_customerslist_call_POST_requests(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e') #franchise f1
        #POST request with empty arguments:
        response = self.client.post(reverse('customers'), {}) 
        # should return all records:
        self.assertTrue( len(response.context['customers']) == 2)
        #POST request with empty search field, no 'action':
        response = self.client.post(reverse('customers'), {'input_search': ''}) 
        # should return all records:
        self.assertTrue( len(response.context['customers']) == 2)
        #POST request with empty 'action', valid filter:
        response = self.client.post(reverse('customers'), {'action': '', 'input_search': '2 Brown Avenue'}) 
        # should return all records (filter would otherwise return 1 record):
        self.assertTrue( len(response.context['customers']) == 2)
        #POST request with invalid 'action', valid search value:
        response = self.client.post(reverse('customers'), {'action': 'random_value', 'input_search': '2 Brown Avenue'}) 
        # should return all records:
        self.assertTrue( len(response.context['customers']) == 2)
        #POST request with valid 'action', empty search field
        response = self.client.post(reverse('customers'), {'action': 'filter', 'input_search': ''}) 
        # should return all records:
        self.assertTrue( len(response.context['customers']) == 2) 
        #POST request with valid 'action', valid search field
        response = self.client.post(reverse('customers'), {'action': 'filter', 'input_search': 'Brown Avenue'}) 
        # should return 1 record (1 is filtered by franchise):
        self.assertTrue( len(response.context['customers']) == 1) 
    
    def test_customer_create_get_tests(self):
        #no logged in user:
        response = self.client.get(reverse('customer_add')) 
        self.assertRedirects(response, '/login/?next=/customers/new/')
        #user logged in, window_cleaner:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('customer_add')) 
        self.assertRedirects(response, '/login/?next=/customers/new/')
        #user logged in, office_admin:
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('customer_add')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_add.html')
    
    def test_customer_create_post_tests(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        #empty form: reloads page
        response = self.client.post(reverse('customer_add'), {}) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_add.html')
        #valid/required data:
        data_valid = {
            'title': 'Mr',
            'first_name': 'Arthur C.',
            'last_name': 'Clarke',
            'email': 'acc@clarke.com',
            'address_line_1': '23 Clarke Avenue',
            'city': 'London',
            'postcode': 'NW3',
            'property_type': "2",
            'frequency': '4',
            'franchise': "2"
        }
        response = self.client.post(reverse('customer_add'), data_valid)     
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customers/5/jobs/') #we've already added 4 customers
        cust = Customer.objects.get(pk=5)
        self.assertEqual(cust.email, 'acc@clarke.com')
        #with 'title' missing:
        data_invalid = {
            'first_name': 'Arthur C.',
            'last_name': 'Clarke',
            'email': 'acc@clarke.com',
            'address_line_1': '23 Clarke Avenue',
            'city': 'London',
            'postcode': 'NW3',
            'property_type': "2",
            'frequency': '4',
            'franchise': "2"
        }
        response = self.client.post(reverse('customer_add'), data_invalid)     
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_add.html')
        # self.assertRaises(TypeError, Customer.objects.get(pk=6))

        #check initial values:
        response = self.client.get(reverse('customer_add'), data_valid) 
        self.assertEquals(response.context['form']['franchise'].value(), 2)
        self.assertEquals(response.context['form']['frequency'].value(), '4')




