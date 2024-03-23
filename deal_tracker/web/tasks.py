import random

from celery import group
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask

from deal_tracker_config import celery_app as app
from deal_tracker.scrapers.exceptions import BlockedByRemote
from deal_tracker.scrapers.scraper import ScraperFactory
from .models import Item, PriceLog
from .services import get_deals

logger = get_task_logger(__name__)
UserModel = get_user_model()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    if not settings.CELERY_ENABLE_SCHEDULED_TASKS:
        logger.info("Disabling periodic tasks")
        deleted_rows, _ = PeriodicTask.objects.filter(name__in=("send_mails", "scrape_tracked_items")).delete()
        logger.info("Deleted %s periodic tasks", deleted_rows)
    else:
        logger.info("Enabling periodic tasks")
        sender.add_periodic_task(crontab(hour="10,18", minute="0"), send_mails.s())
        sender.add_periodic_task(crontab(hour="*/1", minute="0"), scrape_tracked_items.s())


@app.task(time_limit=7 * 3600)
def send_mails():
    for user in UserModel.objects.all().filter(is_active=True):
        deals = get_deals(user)
        if len(deals) > 0:
            template = "scraper/deal_notification_email"
            context = {"username": user.username, "deals": deals}

            logger.info("New mail will be sent to %s", user.email)

            message_plain = render_to_string(f"{template}.txt", context)
            message_html = render_to_string(f"{template}.html", context)

            send_mail(
                subject="Deal Tracker - Daily deals",
                message=message_plain,
                html_message=message_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


@app.task(time_limit=3300)
def scrape_tracked_items():
    logger.info("Scheduling tasks for scraping tracked items")
    tracked_items = Item.objects.filter(wish__isnull=False).all()
    group(scrape_item.s(item.id) for item in tracked_items).apply_async()


@app.task(
    bind=True,
    autoretry_for=(BlockedByRemote,),
    max_retries=6,
)
def scrape_item(self, item_id):
    item = Item.objects.get(id=item_id)
    client = ScraperFactory()

    if not hasattr(self, "http_proxies"):
        self.http_proxies = settings.HTTP_PROXY_LIST.copy()

    if not hasattr(self, "https_proxies"):
        self.https_proxies = settings.HTTPS_PROXY_LIST.copy()

    scraper = client.get_scraper(item.shop.domain)

    http_proxy, https_proxy = random.choice(self.http_proxies), random.choice(self.https_proxies)
    if self.request.retries >= 2:
        scraper.set_proxy(http_proxy, https_proxy)
        logger.debug("Using proxies: %s, %s", http_proxy, https_proxy)

    try:
        new_item = scraper.scrape_item(item.url)
        logger.debug("New data for item_url=%s, item_data=%s", item.url, new_item)

        item.update_from_scraper(new_item)
        PriceLog.objects.create(item=item, price=new_item.price, stock=new_item.stock)

    except BlockedByRemote as exception:
        self.https_proxies.remove(http_proxy)
        self.http_proxies.remove(https_proxy)
        raise exception
