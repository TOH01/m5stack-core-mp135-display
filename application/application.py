from widgets.widget import Widget
from pathlib import Path
import driver.constants as constants
from driver.display import Display
from driver.input_manager import InputManager
import time
from structures.dataclasses import PressEvent, SwipeEvent
from application.timer_event import TimerEvent
from widgets.renderer import Renderer

class Application:
    def __init__(self, framebuffer_path: Path = constants.FRAMEBUFFER_PATH, refresh_interval_s: float = 0.05) -> None:
        self.stop = False
        self.widgets : list[Widget] = []
        self.timers: list[TimerEvent] = []
        self.display = Display(framebuffer_path=framebuffer_path)
        self.renderer = Renderer(self.display)
        self.input_manager = InputManager()
        self.input_manager.start()
        self.refresh_interval_s = refresh_interval_s

    def register_widget(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def register_timer(self, timer: TimerEvent):
        self.timers.append(timer)

    def main_loop(self) -> None:
        while not self.stop:
            self._execute()
            time.sleep(self.refresh_interval_s)

    def _execute(self) -> None:
        input_event = self.input_manager.poll()

        if isinstance(input_event, PressEvent):
            for widget in self.widgets:
                widget.on_click(input_event)
        if isinstance(input_event, SwipeEvent):
            for widget in self.widgets:
                widget.on_swipe(input_event)

        for timer in self.timers:
            timer.check()
        
        for widget in self.widgets:
            if widget.rerender:
                widget.render(self.renderer)
                widget.rerender = False

        self.renderer.update()
