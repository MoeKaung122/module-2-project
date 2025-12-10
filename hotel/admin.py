from django.contrib import admin
from hotel import models

# Register your models here.
admin.site.register(models.Hotel)
admin.site.register(models.City)
admin.site.register(models.RoomType)
admin.site.register(models.Room)
admin.site.register(models.Booking)
admin.site.register(models.Payment)
admin.site.register(models.Blog)
admin.site.register(models.Comment)
admin.site.register(models.Contact)
