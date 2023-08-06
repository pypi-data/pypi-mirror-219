class GameSearch:
    def __init__(self, id: str, platform: str, title: str) -> None:
        self.id = id
        self.title = title

        self.platform = platform

    def __str__(self) -> str:
        return f"Game({self.id})"


class Driver:
    url: str

    E: dict[str, dict]

    def search(self, q: str, page: int) -> list[GameSearch]:
        ...
