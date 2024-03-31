# -*- coding: utf-8 -*-

from PySide6 import QtWidgets


def empty_items_from_grid_layout(grid_lay: QtWidgets.QGridLayout):
    """
    清空 grid_lay 中的所有 widget. 注意, 这个方法会在内存中删除所有的 widget.
    因为如果你不删除 widget, 它们还依然存在, 会导致 GUI 上乱掉. 请不要尝试仅仅从 layout
    中移除 widget 而不彻底从内存中清除它们.
    """
    for i in reversed(range(grid_lay.count())):
        widget = grid_lay.itemAt(i).widget()
        grid_lay.removeWidget(widget)
        widget.deleteLater()  # delete the widget and garbage collect it


def replace_items_in_grid_layout(
    grid_lay: QtWidgets.QGridLayout,
    item_wgt_list: list[QtWidgets.QWidget],
    item_per_row: int,
    pad_to_full_row: bool = True,
):
    """
    用 item_wgt_list 中的 widget 替换 grid_lay 中的所有 widget.
    """
    # 清除原有的 widget
    empty_items_from_grid_layout(grid_lay)

    # 如果我们需要 pad 填满一整行, 那么我们需要填充一些空的 widget
    if pad_to_full_row:
        # create a new list, don't modify the original list
        item_wgt_list = list(item_wgt_list)
        n_items = len(item_wgt_list)
        if n_items < item_per_row:
            n_more = item_per_row - n_items
            item_wgt_list.extend([QtWidgets.QLabel("") for _ in range(n_more)])

    # 将 widget 放入 grid 中
    row, col = 0, 0
    for item_wgt in item_wgt_list:
        grid_lay.addWidget(item_wgt, row, col)
        col += 1
        if col >= item_per_row:  # Change line when 3 checkboxes in a row
            col = 0
            row += 1
