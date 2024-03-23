from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    url: Optional[str] = None
    shop: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.name, self.url}"

    def is_empty(self):
        for obj in self.__dict__:
            if obj is None:
                return True
        return False
