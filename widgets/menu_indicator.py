from structures.dataclasses import CircleStyle, Point, Rect
from widgets.renderer import Renderer
from widgets.widget import Widget


class MenuIndicator(Widget):
    INACTIVE_RATIO = 0.7
    GAP_RATIO = 1.0
    MIN_RADIUS = 1

    def __init__(
        self,
        rect: Rect,
        pages: int,
        active_style: CircleStyle | None = None,
        inactive_style: CircleStyle | None = None,
    ) -> None:
        super().__init__(rect)
        self.pages = pages
        self.active_page = 1
        self.active_style = active_style or CircleStyle(fill=(255, 255, 255))
        self.inactive_style = inactive_style or CircleStyle(fill=(90, 90, 90))

    def set_active_page(self, active_page: int) -> None:
        if active_page < 1 or active_page > self.pages:
            raise ValueError(f"Invalid page {active_page}/{self.pages}")
        self.active_page = active_page

    def _compute_layout(self, rect: Rect) -> tuple[int, int, int, int]:
        active_r = max(self.MIN_RADIUS, rect.h // 2)

        while True:
            inactive_r = max(self.MIN_RADIUS, round(active_r * self.INACTIVE_RATIO))
            gap = max(2, round(active_r * self.GAP_RATIO))
            total_w = 2 * active_r + (self.pages - 1) * (2 * inactive_r + gap)

            if total_w <= rect.w or active_r <= self.MIN_RADIUS:
                return active_r, inactive_r, gap, total_w

            active_r -= 1

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            active_r, inactive_r, gap, total_w = self._compute_layout(rect)

            center_y = rect.y + rect.h // 2
            cursor_x = rect.x + (rect.w - total_w) // 2

            for page in range(1, self.pages + 1):
                if page == self.active_page:
                    r, style = active_r, self.active_style
                else:
                    r, style = inactive_r, self.inactive_style

                renderer.draw_circle(Point(cursor_x + r, center_y), r, style)
                cursor_x += 2 * r + gap
            self.rerender = False
