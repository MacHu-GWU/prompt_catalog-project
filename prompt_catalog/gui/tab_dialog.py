# -*- coding: utf-8 -*-


from PySide6 import QtWidgets

from .tabs.compose.api import ComposeScrollAreaWidget
# from .tabs.search.api import SearchScrollAreaWidget


class TabDialog(QtWidgets.QDialog):
    """
    这是我们主要的 Widget, 它包含了多个 Tab.

    每个 Tab 本身是一个子 Widget.

    Reference:

    - https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html
    """

    def __init__(self, parent: QtWidgets.QWidget = None):
        # based on the official doc, QDialog should not use parent,
        # it is always top level widget
        super().__init__(parent)
        self.tag_wgt = QtWidgets.QTabWidget()

        self.compose_scroll_area_wgt = ComposeScrollAreaWidget(self)
        self.tag_wgt.addTab(self.compose_scroll_area_wgt, "Compose")

        # 这个 Widget 只有一个 Layout, 用于放置 Tab
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.tag_wgt)
        self.setLayout(self.main_layout)
