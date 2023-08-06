from bs4 import BeautifulSoup
from rich import print
from rich.table import Table

from playcli.core.web import scrap
from playcli.values import BASE_URL
from playcli.values import E_SEARCH as E


def call(q: str, page: int):
    parse: BeautifulSoup = scrap(params={"q": q, "page": page})

    table: Table = Table(box=None, expand=True)

    table.add_column("Title")
    table.add_column("Id", style="green", no_wrap=True)

    for el in parse.select(E["card"]):
        title: str = el.text
        id: str = el["href"].replace(BASE_URL + "games/", "")  # type: ignore

        if title in E["skip"]:  # ADS
            continue

        table.add_row(title, id)

    if table.row_count >= 1:
        print(table)
    else:
        print("No results were found.")
