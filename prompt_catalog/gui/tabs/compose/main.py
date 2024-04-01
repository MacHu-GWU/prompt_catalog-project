# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

from PySide6 import QtWidgets, QtCore

from .one_element import OneElementScrollAreaWidget


class ComposeScrollAreaContentWidget(QtWidgets.QWidget):
    """
    todo: add docstring
    """

    def __init__(self, parent):
        super().__init__(parent)
        # widget
        self.one_element_scroll_area_wgt_list = list()
        for ith in range(1, 1 + 5):
            one_element_scroll_area_wgt = OneElementScrollAreaWidget(
                self,
                ith=ith,
                compose_scroll_area_content_wgt=self,
            )
            self.one_element_scroll_area_wgt_list.append(one_element_scroll_area_wgt)

        self.prompt_wgt = QtWidgets.QTextBrowser()

        # layout
        self.main_lay = QtWidgets.QHBoxLayout()

        self.element_list_lay = QtWidgets.QVBoxLayout()
        for one_element_scroll_area_wgt in self.one_element_scroll_area_wgt_list:
            self.element_list_lay.addWidget(one_element_scroll_area_wgt)

        self.main_lay.addLayout(self.element_list_lay)
        self.main_lay.addWidget(self.prompt_wgt)

        self.setLayout(self.main_lay)

    # fmt: off
    def generate_prompt(self) -> str:
        lines = list()

        for one_element_scroll_area_wgt in self.one_element_scroll_area_wgt_list:
            element_name = one_element_scroll_area_wgt.main_wgt.select_element_wgt.search_element_line_edit_wgt.text()
            if not (element_name):
                continue
            choice_body = one_element_scroll_area_wgt.main_wgt.select_choice_wgt.search_choice_browser_wgt.toPlainText()
            if not (choice_body):
                continue
            lines.append(f"# {element_name}\n")
            lines.append(choice_body + "\n")

        return "\n".join(lines)
    # fmt: on


class ComposeScrollAreaWidget(QtWidgets.QScrollArea):
    """
    .. seealso::

        https://github.com/MacHu-GWU/video_search-project/blob/main/docs/source/02-GUI/02-Data-Entry-Tab/index.rst#ui
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.main_wgt = ComposeScrollAreaContentWidget(self)
        self.setWidget(self.main_wgt)
