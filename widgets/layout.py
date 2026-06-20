import theme
from structures.dataclasses import Rect
from widgets.icon import Icon
from widgets.label import Label


class Layout1:
    def __init__(self, rect: Rect) -> None:
        margin = theme.Spacing.MARGIN

        self.hero_label    = Label(Rect(margin, 8, 180, 70), "", theme.hero_value_style())
        self.caption_label = Label(Rect(margin + 2, 84, rect.w - 2 * margin, 20), "", theme.caption_style())

    def get_layout(self) -> tuple[Label, Label]:
        return self.hero_label, self.caption_label
    

class Layout2:
    def __init__(self, rect: Rect) -> None:
        margin = theme.Spacing.MARGIN

        self.icon = Icon(Rect(rect.w - margin - 48, margin, 48, 48), [])

    def get_layout(self) -> Icon:
        return self.icon
    
class Layout3:
    def __init__(self, rect: Rect) -> None:
        margin = theme.Spacing.MARGIN
        col_w = (rect.w - 2 * margin) // 2
        left_x = margin
        right_x = margin + col_w

        icon_size = 32
        icon_slot_w = 66
        text_block_h = 50

        icon_x_offset = (icon_slot_w - icon_size) // 2
        row_y = 128
        icon_y = row_y + (text_block_h - icon_size) // 2

        self.icon_left  = Icon(Rect(left_x + icon_x_offset, icon_y, icon_size, icon_size), [])
        self.icon_right = Icon(Rect(right_x + icon_x_offset, icon_y, icon_size, icon_size), [])

    def get_layout(self) -> tuple[Icon, Icon]:
        return self.icon_left, self.icon_right


class Layout4:
    def __init__(self, rect: Rect) -> None:
        margin = theme.Spacing.MARGIN
        col_w = (rect.w - 2 * margin) // 2
        left_x = margin
        right_x = margin + col_w
        text_x = 55
        text_w = col_w - 72

        row_y = 128
        text_block_h = 50
        label_h = 28
        label_y = row_y + (text_block_h - label_h) // 2

        self.label_left = Label(Rect(left_x + text_x, label_y, text_w, label_h), "", theme.value_style())
        self.label_right = Label(Rect(right_x + text_x, label_y, text_w, label_h), "", theme.value_style())

    def get_layout(self):
        return self.label_left, self.label_right


class Layout5:
    def __init__(self, rect: Rect) -> None:
        margin = theme.Spacing.MARGIN
        col_w = (rect.w - 2 * margin) // 2
        left_x = margin
        right_x = margin + col_w
        text_x = 66
        text_w = col_w - 72

        row_y = 128
        caption_h = 20
        value_h = 28
        gap = 2

        caption_y = row_y
        value_y = row_y + caption_h + gap

        self.caption_left = Label(Rect(left_x + text_x, caption_y, text_w, caption_h), "", theme.caption_style())
        self.value_left = Label(Rect(left_x + text_x, value_y, text_w, value_h), "", theme.value_style())
        self.caption_right = Label(Rect(right_x + text_x, caption_y, text_w, caption_h), "", theme.caption_style())
        self.value_right = Label(Rect(right_x + text_x, value_y, text_w, value_h), "", theme.value_style())

    def get_layout(self):
        return (self.caption_left, self.value_left, self.caption_right, self.value_right)