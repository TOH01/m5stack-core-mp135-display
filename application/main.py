from application.application import Application
from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager


def setup(app: Application) -> None:

    def display_timer_cbk() -> None:
        app.display.set_brightness(30)

    timer = TimerEvent(5 * 60 * 1000, display_timer_cbk)

    def click_notifier(click_event) -> None:
        timer.reset()
        print(click_event)
        app.display.set_brightness(100)

    def swipe_callback(swipe_event) -> None:
        print(swipe_event)

    app.register_timer(timer)

    app.set_swipe_callback(swipe_callback)
    app.set_click_notification(click_notifier)
    app.set_background((18, 18, 20))


if __name__ == "__main__":
    display = Display()
    input_manager = InputManager()
    app = Application(display, input_manager)
    setup(app)
    app.main_loop()
