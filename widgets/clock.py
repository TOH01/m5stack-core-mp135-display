from datetime import datetime

import theme
from application.timer_event import TimerEvent
from structures.dataclasses import ContainerStyle, Rect
from widgets.container import Container
from widgets.label import Label


class Clock(Container):
    def __init__(self, rect: Rect, style: ContainerStyle) -> None:
        super().__init__(rect, style)

        self._colon_visible = True

        self.add_timer(TimerEvent(1000, self._update_time))
        self.add_timer(TimerEvent(750, self._blink_colon))

        self._build()

    def _make_label(self, text: str, x: int, width: int) -> Label:
        return Label(
            Rect(x, 0, width, 20),
            text,
            theme.LABEL_TIME,
        )

    def _update_time(self) -> None:
        now = datetime.now()

        hour = f"{now.hour:02d}"
        minute = f"{now.minute:02d}"

        if self.last_hour != hour:
            self.hour_widget.update_text(hour)
            self.last_hour = hour
        if self.last_minute != minute:
            self.min_widget.update_text(minute)
            self.last_minute = minute

    def _blink_colon(self) -> None:
        self._colon_visible = not self._colon_visible

        if self._colon_visible:
            self.sep_widget.update_text(":")
        else:
            self.sep_widget.update_text(" ")

    def _build(self) -> None:
        now = datetime.now()
        hour = f"{now.hour:02d}"
        minute = f"{now.minute:02d}"

        self.last_hour = hour
        self.last_minute = minute

        self.hour_widget = self._make_label(hour, 0, 20)
        self.sep_widget = self._make_label(":", 22, 6)
        self.min_widget = self._make_label(minute, 32, 20)

        self.add_widget(self.hour_widget)
        self.add_widget(self.sep_widget)
        self.add_widget(self.min_widget)
