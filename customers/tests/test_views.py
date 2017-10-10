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
from worksheets.models import Jobs, Job_status
import datetime
from django_dynamic_fixture import G
#http://django-dynamic-fixture.readthedocs.io/en/latest/overview.html

# views test

class CustomerViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create 2 franchises
        cls.f1 = G(Franchise)
        cls.f2 = G(Franchise)
        cls.f3 = G(Franchise)
        # create groups:
        Group.objects.create(name='office_admin')
        Group.objects.create(name='window_cleaner')
        # create a user:
        cls.user1 = G(User,
            username='testuser1',
            password='1a2b3c4d5e',
            franchise=cls.f1
        )
        cls.user2 = G(User,
            username='testuser2',
            password='1a2b3c4d5e',
            franchise=cls.f1
        )
        cls.user3 =G(User,
            username='testuser3',
            password='1a2b3c4d5e',
            franchise=cls.f2
        )
        cls.user4 =G(User,
            username='testuser4',
            password='1a2b3c4d5e',
            franchise=cls.f3
        )
        # add users to groups
        group = Group.objects.get(name='office_admin')
        group.user_set.add(cls.user1)
        group = Group.objects.get(name='window_cleaner')
        group.user_set.add(cls.user2)
        group = Group.objects.get(name='office_admin')
        group.user_set.add(cls.user3)
        group = Group.objects.get(name='office_admin')
        group.user_set.add(cls.user4)
        # create property_types:
        pt = Property_type.objects.create(property_type='House')
        # create some customers
        cls.cust1 = G(Customer, Franchise=cls.f1)
        cls.cust2 = G(Customer, Franchise=cls.f2)
        cls.cust3 =  G(Customer, Franchise=cls.f3)
    # https://stackoverflow.com/questions/11885211/how-to-write-a-unit-test-for-a-django-view

    def test_customers_call_view_denies_anonymous(self):
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')
    def test_customer_add_call_view_denies_anonymous(self):
        response = self.client.get(reverse('customer_add'))
        self.assertRedirects(response, '/login/?next=/customers/new/')
    def test_customer_update_call_view_denies_anonymous(self):
        response = self.client.get(
            reverse('customer_update', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/')
    def test_customer_delete_call_view_denies_anonymous(self):
        response = self.client.get(
            reverse('customer_delete', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/delete/')
    def test_customer_job_list_call_view_denies_anonymous(self):
        response = self.client.get(
            reverse('customer_job_list', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/jobs/')
    def test_customer_map_call_view_denies_anonymous(self):
        response = self.client.get(reverse('customer_map', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/customers/1/map/')

    def test_customers_call_view_denies_for_window_cleaner_franchise_1(self):
        # for franchise 1 user:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')
    def test_customerslist_call_view_denies_for_window_cleaner_franchise_2(self):
        # for franchise 2 user:
        self.client.login(username='testuser3', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertRedirects(response, '/login/?next=/customers/')

    def test_customerslist_call_view_loads_for_office_admin_franchise_1(self):
        # for franchise 1 user:
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'), follow=True)
        print response.content
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        # should return 1 customer only:
        self.assertTrue(len(response.context['customers']) == 2)
        self.assertContains(response, '1 Brown Avenue')
        self.assertContains(response, '22 White Road')
    def test_customerslist_call_view_loads_for_office_admin_franchise_2(self):
        # for franchise 2 user:
        self.client.login(username='testuser3', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        # should return 1 customer only:
        self.assertTrue(len(response.context['customers']) == 1)
        self.assertContains(response, '2 Brown Avenue')
    def test_customerslist_call_view_loads_for_office_admin_franchise_3(self):
        # for franchise 3 user:
        self.client.login(username='testuser4', password='1a2b3c4d5e')
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_list.html')
        # should return 0 customers:
        self.assertTrue(len(response.context['customers']) == 0)

    def test_customerslist_call_POST_request_empty_arguments(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1
        # POST request with empty arguments:
        response = self.client.post(reverse('customers'), {})
        # should return all records:
        self.assertTrue(len(response.context['customers']) == 2)
    def test_customerslist_call_POST_request_no_action(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1    
        # POST request with empty search field, no 'action':
        response = self.client.post(reverse('customers'), {'input_search': ''})
        # should return all records:
        self.assertTrue(len(response.context['customers']) == 2)
    def test_customerslist_call_POST_requests_no_action_valid_filter(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1
        # POST request with empty 'action', valid filter:
        response = self.client.post(reverse('customers'), {
                                    'action': '', 'input_search': '2 Brown Avenue'})
        # should return all records (filter would otherwise return 1 record):
        self.assertTrue(len(response.context['customers']) == 2)
    def test_customerslist_call_POST_requests_invalid_action_valid_search(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1
        # POST request with invalid 'action', valid search value:
        response = self.client.post(reverse('customers'), {
                                    'action': 'random_value', 'input_search': '2 Brown Avenue'})
        # should return all records:
        self.assertTrue(len(response.context['customers']) == 2)
    def test_customerslist_call_POST_requests_valid_action_empty_search(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1
        # POST request with valid 'action', empty search field
        response = self.client.post(reverse('customers'), {
                                    'action': 'filter', 'input_search': ''})
        # should return all records:
        self.assertTrue(len(response.context['customers']) == 2)
    def test_customerslist_call_POST_requests_valid_action_valid_search(self):
        self.client.login(username='testuser1',
                          password='1a2b3c4d5e')  # franchise f1
        # POST request with valid 'action', valid search field
        response = self.client.post(reverse('customers'), {
                                    'action': 'filter', 'input_search': 'Brown Avenue'})
        # should return 1 record (1 is filtered by franchise):
        self.assertTrue(len(response.context['customers']) == 1)

    def test_customer_create_get_tests(self):
        # no logged in user:
        response = self.client.get(reverse('customer_add'))
        self.assertRedirects(response, '/login/?next=/customers/new/')
        # user logged in, window_cleaner:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('customer_add'))
        self.assertRedirects(response, '/login/?next=/customers/new/')
        # user logged in, office_admin:
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('customer_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_add.html')

    # todo: customer update tests

    def test_customer_create_post_tests(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        # empty form: reloads page
        response = self.client.post(reverse('customer_add'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_add.html')
    def test_customer_create_post_tests_valid_data(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        # valid/required data:
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
        # we've already added 4 customers
        self.assertRedirects(response, '/customers/5/jobs/')
        cust = Customer.objects.get(pk=5)
        self.assertEqual(cust.email, 'acc@clarke.com')

    def test_customer_create_post_tests_invalid_data(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        # with 'title' missing:
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
        # check no customer was created:
        count = Customer.objects.filter(pk=6).count()
        self.assertEqual(count, 0)

        # check initial values:
    def test_customer_create_post_tests_initial_values(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
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
            'franchise': self.f1.id
        }
        
        response = self.client.get(reverse('customer_add'), data_valid)
        print 'response:' , response.content 
        # self.assertEqual(response.status_code, 200)
        
        # print 'franchise: ', response.context #['form']['franchise'] #.value()
        # self.assertEquals(response.context['form'].initial['franchise'], 2)
        # self.assertEquals(response.context['form']['frequency'].value(), '4')

    def test_customer_delete_tests(self):
        f1 = Franchise.objects.get(franchise='franchise_1')
        pt = Property_type.objects.create(property_type='House')
        cust = Customer.objects.create(
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
        custid = cust.id
        # no logged in user:
        response = self.client.post(
            reverse('customer_delete', kwargs={'pk': custid}))
        url = '/login/?next=/customers/%s/delete/' % custid
        self.assertRedirects(response, url)
    def test_customer_create_post_tests_window_cleaner(self):
        f1 = Franchise.objects.get(franchise='franchise_1')
        pt = Property_type.objects.create(property_type='House')
        cust = Customer.objects.create(
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
        custid = cust.id
        # #user logged in, window_cleaner:
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.post(
            reverse('customer_delete', kwargs={'pk': custid}))
        self.assertRedirects(response, url)

    def test_customer_create_post_tests_office_admin(self):
        f1 = Franchise.objects.get(franchise='franchise_1')
        pt = Property_type.objects.create(property_type='House')
        cust = Customer.objects.create(
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
        custid = cust.id
        # user logged in, office_admin:    
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.post(
            reverse('customer_delete', kwargs={'pk': custid}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customers/')
        count = Customer.objects.filter(pk=custid).count()
        self.assertEqual(count, 0)

    def test_customer_job_list_view(self):
        # f1 = Franchise.objects.get(franchise='franchise_1')
        # f2 = Franchise.objects.get(franchise='franchise_2')
        pt = Property_type.objects.create(property_type='House')
        cust1 = Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Pink',
            email='jb@jb.com',
            address_line_1='1 Pink Avenue',
            city='Pink City',
            postcode='N1 6PP',
            franchise=f1,
            frequency=4,
            property_type=pt
        )
        cust2 = Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Red',
            email='jb@jb.com',
            address_line_1='1 Red Avenue',
            city='Red City',
            postcode='N1 6PP',
            franchise=f1,
            frequency=4,
            property_type=pt
        )
        cust3 = Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Black',
            email='jb@jb.com',
            address_line_1='1 Black Avenue',
            city='Black City',
            postcode='BK 6PP',
            franchise=f2,
            frequency=4,
            property_type=pt
        )
        cust1id = cust1.id
        cust2id = cust2.id
        cust3id = cust3.id
        # create some jobs:
        due = Job_status.objects.create(job_status_description='Due')
        Jobs.objects.create(
            customer=cust1,
            scheduled_date=datetime.datetime.now(),
            allocated_date=datetime.datetime.now(),
            price=99,
            job_status=due
        )
        # Jobs.objects.create(
        #     customer=cust1,
        #     scheduled_date=datetime.datetime.now(),
        #     allocated_date=datetime.datetime.now(),
        #     price=999,
        #     job_status=due
        # )
        # Jobs.objects.create(
        #     customer=cust2,
        #     scheduled_date=datetime.datetime.now(),
        #     allocated_date=datetime.datetime.now(),
        #     price=999,
        #     job_status=due
        # )
        # url = '/login/?next=/customers/%s/jobs/' % cust1id
        # # no logged in user:
        # response = self.client.get(
        #     reverse('customer_job_list', kwargs={'pk': cust1id}))
        # self.assertRedirects(response, url)
        # # user logged in, window_cleaner:
        # self.client.login(username='testuser2', password='1a2b3c4d5e')
        # response = self.client.get(
        #     reverse('customer_job_list', kwargs={'pk': cust1id}))
        # self.assertRedirects(response, url)
        # # user logged in, office_admin, different franchise:
        # self.client.login(username='testuser3', password='1a2b3c4d5e')
        # response = self.client.get(
        #     reverse('customer_job_list', kwargs={'pk': cust1id}))
        # self.assertEqual(response.status_code, 404)
        # response = self.client.get(
        #     reverse('customer_job_list', kwargs={'pk': cust3id}))
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'customer_job_list.html')
        # # #user logged in, office_admin, same franchise:
        # self.client.login(username='testuser1', password='1a2b3c4d5e')
        # response = self.client.get(
        #     reverse('customer_job_list', kwargs={'pk': cust1id}))
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'customer_job_list.html')
        # # should return 2 customers:
        # print response.context['object']
        # for key in response.context.keys():
        #     print key, 'corresponds to', response.context[key]
        # # print response.context['request']
        # # self.assertTrue( len(response.context['customer'][1]) == 2)
