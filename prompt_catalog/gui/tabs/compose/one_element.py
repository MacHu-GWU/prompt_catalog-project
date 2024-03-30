# -*- coding: utf-8 -*-

"""
"""

from PySide6 import QtWidgets, QtCore


class OneElementScrollAreaContentWidget(QtWidgets.QWidget):
    """
    """

    def __init__(self, parent):
        super().__init__(parent)
        # widget
        # self.all_field_input_scroll_area_wgt = AllFieldInputScrollAreaWidget(self)
        # self.fts_scroll_area_wgt = FtsScrollAreaWidget(
        #     self,
        #     all_field_input_scroll_area_content_wgt=self.all_field_input_scroll_area_wgt.main_wgt,
        # )
        # self.all_tag_group_scroll_area_wgt = AllTagGroupScrollAreaWidget(
        #     self,
        #     tag_input_line_edit_wgt=self.all_field_input_scroll_area_wgt.main_wgt.tags_input_box_wgt.line_edit_wgt,
        # )

        # layout
        self.main_lay = QtWidgets.QHBoxLayout()

        # self.left_column_lay = QtWidgets.QVBoxLayout()
        # self.left_column_lay.addWidget(self.all_field_input_scroll_area_wgt)
        # self.left_column_lay.addWidget(self.fts_scroll_area_wgt)
        #
        # self.right_column_lay = QtWidgets.QVBoxLayout()
        # self.right_column_lay.addWidget(self.all_tag_group_scroll_area_wgt)
        #
        # self.main_lay.addLayout(self.left_column_lay)
        # self.main_lay.addLayout(self.right_column_lay)

        self.setLayout(self.main_lay)


class OneElementScrollAreaWidget(QtWidgets.QScrollArea):
    """
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.main_wgt = OneElementScrollAreaContentWidget(self)
        self.setWidget(self.main_wgt)
