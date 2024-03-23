from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from regex_field.fields import RegexField


class UserPreference(models.Model):
    language: str  # type: ignore
    language_choices = (("en", _("English")), ("de", _("German")))
    language = models.CharField(max_length=2, default="en", choices=language_choices)  # type: ignore
    theme_choices = (
        ("LIGHT", _("Light")),
        ("DARK", _("Dark")),
    )
    theme = models.CharField(max_length=10, default="LIGHT", choices=theme_choices)
    enable_list_view = models.BooleanField(blank=True, default=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")

    class Meta:
        db_table = "user_preference"
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")

    def __str__(self):
        return f"{self.user}, {self.language}, {self.theme}"


class Shop(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=1000, unique=True)
    domain = models.URLField(max_length=200, unique=True)
    regex = RegexField(max_length=200, unique=True)
    example = models.URLField(max_length=1000)
    currency_choices = (
        ("CHF", _("Swiss francs")),
        ("USD", _("US Dollars")),
    )
    currency = models.CharField(max_length=10, default="CHF", choices=currency_choices)

    class Meta:
        db_table = "shop"
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f"{self.name}, {self.url}"


class Item(models.Model):
    url = models.URLField(max_length=1000, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000, blank=True)
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    brand = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "item"
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return self.url

    def update_from_scraper(self, data):
        self.name = data.name[:200]
        self.brand = data.brand[:50]
        self.image_url = data.image_url[:1000]
        self.description = data.description[:1000]
        self.save()


class PriceLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=30, blank=True)
    stock = models.IntegerField(blank=True, default=None, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "price_log"
        verbose_name = _("Price Log")
        verbose_name_plural = _("Price Logs")

    def __str__(self):
        return f"{self.item.name}, {self.price}, {self.datetime}"


class ShopPreference(models.Model):
    enabled = models.BooleanField(default=True)
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=4, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        db_table = "shop_preference"
        verbose_name = _("Shop Preference")
        verbose_name_plural = _("Shop Preferences")
        unique_together = ["user", "shop"]

    def __str__(self):
        return f"{self.shop}, {self.user}, {self.enabled}, {self.discount}"


class Wish(models.Model):
    price_trigger = models.DecimalField(default=0, decimal_places=2, max_digits=30)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = "wish"
        verbose_name = _("Wish")
        verbose_name_plural = _("Wishes")
        unique_together = ["item", "user"]

    def __str__(self):
        return f"{self.item}, {self.user}, {self.price_trigger}"
