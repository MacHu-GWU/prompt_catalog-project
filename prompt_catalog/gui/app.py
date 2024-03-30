# -*- coding: utf-8 -*-

import sys

from PySide6 import QtWidgets

# 创建 App 对象, 并获得屏幕尺寸
app = QtWidgets.QApplication(sys.argv)
screen_width, screen_height = app.screens()[0].size().toTuple()
