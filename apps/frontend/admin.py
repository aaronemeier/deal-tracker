from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.Settings)
admin.site.register(models.Wishlist)
admin.site.register(models.Shop)
admin.site.register(models.Item)
