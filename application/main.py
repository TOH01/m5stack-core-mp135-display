from application.application import Application
from application.timer_event import TimerEvent
from widgets.clickable import Clickable
from structures.dataclasses import Rect

app = Application()

def display_timer_cbk() -> None:
    app.display.set_brightness(30)

timer = TimerEvent(5 * 60 * 1000, display_timer_cbk)

def click_cbk() -> None:
    timer.reset()
    app.display.set_brightness(100)

click_area = Clickable(Rect(0, 0, 320, 240), click_cbk)

if __name__ == '__main__':
    app.register_timer(timer)
    app.register_widget(click_area)
    
    app.main_loop()