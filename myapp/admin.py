# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from myapp import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=('nickname','message','enable','pub_time')
    
    orderinf=('-pub_time',)

admin.site.register(models.Mood)
admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Post,PostAdmin)

