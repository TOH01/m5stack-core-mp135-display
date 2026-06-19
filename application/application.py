import time
from typing import Callable

from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import Color, ContainerStyle, PressEvent, Rect, RectStyle, SwipeEvent
from widgets.container import Container
from widgets.renderer import Renderer
from widgets.widget import Widget


class Application:
    def __init__(self, display: Display, input_manager: InputManager, target_fps: float = 60.0) -> None:
        self.stop = False
        self.display = display
        self.renderer = Renderer(self.display)
        self.input_manager = input_manager
        self.input_manager.start()
        self.frame_interval_s = 1.0 / target_fps
        self.swipe_callback: Callable | None = None
        self.click_notifier: Callable | None = None
        self.root = Container(Rect(0, 0, self.display.width, self.display.height), ContainerStyle(RectStyle()))

    def register_widget(self, widget: Widget) -> None:
        self.root.add_widget(widget)

    def register_timer(self, timer: TimerEvent) -> None:
        self.root.add_timer(timer)

    def set_background(self, color: Color) -> None:
        self.root.style.background.fill = color
        self.root.rerender = True

    def set_click_notification(self, callback: Callable) -> None:
        self.click_notifier = callback

    def set_swipe_callback(self, callback: Callable) -> None:
        self.swipe_callback = callback

    def main_loop(self) -> None:
        while not self.stop:
            frame_start = time.monotonic()
            self._execute()
            elapsed = time.monotonic() - frame_start
            time.sleep(max(0.0, self.frame_interval_s - elapsed))

    def _execute(self) -> None:
        input_event = self.input_manager.poll()

        if isinstance(input_event, PressEvent):
            if self.click_notifier:
                self.click_notifier(input_event)
            self.root.on_click(input_event)
        if isinstance(input_event, SwipeEvent):
            if self.swipe_callback:
                self.swipe_callback(input_event)

        self.root.check_timers()

        self.root.render(self.renderer)

        self.renderer.update()
