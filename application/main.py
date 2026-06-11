import theme
from application.application import Application
from application.timer_event import TimerEvent
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import Rect
from widgets.bottom_bar import BottomBar
from widgets.indoor_air_page import IndoorAirPage
from widgets.outside_page import OutsidePage
from widgets.page_manager import PageManager
from widgets.power_page import PowerPage
from widgets.system_page import SystemPage
from widgets.top_bar import TopBar


def setup(app: Application) -> None:

    def display_timer_cbk() -> None:
        app.display.set_brightness(30)

    timer = TimerEvent(5 * 60 * 1000, display_timer_cbk)

    top_bar = TopBar()
    bottom_bar = BottomBar()
    page_manager = PageManager(Rect(0, 0, 320, 240), top_bar, bottom_bar)
    
    page_manager.add_page(SystemPage())
    page_manager.add_page(IndoorAirPage())
    page_manager.add_page(OutsidePage())
    page_manager.add_page(PowerPage())

    def click_notifier(click_event) -> None:
        timer.reset()
        print(click_event)
        app.display.set_brightness(100)

    def swipe_callback(swipe_event) -> None:
        timer.reset()
        app.display.set_brightness(100)
        print(swipe_event)
        page_manager.handle_swipe(swipe_event)

    app.register_timer(timer)

    # Add page manager first, then top and bottom chrome bars on top of it
    app.register_widget(page_manager)
    app.register_widget(top_bar)
    app.register_widget(bottom_bar)

    app.set_swipe_callback(swipe_callback)
    app.set_click_notification(click_notifier)
    app.set_background(theme.BG)


if __name__ == "__main__":
    display = Display()
    input_manager = InputManager()
    app = Application(display, input_manager)
    setup(app)
    app.main_loop()
