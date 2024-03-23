from django.db import migrations


class ShopData:
    name = "Digitec"
    url = "https://www.digitec.ch/"
    domain = "digitec.ch"
    regex = r"(^https?:\/\/(?:www\.)?digitec\.ch\/(?:[a-z0-9]{1,10}\/){0,3}product\/[a-z0-9-]{1,}$)"
    example = (
        "https://www.digitec.ch/en/s1/product/nintendo-switch-neon-red-neon-blue-de-fr-it-en-game-consoles-11586094"
    )
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
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add, remove),
    ]
