# -*- coding: utf-8 -*-

"""
"""

import typing as T

from PySide6 import QtWidgets, QtCore

from ...utils import api as gui_utils
from ....fts import element_dataset, element_choice_dataset

if T.TYPE_CHECKING:
    from .select_choice import SelectChoiceWidget


class ElementRadioButton(gui_utils.RadioButton):
    def __init__(
        self,
        parent,
        display_value: gui_utils.DisplayValue,
        select_element_wgt: "SelectElementWidget",
    ):
        super().__init__(parent=parent, display_value=display_value)
        self.select_element_wgt = select_element_wgt

    def toggled_event_handler(self):
        print("📣 ElementRadioButton.toggled_event_handler")
        self.select_element_wgt.search_element_line_edit_wgt.setText(
            self.display_value.label
        )
        self.select_element_wgt.search_element_line_edit_wgt._element_id = (
            self.display_value.value
        )
        self.select_element_wgt.select_choice_wgt.query_changed_event_handler()


class ElementGridLayout(QtWidgets.QGridLayout):
    def __init__(
        self,
        *args,
        item_per_row: int = 5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.item_per_row = item_per_row
        self.radio_wgt_list: list[QtWidgets.QRadioButton] = list()

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


class SelectElementWidget(QtWidgets.QWidget):
    """ """

    def __init__(
        self,
        parent,
        ith: int,
        select_choice_wgt: "SelectChoiceWidget",
    ):
        super().__init__(parent)
        self.ith = ith
        self.select_choice_wgt = select_choice_wgt

        self.set_widget()
        self.set_layout()

    def set_widget(self):
        self.ith_label_wgt = QtWidgets.QLabel(f"Element {self.ith}")
        self.ith_label_wgt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.search_element_label_wgt = QtWidgets.QLabel("Search Element")

        self.search_element_line_edit_wgt = QtWidgets.QLineEdit()
        self.search_element_line_edit_wgt.setPlaceholderText("Search Element")
        self.search_element_line_edit_wgt.textEdited.connect(
            self.query_changed_event_handler
        )
        self.search_element_line_edit_wgt._element_id = "NA"

    @QtCore.Slot()
    def query_changed_event_handler(self):
        print("📣 SelectElementWidget.query_changed_event_handler")
        query = self.search_element_line_edit_wgt.text()
        if not query:
            query = "*"
        res = element_dataset.search(
            query,
            limit=10,
        )
        # print(res) # for debug only
        radio_wgt_list = list()
        for doc in res:
            label = doc["Name"]
            value = doc["id"]
            radio_wgt = ElementRadioButton(
                parent=self,
                display_value=gui_utils.DisplayValue(label, value),
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
