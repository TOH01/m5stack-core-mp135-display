import theme
from structures.dataclasses import LabelStyle, Rect
from structures.enums import TextAlignment, TextPreset
from widgets.container import Container
from widgets.label import Label
from widgets.value_unit import ValueUnitWidget


class SystemPage(Container):
    def __init__(self) -> None:
        super().__init__(Rect(0, 0, 320, 240), theme.TRANSPARENT_CONTAINER)
        self.construct_widgets()

    def construct_widgets(self) -> None:
        # Styles
        label_micro_center = LabelStyle(
            color=theme.SUB,
            preset=TextPreset.MICRO_LABEL,
            alignment=TextAlignment.CENTER,
            tracking=1,
        )
        label_detail_center = LabelStyle(
            color=theme.FAINT, preset=TextPreset.META_STATUS, alignment=TextAlignment.CENTER
        )
        label_footer_left = theme.LABEL_SUB
        label_footer_right = LabelStyle(
            color=theme.FAINT, preset=TextPreset.META_STATUS, alignment=TextAlignment.RIGHT
        )

        # 1. CPU Column (Center x ≈ 62, width 98, start x = 13)
        self.add_widget(Label(Rect(13, 80, 98, 12), "CPU", label_micro_center))
        self.add_widget(
            ValueUnitWidget(
                Rect(13, 99, 98, 32),
                "34",
                "%",
                TextPreset.COLUMN_VALUE,
                TextPreset.UNIT,
                val_color=theme.TEXT,
                unit_color=theme.SUB,
            )
        )
        self.add_widget(Label(Rect(13, 138, 98, 12), "4 cores · 1.2 GHz", label_detail_center))

        # 2. RAM Column (Center x ≈ 160, width 98, start x = 111)
        self.add_widget(Label(Rect(111, 80, 98, 12), "RAM", label_micro_center))
        self.add_widget(
            ValueUnitWidget(
                Rect(111, 99, 98, 32),
                "35",
                "%",
                TextPreset.COLUMN_VALUE,
                TextPreset.UNIT,
                val_color=theme.TEXT,
                unit_color=theme.SUB,
            )
        )
        self.add_widget(Label(Rect(111, 138, 98, 12), "178 / 512 MB", label_detail_center))

        # 3. Temp Column (Center x ≈ 258, width 98, start x = 209)
        self.add_widget(Label(Rect(209, 80, 98, 12), "TEMP", label_micro_center))
        
        # Temp logic: <60° text · ≥60° warn · ≥75° bad
        temp_val = 52
        if temp_val < 60:
            temp_color = theme.TEXT
        elif temp_val < 75:
            temp_color = theme.WARN
        else:
            temp_color = theme.BAD
            
        self.add_widget(
            ValueUnitWidget(
                Rect(209, 99, 98, 32),
                f"{temp_val}°",
                "C",
                TextPreset.COLUMN_VALUE,
                TextPreset.UNIT,
                val_color=temp_color,
                unit_color=theme.SUB,
            )
        )
        self.add_widget(Label(Rect(209, 138, 98, 12), "throttle 85°", label_detail_center))

        # Footer (y ≈ 216, left x13, right x307)
        self.add_widget(Label(Rect(13, 206, 140, 12), "up 6d 04h", label_footer_left))
        self.add_widget(Label(Rect(167, 206, 140, 12), "192.168.1.135", label_footer_right))
