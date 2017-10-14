# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from franchises.models import Franchise
from django.contrib.auth.models import Group
from accounts.models import User





class ExpensesViewsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # create 2 franchises
        cls.f1 = Franchise.objects.create(franchise='franchise_1')
        cls.f2 = Franchise.objects.create(franchise='franchise_2')
        cls.f3 = Franchise.objects.create(franchise='franchise_3')
        # create groups:
        Group.objects.create(name='office_admin')
        Group.objects.create(name='window_cleaner')
        # create a user:
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='1a2b3c4d5e',
            franchise=cls.f1
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='1a2b3c4d5e',
            franchise=cls.f1
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
        # create property_types
    
    # Tests to check anonymous access not permitted:

    def test_expenses_list_call_view_denies_anonymous(self):
        response = self.client.get(reverse('expenses'))
        self.assertRedirects(response, '/login/?next=/expenses/')

    def test_expense_create_call_view_denies_anonymous(self):
        response = self.client.get(reverse('expenses_add'))
        self.assertRedirects(response, '/login/?next=/expenses/new/')
    
    def test_expenses_update_call_view_denies_anonymous(self):
        response = self.client.get(reverse('expenses_update', 
                                           kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/expenses/1/')

    def test_expense_delete_call_view_denies_anonymous(self):
        response = self.client.get(reverse('expenses_delete',
                                           kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/expenses/1/delete/')
    
    # Tests to check office_admin group access not permitted:

    def test_expenses_list_call_view_denies_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses'))
        self.assertRedirects(response, '/login/?next=/expenses/')

    def test_expense_create_call_view_denies_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_add'))
        self.assertRedirects(response, '/login/?next=/expenses/new/')
    
    def test_expenses_update_call_view_denies_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_update', 
                                           kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/expenses/1/')

    def test_expense_delete_call_view_denies_office_admin(self):
        self.client.login(username='testuser1', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_delete',
                                           kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/expenses/1/delete/')

# Tests to check window_cleaner group access permitted:

    def test_expenses_list_call_view_allows_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses_list.html')
    
    def test_expenses_create_call_view_allows_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_add',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses_add.html')
    
    def test_expenses_update_call_view_allows_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_update',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses_add.html')
    
    def test_expenses_delete_call_view_allows_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.get(reverse('expenses_delete',
                                           kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses.html')

    