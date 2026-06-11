import theme
from structures.dataclasses import Rect, RectStyle
from widgets.renderer import Renderer
from widgets.widget import Widget


class MenuIndicator(Widget):
    def __init__(
        self,
        rect: Rect,
        pages: int,
    ) -> None:
        super().__init__(rect)
        self.pages = pages
        self.active_page = 1

    def set_active_page(self, active_page: int) -> None:
        if active_page < 1 or active_page > self.pages:
            raise ValueError(f"Invalid page {active_page}/{self.pages}")
        if self.active_page != active_page:
            self.active_page = active_page
            self.rerender = True

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Active pill is 14px wide, inactive dots are 5px wide. Gap is 7px.
            total_w = 14 + (self.pages - 1) * 5 + (self.pages - 1) * 7
            
            # Center vertically and horizontally in self.rect
            start_x = rect.x + (rect.w - total_w) // 2
            start_y = rect.y + (rect.h - 5) // 2
            
            cursor_x = start_x
            for page in range(1, self.pages + 1):
                if page == self.active_page:
                    pill_rect = Rect(cursor_x, start_y, 14, 5)
                    renderer.draw_rect(pill_rect, RectStyle(fill=theme.TEXT, radius=2))
                    cursor_x += 14 + 7
                else:
                    dot_rect = Rect(cursor_x, start_y, 5, 5)
                    renderer.draw_rect(dot_rect, RectStyle(fill=theme.FAINT, radius=2))
                    cursor_x += 5 + 7
            self.rerender = False

