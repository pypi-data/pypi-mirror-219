from rich import print
from rich.table import Table

from playcli.models import Driver, Platforms


def call(q: str, page: int, platform: Platforms):
    table: Table = Table(box=None, expand=True)

    table.add_column("Title")
    table.add_column("Id", style="green", no_wrap=True)

    match platform.value:
        case "all":
            for driver in platform:
                print(f"[green]Searching in {driver.__class__.__name__}[/]")

                for game in driver.search(q, page):
                    table.add_row(game.title, game.id + f"-{game.platform.lower()}")
        case "recursive":
            for driver in platform:
                print(f"[green]Searching in {driver.__class__.__name__}[/]")

                for game in driver.search(q, page):
                    table.add_row(game.title, game.id + f"-{game.platform.lower()}")

                if table.row_count != 0:
                    print(f"[green]Results found...[/]")

                    break
        case _:
            driver: Driver = platform.dv()

            for game in driver.search(q, page):
                table.add_row(game.title, game.id + f"-{game.platform.lower()}")

    if table.row_count != 0:
        print("\n", table)
    else:
        print("[red]No results were found.[/]")
