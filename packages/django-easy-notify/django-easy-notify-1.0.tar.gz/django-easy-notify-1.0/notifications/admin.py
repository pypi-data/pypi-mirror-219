from django.contrib import admin

from notifications.models import Category, Notification

# Register your models here.
admin.site.register(Notification)
admin.site.register(Category)
