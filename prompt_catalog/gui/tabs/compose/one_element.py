# -*- coding: utf-8 -*-

"""
"""

import typing as T

from PySide6 import QtWidgets, QtCore

from .select_element import SelectElementWidget
from .select_choice import SelectChoiceWidget

if T.TYPE_CHECKING:
    from .main import ComposeScrollAreaContentWidget


class OneElementScrollAreaContentWidget(QtWidgets.QWidget):
    """ """

    def __init__(
        self,
        parent,
        ith: int,
        compose_scroll_area_content_wgt: "ComposeScrollAreaContentWidget",
    ):
        super().__init__(parent)
        self.ith = ith
        self.compose_scroll_area_content_wgt = compose_scroll_area_content_wgt

        # widget
        self.select_element_wgt = SelectElementWidget(
            self,
            ith=self.ith,
            select_choice_wgt=None,
        )
        self.select_choice_wgt = SelectChoiceWidget(
            self,
            select_element_wgt=self.select_element_wgt,
        )
        self.select_element_wgt.select_choice_wgt = self.select_choice_wgt

        # layout
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addLayout(self.select_element_wgt.main_lay)
        self.main_lay.addLayout(self.select_choice_wgt.main_lay)

        self.setLayout(self.main_lay)


class OneElementScrollAreaWidget(QtWidgets.QScrollArea):
    """ """

    def __init__(
        self,
        parent,
        ith: int,
        compose_scroll_area_content_wgt: "ComposeScrollAreaContentWidget",
    ):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.main_wgt = OneElementScrollAreaContentWidget(
            self,
            ith=ith,
            compose_scroll_area_content_wgt=compose_scroll_area_content_wgt,
        )
        self.setWidget(self.main_wgt)
