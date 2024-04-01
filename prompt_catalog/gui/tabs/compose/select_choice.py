# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import typing as T

from whoosh.query import And, Term
from PySide6 import QtWidgets, QtCore

from ...utils import api as gui_utils
from ....fts import element_choice_dataset

if T.TYPE_CHECKING:  # pragma: no cover
    from .select_element import SelectElementWidget
    from .one_element import OneElementScrollAreaContentWidget
    from .main import ComposeScrollAreaContentWidget


class ChoiceRadioButton(gui_utils.RadioButton):
    """
    todo: add docstring
    """

    def __init__(
        self,
        parent,
        display_value: gui_utils.DisplayValue,
        choice_body: str,
        select_choice_wgt: "SelectChoiceWidget",
    ):
        super().__init__(parent=parent, display_value=display_value)
        self.choice_body = choice_body
        self.select_choice_wgt = select_choice_wgt

    # fmt: off
    def toggled_event_handler(self):
        print("📣 ChoiceRadioButton.toggled_event_handler")
        self.select_choice_wgt.search_choice_line_edit_wgt.setText(self.display_value.label)
        self.select_choice_wgt.selected_choice_body = self.choice_body
        self.select_choice_wgt.search_choice_browser_wgt.setText(self.choice_body)

        # 更新最终的 prompt
        one_element_scroll_area_content_wgt: "OneElementScrollAreaContentWidget" = self.select_choice_wgt.parent()
        compose_scroll_area_content_wgt: "ComposeScrollAreaContentWidget" = one_element_scroll_area_content_wgt.compose_scroll_area_content_wgt
        prompt = compose_scroll_area_content_wgt.generate_prompt()
        compose_scroll_area_content_wgt.prompt_wgt.setText(prompt)
    # fmt: on


class ChoiceGridLayout(QtWidgets.QGridLayout):
    """
    todo: add docstring
    """

    def __init__(
        self,
        *args,
        item_per_row: int = 1,
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


class SelectChoiceWidget(QtWidgets.QWidget):
    """
    todo: add docstring
    """

    def __init__(
        self,
        parent,
        select_element_wgt: "SelectElementWidget",
    ):
        super().__init__(parent)
        self.select_element_wgt = select_element_wgt
        self.selected_choice_body: T.Optional[str] = None

        self.set_widget()
        self.set_layout()

    def set_widget(self):
        self.search_choice_label_wgt = QtWidgets.QLabel("Search Choice")

        self.search_choice_line_edit_wgt = QtWidgets.QLineEdit()
        self.search_choice_line_edit_wgt.setPlaceholderText("Search Choice")
        self.search_choice_line_edit_wgt.textEdited.connect(
            self.query_changed_event_handler
        )

        self.search_choice_browser_wgt = QtWidgets.QTextBrowser()

    @QtCore.Slot()
    def query_changed_event_handler(self):
        print("📣 SelectChoiceWidget.query_changed_event_handler")
        # 根据输入的内容，搜索 element choice
        query = self.search_choice_line_edit_wgt.text()
        if not query:
            query = "*"
        query = element_choice_dataset._parse_query(query)
        query = And(
            [
                query,
                Term(
                    fieldname="Element",
                    text=self.select_element_wgt.selected_element_id,
                ),
            ]
        )
        res = element_choice_dataset.search(
            query,
            limit=10,
        )
        # print(res) # for debug only
        # 把搜索到的 Element choice 显示在界面上
        radio_wgt_list = list()
        for doc in res:
            choice_name = doc["Name"]
            choice_body = doc["Body"]
            radio_wgt = ChoiceRadioButton(
                parent=self,
                display_value=gui_utils.DisplayValue(choice_name, ""),
                choice_body=choice_body,
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
