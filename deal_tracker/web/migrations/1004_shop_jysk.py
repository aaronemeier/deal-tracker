from django.db import migrations


class ShopData:
    name = "Jysk"
    url = "https://www.jysk.ch/"
    domain = "jysk.ch"
    regex = r"(^https?:\/\/(www\.)?jysk\.ch\/(?:[a-zA-Z0-9-]+\/?){1,10}$)"
    example = "https://www.jysk.ch/de/schlafzimmer/boxspringbetten/gold/boxspringbett-140x200-sembella-c400"
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
        ("web", "1003_shop_zalando"),
    ]

    operations = [
        migrations.RunPython(add, remove),
    ]
