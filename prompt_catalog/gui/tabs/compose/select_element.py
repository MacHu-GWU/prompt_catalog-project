# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import typing as T

from PySide6 import QtWidgets, QtCore

from ...utils import api as gui_utils
from ....fts import element_dataset

if T.TYPE_CHECKING:  # pragma: no cover
    from .select_choice import SelectChoiceWidget


class ElementRadioButton(gui_utils.RadioButton):
    """
    todo: add docstring
    """

    def __init__(
        self,
        parent,
        display_value: gui_utils.DisplayValue,
        element_id: str,
        element_name: str,
        select_element_wgt: "SelectElementWidget",
    ):
        super().__init__(parent=parent, display_value=display_value)
        self.element_id = element_id
        self.element_name = element_name
        self.select_element_wgt = select_element_wgt

    # fmt: off
    def toggled_event_handler(self):
        print("📣 ElementRadioButton.toggled_event_handler")
        # 更新 line edit 中的内容
        self.select_element_wgt.search_element_line_edit_wgt.setText(self.display_value.label)
        self.select_element_wgt.selected_element_id = self.element_id
        self.select_element_wgt.selected_element_name = self.element_name
        # 如果这个 radio 改变了, search choice results 也要跟着变
        self.select_element_wgt.select_choice_wgt.query_changed_event_handler()
        self.select_element_wgt.select_choice_wgt.search_choice_line_edit_wgt.setText("")
        self.select_element_wgt.select_choice_wgt.search_choice_browser_wgt.setText("")
    # fmt: on


class ElementGridLayout(QtWidgets.QGridLayout):
    """
    todo: add docstring
    """

    def __init__(
        self,
        *args,
        item_per_row: int = 5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.item_per_row = item_per_row
        self.radio_wgt_list: list[QtWidgets.QRadioButton] = list()
        self.radio_group = QtWidgets.QButtonGroup()

    def clear_items(self):
        gui_utils.empty_items_from_grid_layout(self)
        self.radio_wgt_list.clear()

    def set_items(
        self,
        radio_wgt_list: list[QtWidgets.QRadioButton],
    ):
        self.clear_items()
        gui_utils.replace_items_in_grid_layout(
            grid_lay=self,
            item_wgt_list=radio_wgt_list,
            item_per_row=self.item_per_row,
            pad_to_full_row=True,
        )
        self.radio_wgt_list.extend(radio_wgt_list)
        for radio_wgt in radio_wgt_list:
            self.radio_group.addButton(radio_wgt)


class SelectElementWidget(QtWidgets.QWidget):
    """
    todo: add docstring
    """

    def __init__(
        self,
        parent,
        ith: int,
        select_choice_wgt: "SelectChoiceWidget",
    ):
        super().__init__(parent)
        self.ith = ith
        self.select_choice_wgt = select_choice_wgt

        self.selected_element_id: T.Optional[str] = None
        self.selected_element_name: T.Optional[str] = None

        self.set_widget()
        self.set_layout()

    # fmt: off
    def set_widget(self):
        self.ith_label_wgt = QtWidgets.QLabel(f"Element {self.ith}")
        self.ith_label_wgt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.search_element_label_wgt = QtWidgets.QLabel("Search Element")

        self.search_element_line_edit_wgt = QtWidgets.QLineEdit()
        self.search_element_line_edit_wgt.setPlaceholderText("enter your query here")
        self.search_element_line_edit_wgt.textEdited.connect(self.query_changed_event_handler)
    # fmt: on

    @QtCore.Slot()
    def query_changed_event_handler(self):
        print("📣 SelectElementWidget.query_changed_event_handler")
        # 根据输入的内容，搜索 element
        query = self.search_element_line_edit_wgt.text()
        if not query:
            query = "*"
        res = element_dataset.search(
            query,
            limit=10,
        )
        # print(res) # for debug only
        # 把搜索到的 Element 显示在界面上
        radio_wgt_list = list()
        for doc in res:
            element_id = doc["id"]
            element_name = doc["Name"]
            radio_wgt = ElementRadioButton(
                parent=self,
                display_value=gui_utils.DisplayValue(element_name, ""),
                element_id=element_id,
                element_name=element_name,
                select_element_wgt=self,
            )
            radio_wgt_list.append(radio_wgt)
        self.search_element_results_grid_lay.set_items(radio_wgt_list)

    def set_layout(self):
        # layout
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.ith_label_wgt)

        row_lay = QtWidgets.QHBoxLayout()
        row_lay.addWidget(self.search_element_label_wgt)
        row_lay.addWidget(self.search_element_line_edit_wgt)
        self.main_lay.addLayout(row_lay)

        self.search_element_results_grid_lay = ElementGridLayout()
        self.query_changed_event_handler()
        self.main_lay.addLayout(self.search_element_results_grid_lay)
