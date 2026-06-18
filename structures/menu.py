from dataclasses import dataclass

from widgets.container import Container


@dataclass
class Menu:
    index: int
    title: str
    container: Container
