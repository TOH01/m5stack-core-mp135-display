import theme
from application.timer_event import TimerEvent
from structures.dataclasses import CircleStyle, LabelStyle, Point, Rect, TextStyle
from structures.enums import TextAlignment, TextPreset
from widgets.container import Container
from widgets.label import Label
from widgets.renderer import Renderer
from widgets.widget import Widget


class SocketWidget(Widget):
    def __init__(
        self,
        rect: Rect,
        cx: int,
        name: str,
        val_watts: int,
        initial_state: bool,
    ) -> None:
        super().__init__(rect)
        self.cx = cx
        self.name = name
        self.val_watts = val_watts
        self.is_on = initial_state

    def set_state(self, is_on: bool) -> None:
        if self.is_on != is_on:
            self.is_on = is_on
            self.rerender = True

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            y_start = rect.y
            
            # Determine color based on state
            color = theme.GOOD if self.is_on else theme.FAINT
            rcx = self.cx
            rcy = y_start + 20  # center of the 40px ring
            
            # 1. Draw socket ring (Ø40, stroke 2, good 10% fill when ON)
            if self.is_on:
                renderer.draw_circle(Point(rcx, rcy), 20, CircleStyle(fill=theme.SOCKET_ON_FILL))
            
            # Outline
            renderer.draw_circle(Point(rcx, rcy), 20, CircleStyle(fill=None, outline=color, outline_width=2))
            
            # 2. Draw power glyph (13px inside ring: arc 300° + 2px stem)
            renderer.draw.arc(
                (rcx - 6, rcy - 6, rcx + 6, rcy + 6),
                start=300,
                end=240,
                fill=color,
                width=2,
            )
            # Stem line
            renderer.draw.line(
                (rcx, rcy - 8, rcx, rcy - 2),
                fill=color,
                width=2,
            )
            
            # 3. Draw name
            name_color = theme.TEXT if self.is_on else theme.SUB
            name_rect = Rect(self.cx - 35, y_start + 47, 70, 12)
            renderer.draw_text(
                name_rect,
                self.name,
                TextStyle(color=name_color, preset=TextPreset.HOUR_TEMP, alignment=TextAlignment.CENTER),
            )
            
            # 4. Draw watts (16 SemiBold + 'W' 8.5)
            font_watts = theme.FONT_MAP[TextPreset.SOCKET_WATTS]
            font_unit = theme.FONT_MAP[TextPreset.MICRO_LABEL]
            y_baseline = y_start + 76
            
            if self.is_on:
                val_text = f"{self.val_watts}"
                unit_text = "W"
                val_w = font_watts.getlength(val_text)
                unit_w = font_unit.getlength(unit_text)
                total_w = val_w + 2 + unit_w
                start_x = self.cx - total_w / 2
                
                renderer.draw.text((start_x, y_baseline), val_text, fill=theme.TEXT, font=font_watts, anchor="ls")
                renderer.draw.text((start_x + val_w + 2, y_baseline), unit_text, fill=theme.SUB, font=font_unit, anchor="ls")
            else:
                val_text = "—"
                unit_text = "W"
                val_w = font_watts.getlength(val_text)
                unit_w = font_unit.getlength(unit_text)
                total_w = val_w + 2 + unit_w
                start_x = self.cx - total_w / 2
                
                renderer.draw.text((start_x, y_baseline), val_text, fill=theme.FAINT, font=font_watts, anchor="ls")
                renderer.draw.text((start_x + val_w + 2, y_baseline), unit_text, fill=theme.FAINT, font=font_unit, anchor="ls")
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class PowerFooterWidget(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.total_watts = 248
        self.show_all_time = False

    def update_watts(self, total_watts: int) -> None:
        if self.total_watts != total_watts:
            self.total_watts = total_watts
            self.rerender = True

    def toggle_alternation(self) -> None:
        self.show_all_time = not self.show_all_time
        self.rerender = True

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            y_baseline = rect.y + rect.h - 2
            
            # Left: total watts + now
            font_watts = theme.FONT_MAP[TextPreset.FOOTER_STAT]
            font_now = theme.FONT_MAP[TextPreset.META_STATUS]
            
            val_text = f"{self.total_watts}"
            unit_text = " W"
            now_text = "now"
            
            val_w = font_watts.getlength(val_text)
            unit_w = font_watts.getlength(unit_text)
            
            renderer.draw.text((rect.x, y_baseline), val_text, fill=theme.TEXT, font=font_watts, anchor="ls")
            renderer.draw.text((rect.x + val_w, y_baseline), unit_text, fill=theme.TEXT, font=font_watts, anchor="ls")
            renderer.draw.text((rect.x + val_w + unit_w + 4, y_baseline), now_text, fill=theme.FAINT, font=font_now, anchor="ls")
            
            # Right: Alternating stats
            if self.show_all_time:
                label_text = "all-time "
                val_num = "1 284"
                val_unit = " kWh"
            else:
                label_text = "30 days "
                val_num = "182"
                val_unit = " kWh"
                
            val_unit_w = font_watts.getlength(val_unit)
            val_num_w = font_watts.getlength(val_num)
            
            rx = rect.x + rect.w
            renderer.draw.text((rx, y_baseline), val_unit, fill=theme.TEXT, font=font_watts, anchor="ls")
            renderer.draw.text((rx - val_unit_w, y_baseline), val_num, fill=theme.TEXT, font=font_watts, anchor="ls")
            renderer.draw.text((rx - val_unit_w - val_num_w - 4, y_baseline), label_text, fill=theme.FAINT, font=font_now, anchor="ls")
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class PowerPage(Container):
    def __init__(self) -> None:
        super().__init__(Rect(0, 0, 320, 240), theme.TRANSPARENT_CONTAINER)
        self.socket_states = [True, True, True, False]
        self.socket_watts = [142, 71, 35, 1000]
        
        self.construct_widgets()
        
        # Alternation timer every 5 seconds
        self.add_timer(TimerEvent(5000, self.toggle_footer_alternation))

    def construct_widgets(self) -> None:
        # 4 columns: x centers at 51, 123, 196, 268.
        # Height starts at y=76. Column width ~72.
        self.sockets = [
            SocketWidget(Rect(15, 76, 72, 90), 51, "Server", self.socket_watts[0], self.socket_states[0]),
            SocketWidget(Rect(87, 76, 72, 90), 123, "Monitor", self.socket_watts[1], self.socket_states[1]),
            SocketWidget(Rect(159, 76, 72, 90), 196, "Lamp", self.socket_watts[2], self.socket_states[2]),
            SocketWidget(Rect(231, 76, 72, 90), 268, "Heater", self.socket_watts[3], self.socket_states[3]),
        ]
        for socket_w in self.sockets:
            self.add_widget(socket_w)

        # Footer (y ≈ 206 to 218)
        self.footer_widget = PowerFooterWidget(Rect(13, 206, 294, 12))
        self.add_widget(self.footer_widget)
        self.update_total_watts()

    def update_total_watts(self) -> None:
        total = sum(w if state else 0 for w, state in zip(self.socket_watts, self.socket_states))
        self.footer_widget.update_watts(total)

    def toggle_footer_alternation(self) -> None:
        self.footer_widget.toggle_alternation()
        self.rerender = True

    def on_click(self, event) -> None:
        if self.visible:
            px, py = event.point.x, event.point.y
            # Touch target: y from 30 to 200 (vertical content area)
            if 30 <= py <= 200:
                col_idx = -1
                if 15 <= px < 87:
                    col_idx = 0
                elif 87 <= px < 159:
                    col_idx = 1
                elif 159 <= px < 231:
                    col_idx = 2
                elif 231 <= px < 305:
                    col_idx = 3
                
                if col_idx != -1:
                    # Optimistic toggle click
                    self.socket_states[col_idx] = not self.socket_states[col_idx]
                    self.sockets[col_idx].set_state(self.socket_states[col_idx])
                    self.update_total_watts()
                    self.rerender = True
