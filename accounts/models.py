# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from franchises .models import Franchise


class User(AbstractUser):
    franchise = models.ForeignKey(
        Franchise, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.get_full_name()
