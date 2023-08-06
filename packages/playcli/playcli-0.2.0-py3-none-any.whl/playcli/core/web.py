from bs4 import BeautifulSoup
from requests import Response
from requests import get as requests_get
from rich import print
from typer import Exit


def scrap(url: str, router: list[str] = [], params: dict = {}) -> BeautifulSoup:
    res: Response = requests_get(url + "/".join(router), params=params)

    if res.status_code != 200:
        print("[red]An error occurred while trying to communicate with the service.[/]")

        raise Exit(code=1)

    return BeautifulSoup(res.text, "html.parser")
