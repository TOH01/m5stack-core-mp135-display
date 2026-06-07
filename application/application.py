import time

from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import ContainerStyle, PressEvent, Rect, RectStyle, SwipeEvent
from widgets.container import Container
from widgets.renderer import Renderer
from widgets.widget import Widget


class Application:
    def __init__(
        self, display: Display, input_manager: InputManager, refresh_interval_s: float = 0.05
    ) -> None:
        self.stop = False
        self.timers: list[TimerEvent] = []
        self.display = display
        self.renderer = Renderer(self.display)
        self.input_manager = input_manager
        self.input_manager.start()
        self.refresh_interval_s = refresh_interval_s
        self.swipe_callback = None
        self.click_notifier = None
        self.root = Container(
            Rect(0, 0, self.display.width, self.display.height), ContainerStyle(RectStyle())
        )

    def register_widget(self, widget: Widget) -> None:
        self.root.add_widget(widget)

    def register_timer(self, timer: TimerEvent):
        self.timers.append(timer)

    def set_background(self, color):
        self.root.style.background.fill = color

    def set_click_notification(self, callback):
        self.click_notifier = callback

    def set_swipe_callback(self, callback):
        self.swipe_callback = callback

    def main_loop(self) -> None:
        while not self.stop:
            self._execute()
            time.sleep(self.refresh_interval_s)

    def _execute(self) -> None:
        input_event = self.input_manager.poll()

        if isinstance(input_event, PressEvent):
            if self.click_notifier:
                self.click_notifier(input_event)
            self.root.on_click(input_event)
        if isinstance(input_event, SwipeEvent):
            if self.swipe_callback:
                self.swipe_callback(input_event)

        for timer in self.timers:
            timer.check()

        self.root.render(self.renderer)

        self.renderer.update()
