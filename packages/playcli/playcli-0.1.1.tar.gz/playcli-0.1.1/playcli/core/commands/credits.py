from rich import print

from playcli import __meta__ as meta


def call():
    print(f"Project by [red]{meta['author']}[/] - {meta['version']}")
    print(f": {meta['project_url'][2]}")
