# -*- coding: utf-8 -*-

"""
"""

import typing as T

from whoosh.query import And, Term
from PySide6 import QtWidgets, QtCore

from ...utils import api as gui_utils
from ....fts import element_choice_dataset

if T.TYPE_CHECKING:
    from .select_element import SelectElementWidget


class ChoiceRadioButton(gui_utils.RadioButton):
    def __init__(
        self,
        parent,
        display_value: gui_utils.DisplayValue,
        select_choice_wgt: "SelectChoiceWidget",
    ):
        super().__init__(parent=parent, display_value=display_value)
        self.select_choice_wgt = select_choice_wgt

    def toggled_event_handler(self):
        print("📣 ChoiceRadioButton.toggled_event_handler")
        self.select_choice_wgt.search_choice_line_edit_wgt.setText(
            self.display_value.label
        )
        self.select_choice_wgt.search_choice_line_edit_wgt._choice_id = (
            self.display_value.value
        )
        self.select_choice_wgt.search_choice_browser_wgt.setText(
            self.display_value.value
        )


class ChoiceGridLayout(QtWidgets.QGridLayout):
    def __init__(
        self,
        *args,
        item_per_row: int = 1,
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


class SelectChoiceWidget(QtWidgets.QWidget):
    """ """

    def __init__(
        self,
        parent,
        select_element_wgt: "SelectElementWidget",
    ):
        super().__init__(parent)
        self.select_element_wgt = select_element_wgt

        self.set_widget()
        self.set_layout()

    def set_widget(self):
        self.search_choice_label_wgt = QtWidgets.QLabel("Search Choice")

        self.search_choice_line_edit_wgt = QtWidgets.QLineEdit()
        self.search_choice_line_edit_wgt.setPlaceholderText("Search Choice")
        self.search_choice_line_edit_wgt.textEdited.connect(
            self.query_changed_event_handler
        )
        self.search_choice_line_edit_wgt._choice_id = None
        self.search_choice_line_edit_wgt._choice_body = None

        self.search_choice_browser_wgt = QtWidgets.QTextBrowser()

    @QtCore.Slot()
    def query_changed_event_handler(self):
        print("📣 SelectChoiceWidget.query_changed_event_handler")
        query = self.search_choice_line_edit_wgt.text()
        if not query:
            query = "*"
        query = element_choice_dataset._parse_query(query)
        element_id = self.select_element_wgt.search_element_line_edit_wgt._element_id
        query = And([query, Term("Element", element_id)])
        res = element_choice_dataset.search(
            query,
            limit=10,
        )
        # print(res) # for debug only
        radio_wgt_list = list()
        for doc in res:
            label = doc["Name"]
            value = doc["Body"]
            radio_wgt = ChoiceRadioButton(
                parent=self,
                display_value=gui_utils.DisplayValue(label, value),
                select_choice_wgt=self,
            )
            radio_wgt_list.append(radio_wgt)
        self.search_choice_results_grid_lay.set_items(radio_wgt_list)

    def set_layout(self):
        # layout
        self.main_lay = QtWidgets.QVBoxLayout()
        row_lay = QtWidgets.QHBoxLayout()
        row_lay.addWidget(self.search_choice_label_wgt)
        row_lay.addWidget(self.search_choice_line_edit_wgt)
        self.main_lay.addLayout(row_lay)

        row_lay = QtWidgets.QHBoxLayout()
        self.search_choice_results_grid_lay = ChoiceGridLayout()
        row_lay.addLayout(self.search_choice_results_grid_lay)
        row_lay.addWidget(self.search_choice_browser_wgt)
        self.main_lay.addLayout(row_lay)
