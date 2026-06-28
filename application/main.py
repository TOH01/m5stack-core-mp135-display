import theme
from application.application import Application
from application.indoor_air_data import IndoorAirData
from application.timer_event import TimerEvent
from application.weather_data import WeatherData
from driver.display import Display
from driver.input_manager import InputManager
from structures.dataclasses import PressEvent, Rect, SwipeEvent
from structures.enums import Direction
from structures.menu import Menu
from widgets.air_quality_menu import AirQualityMenu
from widgets.bottom_bar import BottomBar
from widgets.container import Container
from widgets.label import Label
from widgets.menu_manager import MenuManager
from widgets.outdoor_menu import OutdoorWeatherMenu
from widgets.top_bar import TopBar

DISPLAY_TIMEOUT_MS = 5 * 60 * 1000
DIM_BRIGHTNESS     = 30
FULL_BRIGHTNESS    = 100

CONTENT_W = theme.Spacing.SCREEN_W
CONTENT_H = theme.Spacing.SCREEN_H - 2 * theme.Spacing.BAR_HEIGHT

MENU_TITLES = ["Air Quality", "Outdoor", "Power", "System"]

app: Application
dim_timer: TimerEvent
top_bar: TopBar
bottom_bar: BottomBar
menu_manager: MenuManager
weather_data: WeatherData
indoor_air_data: IndoorAirData
outdoor: OutdoorWeatherMenu
air_quality: AirQualityMenu


def build_menu(title: str, slot: int) -> Container:
    container = Container(Rect(0, 0, CONTENT_W, CONTENT_H), theme.transparent_container_style())
    container.add_widget(Label(Rect((CONTENT_W - 160) // 2, 20 + slot * 35, 160, 24), title, theme.content_text_style()))
    return container

def show_menu(menu: Menu) -> None:
    top_bar.update_title(menu.title)
    bottom_bar.menu_indicator.set_active_page(menu.index + 1)


def on_dim_timeout() -> None:
    app.display.set_brightness(DIM_BRIGHTNESS)


def on_data_timer() -> None:
    if menu_manager.active_idx == 1 and weather_data.new_data:
        weather_data.new_data = False
        data = weather_data.get_data()
        outdoor.set_reading(data)

    if menu_manager.active_idx == 0:
        data = indoor_air_data.get_data()
        air_quality.set_reading(data)


def on_click(click_event: PressEvent) -> None:
    dim_timer.reset()
    app.display.set_brightness(FULL_BRIGHTNESS)


def on_swipe(swipe_event: SwipeEvent) -> None:
    dim_timer.reset()
    app.display.set_brightness(FULL_BRIGHTNESS)

    if weather_data.new_data:
        weather_data.new_data = False
        data = weather_data.get_data()
        outdoor.set_reading(data)

    data = indoor_air_data.get_data()
    air_quality.set_reading(data)

    if swipe_event.direction == Direction.LEFT:
        show_menu(menu_manager.next())
    elif swipe_event.direction == Direction.RIGHT:
        show_menu(menu_manager.prev())


def setup(application: Application) -> None:
    global app, dim_timer, top_bar, bottom_bar, menu_manager, weather_data, indoor_air_data, outdoor, air_quality
    app = application
    dim_timer = TimerEvent(DISPLAY_TIMEOUT_MS, on_dim_timeout)
    app.register_timer(dim_timer)

    data_timer = TimerEvent(1000, on_data_timer)
    app.register_timer(data_timer)

    top_bar = TopBar()
    menu_manager = MenuManager(Rect(0, theme.Spacing.BAR_HEIGHT, CONTENT_W, CONTENT_H), theme.menu_background_style())

    air_quality = AirQualityMenu(Rect(0, 0, CONTENT_W, CONTENT_H))
    menu_manager.register_menu(MENU_TITLES[0], air_quality)

    indoor_air_data = IndoorAirData()
    indoor_air_data.start()

    outdoor = OutdoorWeatherMenu(Rect(0, 0, CONTENT_W, CONTENT_H))
    menu_manager.register_menu(MENU_TITLES[1], outdoor)

    weather_data = WeatherData()
    weather_data.start()

    bottom_bar = BottomBar(len(MENU_TITLES))

    app.register_widget(top_bar)
    app.register_widget(menu_manager)
    app.register_widget(bottom_bar)

    app.set_swipe_callback(on_swipe)
    app.set_click_notification(on_click)
    app.set_background(theme.Palette.BACKGROUND)

    show_menu(menu_manager.menus[0])


if __name__ == "__main__":
    display = Display()
    input_manager = InputManager()
    application = Application(display, input_manager)
    setup(application)
    application.main_loop()
