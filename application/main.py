from application.application import Application
from widgets.clickable import Clickable
from structures.dataclasses import Rect

app = Application()

def display_timer_cbk() -> None:
    app.display.set_brightness(70)

def click_cbk() -> None:
    app.display.set_brightness(100)

click_area = Clickable(Rect(0, 0, 320, 240), click_cbk)

if __name__ == '__main__':
    app.register_timer(5 * 60 * 1000, display_timer_cbk)
    app.register_widget(click_area)
    
    app.main_loop()