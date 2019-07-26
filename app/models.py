# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ImageTest(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField()


class ThumbnailTest(models.Model):
    name = models.CharField(max_length=30)
    thumbnail = models.ImageField()
