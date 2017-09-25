from django.core.management.base import BaseCommand

# import your models here, e.g.
from worksheets.models import Jobs

class Command(BaseCommand):
    args = ''
    help = 'Some documentation'

    def handle(self, *args, **options):

        # your code here
        num_jobs = Jobs.objects.all().count()
        print "There are %s photo records" % num_jobs