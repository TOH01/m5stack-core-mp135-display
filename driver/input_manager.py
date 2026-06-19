from collections import deque
from pathlib import Path
from threading import Thread

from evdev import InputDevice, ecodes

import driver.constants as constants
import driver.utils as utils
from structures.dataclasses import Point, PressEvent, SwipeEvent
from structures.enums import TouchEvent


class InputManager:
    def __init__(self, device_path: Path = constants.INPUT_DEVICE_PATH, swipe_threshold: int = 20) -> None:
        self.device = InputDevice(device_path)
        self.swipe_threshold = swipe_threshold
        self.events: deque[SwipeEvent | PressEvent] = deque(maxlen=32)

    def start(self) -> None:
        Thread(target=self._run, daemon=True).start()

    def poll(self) -> SwipeEvent | PressEvent | None:
        if self.events:
            return self.events.popleft()
        return None

    def add_to_queue(self, up: Point, down: Point) -> None:
        if utils.get_distance(up, down) < self.swipe_threshold:
            self.events.append(PressEvent(Point(up.x, up.y)))
        else:
            direction = utils.get_swipe_direction(down, up)
            self.events.append(SwipeEvent(direction))

    def _run(self) -> None:
        down_point = Point(-1, -1)
        up_point = Point(-1, -1)
        temp_x, temp_y = -1, -1
        temp_touch_event = None
        start_drag = False

        for e in self.device.read_loop():
            if e.type == ecodes.EV_ABS:
                if e.code == ecodes.ABS_MT_POSITION_X:
                    temp_x = e.value
                if e.code == ecodes.ABS_MT_POSITION_Y:
                    temp_y = e.value

            elif e.type == ecodes.EV_KEY:
                if e.code == ecodes.BTN_TOUCH:
                    temp_touch_event = e.value

            elif e.type == ecodes.EV_SYN and e.code == ecodes.SYN_REPORT:
                if temp_touch_event == TouchEvent.UP and temp_x >= 0 and temp_y >= 0:
                    start_drag = False
                    up_point.x = temp_x
                    up_point.y = temp_y
                    self.add_to_queue(up_point, down_point)
                if (
                    temp_touch_event == TouchEvent.DOWN
                    and temp_x >= 0
                    and temp_y >= 0
                    and not start_drag
                ):
                    start_drag = True
                    down_point.x = temp_x
                    down_point.y = temp_y
