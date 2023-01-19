# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class Credential(TimeStampedModel):
	status_list = ((True,"Enable"),(False,"Disable"))
	merchant_code = models.IntegerField(max_length=45,verbose_name="Merchant Code")
	working_key = models.CharField(max_length=455,verbose_name="Secret Key")
	iv = models.CharField(max_length=455,verbose_name="IV Key")
	accesscode = models.CharField(max_length=255,verbose_name="Access Code",default="0")
	payment_url = models.CharField(max_length=255,verbose_name="Payment URL")
	success_url = models.CharField(max_length=255, verbose_name="Success URL")
	failure_url = models.CharField(max_length=255, verbose_name="Failure URL")
	knet = models.BooleanField(
        max_length=50, choices=status_list, verbose_name="KNET Staus", default="Enable")
	mpgs = models.BooleanField(
        max_length=50, choices=status_list, verbose_name="MPGS Staus", default="Disable")

