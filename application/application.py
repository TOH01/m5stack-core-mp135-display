from widgets.widget import Widget
from pathlib import Path
import driver.constants as constants
from driver.display import Display
from typing import Callable
from driver.input_manager import InputManager
import time

class Application:
    def __init__(self, framebuffer_path: Path = constants.FRAMEBUFFER_PATH) -> None:
        self.stop = False
        self.widgets : list[Widget] = []
        self.display = Display(framebuffer_path=framebuffer_path)
        self.input_manager = InputManager()
        self.input_manager.start()


    def register_widget(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def register_timer(self, interval: int, callback: Callable):
        pass

    def main_loop(self) -> None:
        while not self.stop:
            self._execute()
            time.sleep(0.1)

    def _execute(self) -> None:
        self.input_manager.poll()

        for widget in self.widgets:
            if widget.rerender:
                widget.render()
