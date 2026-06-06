from threading import Thread
from evdev import InputDevice, ecodes
from collections import deque
import driver.constants as constants

class InputManager:
    def __init__(self, device_path=constants.INPUT_DEVICE_PATH, swipe_threshold=30) -> None:
        self.device = InputDevice(device_path)
        self.swipe_threshold = swipe_threshold
        self.events = deque(maxlen=32)

    def start(self) -> None:
        Thread(target=self._run, daemon=True).start()

    def poll(self) -> None:
        pass

    def _run(self):
        for e in self.device.read_loop():
            print(e.type)
            print(e.code)
            print(e.value)
