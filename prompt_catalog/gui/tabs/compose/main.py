# -*- coding: utf-8 -*-

"""
"""

from PySide6 import QtWidgets, QtCore

from .one_element import OneElementScrollAreaWidget
# from .field_input_scroll_area import AllFieldInputScrollAreaWidget
# from .fts_scroll_area import FtsScrollAreaWidget
# from .tag_group_scroll_area import AllTagGroupScrollAreaWidget


class ComposeScrollAreaContentWidget(QtWidgets.QWidget):
    """
    """

    def __init__(self, parent):
        super().__init__(parent)
        # widget
        self.one_element_scroll_area_wgt_list = list()
        for _ in range(3):
            one_element_scroll_area_wgt = OneElementScrollAreaWidget(self)
            self.one_element_scroll_area_wgt_list.append(one_element_scroll_area_wgt)

        # layout
        self.main_lay = QtWidgets.QHBoxLayout()

        self.element_list_lay = QtWidgets.QVBoxLayout()
        for one_element_scroll_area_wgt in self.one_element_scroll_area_wgt_list:
            self.element_list_lay.addWidget(one_element_scroll_area_wgt)

        self.main_lay.addLayout(self.element_list_lay)

        self.setLayout(self.main_lay)


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
