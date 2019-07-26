# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from app import models

# Register your models here.
admin.site.register(models.ImageTest)
admin.site.register(models.ThumbnailTest)
