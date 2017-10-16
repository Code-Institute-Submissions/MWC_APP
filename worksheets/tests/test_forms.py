import unittest
from django.test import TestCase
from django.contrib.auth.models import Group
from accounts.models import User
from customers.models import Customer, PropertyType
from worksheets.models import Job, JobStatus, PaymentStatus
from worksheets.forms import JobUpdateForm
from django_dynamic_fixture import G
from franchises.models import Franchise
import datetime


class TestJobUpdateForm(TestCase):

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
        cls.user3 = User.objects.create_user(
            username='testuser3',
            password='1a2b3c4d5e',
            franchise=cls.f2
        )
        cls.user4 = User.objects.create_user(
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
        cls.pt = PropertyType.objects.create(property_type='House')
        # create some customers
        cls.cust1 = Customer.objects.create(
            title="Mr.",
            first_name='John',
            last_name='Brown',
            email='jb@jb.com',
            address_line_1='1 Brown Avenue',
            city='Brown City',
            postcode='BN1 6JB',
            franchise=cls.f1,
            frequency=4,
            property_type=cls.pt
        )
        cls.cust2 = Customer.objects.create(
            title="Mrs.",
            first_name='Gemma',
            last_name='Brown',
            email='gb@gb.com',
            address_line_1='2 Brown Avenue',
            city='Brown City',
            postcode='BN2 6JB',
            franchise=cls.f2,
            frequency=4,
            property_type=cls.pt
        )
        cls.cust3 = Customer.objects.create(
            title="Ms.",
            first_name='David',
            last_name='White',
            email='dw@dw.com',
            address_line_1='22 White Road',
            city='London',
            postcode='N2',
            franchise=cls.f1,
            frequency=4,
            property_type=cls.pt
        )
        cls.due = JobStatus.objects.create(
            job_status_description='Due'
        )
        cls.compl = JobStatus.objects.create(
            job_status_description='Completed'
        )
        cls.booked = JobStatus.objects.create(
            job_status_description='Booked'
        )
        cls.owed = PaymentStatus.objects.create(
            payment_status_description='Owed'
        )
        cls.paid = PaymentStatus.objects.create(
            payment_status_description='Paid'
        )
        cls.job1 = Job.objects.create(
            customer=cls.cust1,
            scheduled_date=datetime.datetime.strftime(
                datetime.datetime.now(),
                '%Y-%m-%d'),
            allocated_date=datetime.datetime.strftime(
                datetime.datetime.now(),
                '%Y-%m-%d'),
            price=99,
            job_status=cls.due)
        cls.job2 = Job.objects.create(
            customer=cls.cust1,
            scheduled_date=datetime.datetime.strftime(
                datetime.datetime.now(),
                '%Y-%m-%d'),
            allocated_date=datetime.datetime.strftime(
                datetime.datetime.now(),
                '%Y-%m-%d'),
            price=199,
            job_status=cls.due)

    def test_form_is_valid(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'price': 45,
            'job_status': self.due.id,
        }
        form = JobUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_with_missing_required_field(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            # 'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            # 'job_notes': None,
            'job_status': self.compl.id,
            # 'payment_status': self.owed.id,
            # 'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_with_completed_date_no_alloc(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            # 'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.compl.id,
            'payment_status': self.owed.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Please enter an allocated date'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_due_paid(self):
        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.due.id,
            'payment_status': self.paid.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Job has &#39;Due&#39; status but is set as paid'
                        ' - please correct'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_completed_date_no_payment(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.compl.id,
            # 'payment_status': self.owed.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Please enter a payment status'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_completed_date_no_wc(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.compl.id,
            'payment_status': self.owed.id,
            # 'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Please enter a window cleaner'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_completed_date_due_status(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.due.id,
            'payment_status': self.owed.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        # print form.errors['__all__']
        self.assertTrue('Job has a completed date but not a '
                        '&#39;completed&#39; job status - please correct'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_due_status_and_paid(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.due.id,
            'payment_status': self.owed.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        # print form.errors['__all__']

        self.assertTrue('Job has a completed date but not a '
                        '&#39;completed&#39; job status - please correct'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_booked_status_and_paid(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.booked.id,
            'payment_status': self.paid.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Job has &#39;Booked&#39; '
                        'status but is set as paid - please correct'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_without_scheduled_date(self):

        form_data = {
            'customer': self.cust1.id,
            # 'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.compl.id,
            'payment_status': self.paid.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Please enter a due date'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_booked_no_alloc_wc(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            # 'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.booked.id,
            # 'payment_status': self.paid.id,
            # 'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Job is booked - please enter a window cleaner'
                        ' and an allocated date'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_booked_no_alloc(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            # 'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.booked.id,
            # 'payment_status': self.paid.id,
            'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Job is booked - please enter an allocated date'
                        in str(form.errors['__all__']))

    def test_form_is_not_valid_with_booked_no_wc(self):

        form_data = {
            'customer': self.cust1.id,
            'scheduled_date': '2017-10-01',
            'allocated_date': '2017-10-01',
            # 'completed_date': '2017-10-01',
            'price': 45,
            'job_status': self.booked.id,
            # 'payment_status': self.paid.id,
            # 'window_cleaner': self.user2.id
        }
        form = JobUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('Job is booked - please enter a window cleaner'
                        in str(form.errors['__all__']))
