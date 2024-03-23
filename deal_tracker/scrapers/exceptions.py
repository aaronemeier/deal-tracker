class ScraperError(Exception):
    pass


class ItemException(ScraperError):
    pass


class ItemUrlInvalid(ScraperError):
    pass


class ScraperNotFound(ScraperError):
    pass


class ItemDoesNotExist(ScraperError):
    pass


class ItemParseError(ScraperError):
    pass


class ItemIdNotFound(ScraperError):
    pass


class BlockedByRemote(ScraperError):
    pass


class ScraperTimeout(BlockedByRemote):
    pass


class ScraperResponseError(BlockedByRemote):
    pass
