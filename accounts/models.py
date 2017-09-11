# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
