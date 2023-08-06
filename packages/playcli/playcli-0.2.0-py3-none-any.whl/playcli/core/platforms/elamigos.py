from bs4 import BeautifulSoup

from playcli.core.web import scrap
from playcli.models.driver import Driver, GameSearch


class Elamigos(Driver):
    url: str = "https://www.elamigos-games.com/"

    E: dict[str, dict] = {
        "search": {
            "skip": ["Mortal Kombat 1 Online"],
            "card": ".card-title > a",
        }
    }

    def search(self, q: str, page: int) -> list[GameSearch]:
        E: dict[str, str] = self.E["search"]

        rs: list[GameSearch] = []
        parse: BeautifulSoup = scrap(self.url, params={"q": q, "page": page})

        for el in parse.select(E["card"]):
            title: str = el.text
            id: str = el["href"].replace(self.url + "games/", "")  # type: ignore

            if title in E["skip"]:  # SKIP
                continue

            rs.append(GameSearch(id=id, title=title, platform=self.__class__.__name__))

        return rs
