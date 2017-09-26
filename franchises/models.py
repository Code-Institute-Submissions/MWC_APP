# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Franchise(models.Model):
    franchise = models.CharField(max_length=50)

    def __str__(self):
        return self.franchise
