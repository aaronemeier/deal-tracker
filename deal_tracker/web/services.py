import logging

from .models import Wish, PriceLog, Shop, Item, UserPreference, ShopPreference

LOG = logging.getLogger(__name__)


def get_items_for_user(user):
    items = []
    wishes = Wish.objects.filter(user=user)
    if wishes.count() <= 0:
        return None

    for wish in wishes:
        item = wish.item
        try:
            price_log = PriceLog.objects.filter(item=item).latest("datetime")
            price = price_log.price
        except PriceLog.DoesNotExist:
            price = None
        shop = Shop.objects.get(id=item.shop.id)
        items.append(
            {
                "id": wish.id,
                "name": item.name,
                "price": price,
                "description": item.description,
                "shop": shop.name,
                "url": item.url,
                "currency": shop.currency,
                "image_url": item.image_url,
            }
        )
    return items


def get_wish_info(user, wish_id):
    try:
        wish = Wish.objects.get(id=wish_id, user=user)
        item = Item.objects.get(id=wish.item.id)
        shop = Shop.objects.get(id=item.shop.id)
        try:
            preference = ShopPreference.objects.get(shop=shop, user=user)
        except ShopPreference.DoesNotExist:
            preference = None
        return {"wish": wish, "item": item, "shop": shop, "preference": preference}
    except (Wish.DoesNotExist, Item.DoesNotExist, Shop.DoesNotExist):
        return None


def get_price_log_infos(item_id):
    data = {
        "price_log_dates": [],
        "price_log_prices": [],
        "price_highest": None,
        "price_lowest": None,
        "price_average": None,
        "price_latest": None,
        "stock": None,
    }

    try:
        price_log = PriceLog.objects.all().filter(item=item_id)
        prices = [log.price for log in price_log]
        data.update(
            {
                "price_highest": max(prices),
                "price_lowest": max(prices),
                "price_average": sum(prices) / len(prices),
            }
        )
        price_latest = price_log.latest("datetime")
        data.update({"price_latest": price_latest.price, "stock": price_latest.stock})

        price_log_dates = []
        price_log_prices = []
        for history in price_log.order_by("datetime"):
            price_log_dates.append(str(history.datetime.isoformat()))
            price_log_prices.append(str(history.price))

        data.update({"price_log_dates": price_log_dates, "price_log_prices": price_log_prices})
    except PriceLog.DoesNotExist:
        return None
    return data


def get_preference(user):
    data = {}
    try:
        preference = UserPreference.objects.get(user=user)
        data.update(
            {
                "language": preference.language,
                "theme": preference.theme,
                "enable_list_view": preference.enable_list_view,
            }
        )

        for preference in ShopPreference.objects.filter(user=user):
            data.update({f"shop_enabled_{preference.shop_id}": preference.enabled})
            data.update({f"shop_discount_{preference.shop_id}": float(preference.discount)})

    except UserPreference.DoesNotExist:
        return None

    return data


def get_deals(user):
    deals = []

    for shop in ShopPreference.objects.all().filter(user=user).filter(enabled=True):
        for wish in Wish.objects.all().filter(user=user).filter(item__shop=shop.shop):
            if wish.price_trigger == 0:
                break

            price = PriceLog.objects.all().filter(item=wish.item.id).latest(field_name="datetime").price
            if price is not None:
                discounted_price = round(price * (1 - shop.discount / 100), 2)
                if discounted_price <= wish.price_trigger:
                    deals.append(
                        {
                            "name": wish.item.name,
                            "url": wish.item.url,
                            "price": discounted_price,
                            "currency": shop.shop.currency,
                        }
                    )

    return deals
