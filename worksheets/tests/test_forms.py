import unittest
from worksheets.forms import JobUpdateForm
from worksheets.models import Jobs
from django_dynamic_fixture import G

class TestJobUpdateForm(unittest.TestCase):
    def test_validation(self):
        job = G(Jobs)
        print job.customer
        form_data = {
            # 'customer': 'John Brown', 
            'scheduled_date': '2017-10-01', 
            'allocated_date': '2017-10-01', 
            'completed_date': '2017-10-01', 
            'price': 45, 
            'job_notes': None, 
            # 'job_status': 'Due', 
            'payment_status': None, 
            'window_cleaner':None
        }
        print job.id
        form = JobUpdateForm(data=form_data)
        # self.assertTrue(form.is_valid())
        self.assertEqual(job.id, 3)