from django.db import migrations


class ShopData:
    name = "Brack"
    url = "https://www.brack.ch/"
    domain = "brack.ch"
    regex = r"(^https?:\/\/(?:www\.)?brack\.ch\/[a-z0-9-]+-[0-9-]+$)"
    example = "https://www.brack.ch/nintendo-switch-rot-blau-955290"
    currency = "CHF"


def add(apps, _):
    shop_model = apps.get_model("web", "Shop")
    try:
        shop = shop_model.objects.get(domain=ShopData.domain)
        shop.name = ShopData.name
        shop.url = ShopData.url
        shop.domain = ShopData.domain
        shop.regex = ShopData.regex
        shop.example = ShopData.example
        shop.currency = ShopData.currency
        shop.save()
    except shop_model.DoesNotExist:
        shop_model.objects.create(
            name=ShopData.name,
            url=ShopData.url,
            domain=ShopData.domain,
            regex=ShopData.regex,
            example=ShopData.example,
            currency=ShopData.currency,
        )


def remove(apps, _):
    shop_model = apps.get_model("web", "Shop")
    shop_model.objects.get(domain=ShopData.domain).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("web", "1000_shop_digitec"),
    ]

    operations = [
        migrations.RunPython(add, remove),
    ]
