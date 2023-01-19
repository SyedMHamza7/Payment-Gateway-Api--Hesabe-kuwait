# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import TextInput, Textarea
from django.contrib import admin
from .models import Credential
from django.db import models
# Register your models here.




class CredentialAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
        
    }

admin.site.register(Credential,CredentialAdmin)
