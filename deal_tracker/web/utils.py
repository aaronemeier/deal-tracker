from urllib import parse


def get_domain_from_url(url):
    try:
        url = parse.urlparse(url)
        return str(".".join(url.netloc.split(".")[-2:]))
    except ValueError:
        return None
