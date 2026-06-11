import theme
from structures.dataclasses import Rect
from structures.enums import Direction
from widgets.bottom_bar import BottomBar
from widgets.container import Container
from widgets.top_bar import TopBar


class PageManager(Container):
    def __init__(self, rect: Rect, top_bar: TopBar, bottom_bar: BottomBar) -> None:
        super().__init__(rect, theme.TRANSPARENT_CONTAINER)
        self.top_bar = top_bar
        self.bottom_bar = bottom_bar
        self.pages: list[Container] = []
        self.current_page_idx = 1
        
        self.titles = {
            1: "SYSTEM",
            2: "INDOOR AIR",
            3: "OUTSIDE",
            4: "POWER",
        }

    def add_page(self, page_container: Container) -> None:
        # Register the page container as a child widget
        self.add_widget(page_container)
        self.pages.append(page_container)
        
        # Hide pages by default except the first one
        idx = len(self.pages)
        if idx == self.current_page_idx:
            page_container.visible = True
            page_container.active = True
        else:
            page_container.visible = False
            page_container.active = False

    def handle_swipe(self, swipe_event) -> None:
        if not self.pages:
            return

        num_pages = len(self.pages)
        if swipe_event.direction == Direction.LEFT:
            # Swipe left (pull next page)
            next_idx = (self.current_page_idx % num_pages) + 1
            self.set_page(next_idx)
        elif swipe_event.direction == Direction.RIGHT:
            # Swipe right (pull previous page)
            prev_idx = ((self.current_page_idx - 2) % num_pages) + 1
            self.set_page(prev_idx)

    def set_page(self, page_idx: int) -> None:
        if page_idx < 1 or page_idx > len(self.pages):
            return
        
        self.current_page_idx = page_idx
        
        # Update each page's visibility and active flags
        for i, page in enumerate(self.pages, 1):
            if i == page_idx:
                page.visible = True
                page.active = True
                page.rerender = True
            else:
                page.visible = False
                page.active = False
        
        # Sync Chrome
        self.top_bar.update_title(self.titles.get(page_idx, ""))
        self.bottom_bar.menu_indicator.set_active_page(page_idx)
        
        # Trigger rerender on ourselves and parent to redraw screen background
        self.rerender = True
        if self.parent:
            self.parent.rerender = True
