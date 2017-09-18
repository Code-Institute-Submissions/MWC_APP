# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from franchises.models import Franchise

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    franchise = models.ForeignKey(Franchise, null=False, blank=False, on_delete=models.PROTECT)
    def __str__(self):
            return self.get_full_name()

# dont forget to add admin.site.register(User, UserAdmin) to admin.py