
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False)
    language_choices = ('de', 'en')
    language_choices = (('de', _('German')), ('en', _('English')))
    language = models.CharField(max_length=2, default="de", choices=language_choices)


class Settings(models.Model):
    force_ssl = models.BooleanField(default=False)
    welcome_message = models.CharField(max_length=250)
    telnet = models.BooleanField(default=False)

class Wishlist(models.Model):
    item = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    limit = models.DecimalField

    def __str__(self):
        return self.id

class Shop(models.Model):
    name = models.CharField(max_length=64)
    shipping_costs = models.DecimalField
    discount = models.DecimalField
    url = models.URLField

    # TODO: Use List
    items = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=64)
    name_from = models.ForeignKey(Shop, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    price = models.DecimalField
    image = models.URLField
    last_updated = models.DateTimeField()
    # Absolute path to product item
    path = models.TextField(max_length=1024)

    def __str__(self):
        return self.name
