# -*- coding: utf-8 -*-

"""
"""

from PySide6 import QtWidgets, QtCore

from .select_element import SelectElementWidget
from .select_choice import SelectChoiceWidget


class OneElementScrollAreaContentWidget(QtWidgets.QWidget):
    """ """

    def __init__(
        self,
        parent,
        ith: int,
    ):
        super().__init__(parent)
        self.ith = ith

        # widget
        self.select_element_wgt = SelectElementWidget(self, ith=self.ith, select_choice_wgt=None)
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
    ):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.main_wgt = OneElementScrollAreaContentWidget(self, ith=ith)
        self.setWidget(self.main_wgt)
