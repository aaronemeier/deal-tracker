from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _("Deal Tracker Administration")
admin.site.site_title = _("Deal Tracker Administration")
admin.site.index_title = f'{_("Welcome to Deal Tracker Administration")} ({settings.SITE_VERSION})'  # type: ignore

admin.site.register(models.UserPreference)
admin.site.register(models.Shop)
admin.site.register(models.Item)
admin.site.register(models.PriceLog)
admin.site.register(models.ShopPreference)
admin.site.register(models.Wish)
