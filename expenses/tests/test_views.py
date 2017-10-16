# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import Max
from franchises.models import Franchise
from django.contrib.auth.models import Group
from accounts.models import User
from expenses.models import Expense, ExpenseCategory


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

        # add an expense:
        cls.cat1 = ExpenseCategory.objects.create(category='Fuel')
        cls.exp1 = Expense.objects.create(category=cls.cat1, user=cls.user2,
                                          amount=99, date='2017-10-09')

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

    def test_expenses_create_call_view_allows_window_cleaner_valid_data(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        # valid/required data:
        data_valid = {
            'category': self.cat1.id,
            'user': self.user2.id,
            'amount': 99,
            'date': '2017-10-16'
        }
        max_id_dic = Expense.objects.all().aggregate(Max('id'))
        max_id_before = max_id_dic['id__max']
        response = self.client.post(reverse('expenses_add'), data_valid)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/expenses/')
        max_id_dic = Expense.objects.all().aggregate(Max('id'))
        max_id_after = max_id_dic['id__max']

        self.assertEqual(max_id_before + 1, max_id_after)

    def test_expenses_create_call_view_denies_w_c_invalid_data(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        # valid/required data:
        data_valid = {
            # 'category': self.cat1.id,
            'user': self.user2.id,
            'amount': 99,
            'date': '2017-10-16'
        }
        max_id_dic = Expense.objects.all().aggregate(Max('id'))
        max_id_before = max_id_dic['id__max']
        response = self.client.post(reverse('expenses_add'), data_valid)
        self.assertEqual(response.status_code, 200)
        max_id_dic = Expense.objects.all().aggregate(Max('id'))
        max_id_after = max_id_dic['id__max']

        self.assertEqual(max_id_before, max_id_after)

    def test_expenses_update_allows_wc_invalid_data(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        # valid/required data:
        data_invalid = {
            # 'category': self.cat1.id,
            'user': self.user2.id,
            'amount': 99,
            'date': '2017-10-16'
        }
        response = self.client.post(reverse('expenses_update',
                                            kwargs={'pk': self.exp1.id}),
                                    data_invalid)
        self.assertEqual(response.status_code, 400)

    def test_expenses_update_allows_wc_valid_data(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        # valid/required data:
        data_invalid = {
            'category': self.cat1.id,
            'user': self.user2.id,
            'amount': 99,
            'date': '2017-10-16'
        }
        response = self.client.post(reverse('expenses_update',
                                            kwargs={'pk': self.exp1.id}),
                                    data_invalid)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/expenses/')

    def test_expenses_delete_window_cleaner(self):
        self.client.login(username='testuser2', password='1a2b3c4d5e')
        response = self.client.post(reverse('expenses_delete',
                                            kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/expenses/')
