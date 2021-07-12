from django.contrib import admin
from . import models


@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id', 'email',]
    fields = ['email', ]


@admin.register(models.Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'to', 'subject', 'text', 'is_sent', ]

    fields = ['to', 'subject', 'text', 'is_sent', ]