import re

import pytest

from deal_tracker.scrapers.scraper import ScraperFactory

# pylint: disable=redefined-outer-name


@pytest.fixture
def scraper_client():
    return ScraperFactory()


def test_get_scrapers_count(scraper_client):
    scrapers = scraper_client.get_scrapers()
    assert len(scrapers) > 0


@pytest.mark.no_ci
def test_get_scraper_digitec(scraper_client):
    url = "https://www.digitec.ch/en/product/nintendo-switch-neon-rotneon-blau-de-fr-it-en-spielkonsole-11586094"
    shop = "digitec.ch"
    brand = "Nintendo"
    image_url = re.compile("https://www.digitec.ch/im/Files/.*")
    description = re.compile(r"[a-zA-Z0-9-.:; ]+")

    digitec_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = digitec_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert re.compile("Nintendo Switch.*").match(scraped_item.name)
    assert scraped_item.brand == brand
    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock in (0, 10)


@pytest.mark.no_ci
def test_get_scraper_galaxus(scraper_client):
    url = "https://www.galaxus.ch/en/s5/product/lego-millennium-falcon-75192-lego-7238420"
    shop = "galaxus.ch"
    name = re.compile("LEGO Millennium Falcon.*")
    brand = "LEGO"
    image_url = re.compile("https://www.galaxus.ch/im/Files/.*")
    description = re.compile(r"[a-zA-Z0-9-.:; ]+")

    galaxus_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = galaxus_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert name.match(scraped_item.name)
    assert scraped_item.brand == brand
    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock in (0, 10)


@pytest.mark.no_ci
def test_get_scraper_brack(scraper_client):
    url = "https://www.brack.ch/nintendo-switch-rot-blau-1485182"
    shop = "brack.ch"
    name = re.compile("Switch.*")
    brand = "Nintendo"
    image_url = re.compile("https://cdn.competec.ch/.*")
    description = re.compile(r"[a-zA-Z0-9-.:; ]+")

    brack_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = brack_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert name.match(scraped_item.name)
    assert scraped_item.brand == brand
    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock > 0.0


@pytest.mark.no_ci
def test_get_scraper_zalando(scraper_client):
    url = "https://www.zalando.ch/nike-sportswear-club-hoodie-sweatjacke-blackblackwhite-ni122s0au-q11.html"
    shop = "zalando.ch"
    name = re.compile("CLUB HOODIE.*")
    brand = "Nike Sportswear"
    image_url = re.compile("https://img.*.ztat.net/.*")
    description = re.compile("[a-zA-Z0-9-.:; ]+")

    zalando_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = zalando_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert name.match(scraped_item.name)
    assert scraped_item.brand == brand
    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock >= 0


@pytest.mark.no_ci
def test_get_scraper_jysk(scraper_client):
    url = "https://jysk.ch/de/schlafzimmer/boxspringbetten/boxspringbett-90x200cm-plus-c60-grau-33"
    shop = "jysk.ch"
    name = re.compile("Boxspringbett.*")
    brand = "DREAMZONE"
    image_url = re.compile("https://.*.jysk.com/getimage.*")
    description = re.compile(r"[a-zA-Z0-9-.:; \/²]+")

    jysk_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = jysk_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert name.match(scraped_item.name)
    assert scraped_item.brand == brand
    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock >= 0


@pytest.mark.no_ci
def test_get_scraper_toppreise(scraper_client):
    url = "https://www.toppreise.ch/preisvergleich/Kopfhoerer/APPLE-AirPods-mit-kabellosem-Ladecase-MME73ZM-A-p668453"
    shop = "toppreise.ch"
    name = re.compile("AirPods.*")
    brand = "Apple"
    image_url = re.compile("https://imgsrv.toppreise.ch/.*")
    description = re.compile(r"[a-zA-Z0-9-.:;\w,\/²(_)]+")

    toppreise_scraper = scraper_client.get_scraper(domain=shop)
    scraped_item = toppreise_scraper.scrape_item(url)

    assert scraped_item.url == url
    assert scraped_item.shop == shop
    assert name.match(scraped_item.name)

    assert scraped_item.brand == brand

    assert scraped_item.price > 0.0
    assert image_url.match(scraped_item.image_url)
    assert description.match(scraped_item.description)
    assert scraped_item.stock >= 0
