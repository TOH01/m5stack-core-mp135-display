import theme
from structures.dataclasses import CircleStyle, Color, Point, Rect, RectStyle
from widgets.renderer import Renderer
from widgets.widget import Widget


class MenuIndicator(Widget):
    def __init__(self, rect: Rect, pages: int, background: Color = theme.Palette.SURFACE, active_style: RectStyle | None = None, inactive_style: CircleStyle | None = None) -> None:
        super().__init__(rect)
        self.pages = pages
        self.active_page = 1
        self.background = background
        self.active_style = active_style or RectStyle(fill=theme.Palette.ACCENT)
        self.inactive_style = inactive_style or CircleStyle(fill=theme.Palette.MUTED)

    def set_active_page(self, active_page: int) -> None:
        if active_page < 1 or active_page > self.pages:
            raise ValueError(f"Invalid page {active_page}/{self.pages}")
        self.active_page = active_page
        self.rerender = True

    def _compute_layout(self, rect: Rect) -> tuple[int, int, int, int]:
        dot_r = max(theme.Indicator.MIN_RADIUS, round((rect.h // 2) * theme.Indicator.DOT_RATIO))

        while True:
            dot_d = 2 * dot_r + 1
            pill_w = max(dot_d, round(dot_d * theme.Indicator.PILL_RATIO))
            gap = max(2, round(dot_r * theme.Indicator.GAP_RATIO))
            total_w = pill_w + (self.pages - 1) * (dot_d + gap)

            if total_w <= rect.w or dot_r <= theme.Indicator.MIN_RADIUS:
                return dot_r, pill_w, gap, total_w

            dot_r -= 1

    def render(self, renderer: Renderer) -> None:
        if not self.rerender:
            return

        rect = self.get_rect()
        renderer.draw_rect(rect, RectStyle(fill=self.background))
        dot_r, pill_w, gap, total_w = self._compute_layout(rect)

        dot_d = 2 * dot_r + 1
        center_y = rect.y + rect.h // 2
        cursor_x = rect.x + (rect.w - total_w) // 2

        for page in range(1, self.pages + 1):
            if page == self.active_page:
                renderer.draw_pill(Rect(cursor_x, center_y - dot_r, pill_w, dot_d), self.active_style)
                cursor_x += pill_w + gap
            else:
                renderer.draw_circle(Point(cursor_x + dot_r, center_y), dot_r, self.inactive_style)
                cursor_x += dot_d + gap
        self.rerender = False
