# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from myapp import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=('nickname','message','enable','pub_time')

    ordering=('-pub_time',)

class PollItemAdmin(admin.ModelAdmin):
    list_display=('poll','name','vote','image_url')
    ordering=('poll',)

class PollAdmin(admin.ModelAdmin):
    list_display=('name','create_at','enable')
    ordering=('-create_at',)

admin.site.register(models.Mood)
admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Poll,PollAdmin)
admin.site.register(models.PollItem,PollItemAdmin)

