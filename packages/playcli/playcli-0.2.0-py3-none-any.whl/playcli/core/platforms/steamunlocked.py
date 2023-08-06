from bs4 import BeautifulSoup

from playcli.core.web import scrap
from playcli.models.driver import Driver, GameSearch


class Steamunlocked(Driver):
    url: str = "https://steamunlocked.net/"

    E: dict[str, dict] = {"search": {"card": ".cover-item-title > a"}}

    def search(self, q: str, page: int) -> list[GameSearch]:
        E: dict[str, str] = self.E["search"]

        rs: list[GameSearch] = []
        parse: BeautifulSoup = scrap(self.url, ["page", str(page)], {"s": q})

        for el in parse.select(E["card"]):
            id: str = el["href"]  # type: ignore

            title: str = el.text.replace("Free Download", "")

            for x in [self.url, "-free-download", "/"]:
                id = id.replace(x, "")

            rs.append(
                GameSearch(id=id, title=title.strip(), platform=self.__class__.__name__)
            )

        return rs
