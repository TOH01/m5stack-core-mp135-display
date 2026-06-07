from application.application import Application
from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import Rect
from widgets.clickable import Clickable


def setup(app: Application) -> None:
    def display_timer_cbk() -> None:
        app.display.set_brightness(30)

    timer = TimerEvent(5 * 60 * 1000, display_timer_cbk)

    def click_cbk() -> None:
        timer.reset()
        app.display.set_brightness(100)

    click_area = Clickable(Rect(0, 0, 320, 240), click_cbk)

    app.register_timer(timer)
    app.register_widget(click_area)


if __name__ == "__main__":
    display = Display()
    input_manager = InputManager()
    app = Application(display, input_manager)
    setup(app)
    app.main_loop()
