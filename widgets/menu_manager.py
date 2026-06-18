import widgets.utils as utils
from structures.dataclasses import ContainerStyle, Rect
from structures.menu import Menu
from widgets.container import Container
from widgets.renderer import Renderer


class MenuManager(Container):
    def __init__(self, rect: Rect, style: ContainerStyle) -> None:
        super().__init__(rect, style)
        self.menus: list[Menu] = []
        self.active_idx = 0
        self._pending_clear: list[Rect] = []

    def register_menu(self, title: str, container: Container) -> Menu:
        menu = Menu(len(self.menus), title, container)
        container.visible = container.active = not self.menus
        self.add_widget(container)
        self.menus.append(menu)
        return menu

    def set_active(self, idx: int) -> Menu:
        if not (0 <= idx < len(self.menus)):
            raise ValueError(f"Invalid menu {idx}/{len(self.menus)}")
        if idx == self.active_idx:
            return self.menus[idx]

        old = self.menus[self.active_idx].container
        new = self.menus[idx].container
        old.visible = old.active = False
        new.visible = new.active = True
        new.rerender = True
        self._pending_clear = [widget.get_rect() for widget in old.widgets]
        self.active_idx = idx
        return self.menus[idx]

    def next(self) -> Menu:
        return self.set_active(min(self.active_idx + 1, len(self.menus) - 1))

    def prev(self) -> Menu:
        return self.set_active(max(self.active_idx - 1, 0))

    def render(self, renderer: Renderer) -> None:
        if not self.visible:
            return

        active = self.menus[self.active_idx].container

        if self.rerender:
            renderer.draw_rect(self.get_rect(), self.style.background)
            self.rerender = False
            active.rerender = True
            self._pending_clear = []
        elif self._pending_clear:
            new_rects = [widget.get_rect() for widget in active.widgets]
            for rect in utils.subtract_regions(self._pending_clear, new_rects):
                renderer.draw_rect(rect, self.style.background)
            self._pending_clear = []

        active.render(renderer)
