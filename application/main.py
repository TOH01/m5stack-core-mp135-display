import theme
from application.application import Application
from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import PressEvent, SwipeEvent
from widgets.bottom_bar import BottomBar
from widgets.top_bar import TopBar

DISPLAY_TIMEOUT_MS = 5 * 60 * 1000
DIM_BRIGHTNESS     = 30
FULL_BRIGHTNESS    = 100

app: Application
dim_timer: TimerEvent


def on_dim_timeout() -> None:
    app.display.set_brightness(DIM_BRIGHTNESS)


def on_click(click_event: PressEvent) -> None:
    dim_timer.reset()
    print(click_event)
    app.display.set_brightness(FULL_BRIGHTNESS)


def on_swipe(swipe_event: SwipeEvent) -> None:
    print(swipe_event)


def setup(application: Application) -> None:
    global app, dim_timer
    app = application
    dim_timer = TimerEvent(DISPLAY_TIMEOUT_MS, on_dim_timeout)

    app.register_timer(dim_timer)

    app.register_widget(TopBar())
    app.register_widget(BottomBar())

    app.set_swipe_callback(on_swipe)
    app.set_click_notification(on_click)
    app.set_background(theme.Palette.BACKGROUND)


if __name__ == "__main__":
    display = Display()
    input_manager = InputManager()
    application = Application(display, input_manager)
    setup(application)
    application.main_loop()
