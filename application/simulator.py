import io
import tkinter as tk
from collections import deque

import driver.constants as constants
import driver.utils as utils
from application.application import Application
from application.main import setup
from structures.dataclasses import Point, PressEvent, Rect, SwipeEvent


class SimDisplay:
    def __init__(self) -> None:
        self.width = constants.DISPLAY_WIDTH
        self.height = constants.DISPLAY_HEIGHT

    def draw_region(self, rect: Rect, data: bytes) -> None:
        print(f"Draw {len(data)} bytes")

    def set_brightness(self, brightness: int) -> None:
        pass

    def close(self) -> None:
        pass


class SimInputManager:
    def __init__(self, canvas: tk.Canvas, swipe_threshold: int = 30) -> None:
        self.events: deque[SwipeEvent | PressEvent] = deque(maxlen=32)
        self._threshold = swipe_threshold
        self._down: Point | None = None
        canvas.bind("<ButtonPress-1>", self._on_down)
        canvas.bind("<ButtonRelease-1>", self._on_up)

    def start(self) -> None:
        pass

    def poll(self) -> SwipeEvent | PressEvent | None:
        return self.events.popleft() if self.events else None

    def _on_down(self, e: tk.Event) -> None:
        self._down = Point(e.x, e.y)

    def _on_up(self, e: tk.Event) -> None:
        if not self._down:
            return
        up = Point(e.x, e.y)
        if utils.get_distance(up, self._down) < self._threshold:
            self.events.append(PressEvent(up))
        else:
            self.events.append(SwipeEvent(utils.get_swipe_direction(self._down, up)))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("M5Stack Simulator")
    root.resizable(False, False)

    tk_canvas = tk.Canvas(root, width=constants.DISPLAY_WIDTH, height=constants.DISPLAY_HEIGHT, highlightthickness=0)
    tk_canvas.pack()

    display = SimDisplay()
    input_manager = SimInputManager(tk_canvas)
    app = Application(display, input_manager)
    setup(app)

    photo: list[tk.PhotoImage | None] = [None]

    def tick() -> None:
        app._execute()
        ppm = io.BytesIO()
        app.renderer.canvas.save(ppm, format="PPM")
        photo[0] = tk.PhotoImage(data=ppm.getvalue())
        tk_canvas.create_image(0, 0, anchor=tk.NW, image=photo[0])
        root.after(int(app.refresh_interval_s * 1000), tick)

    tick()
    root.mainloop()
