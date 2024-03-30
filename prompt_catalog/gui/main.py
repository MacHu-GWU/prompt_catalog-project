# -*- coding: utf-8 -*-

# 任何面向最终用户的 app 基本上都是从命令行接入的, 所以 sys 模块是必须的
import sys

# QtCore, QtWidgets, QtGui 是 PySide 的三个主要模块, 一般每一个项目都会用到这三个模块.
# 所以我一般在开始就会 Import 它们, 不管用不用得到.
# 全部的模块列表: https://doc.qt.io/qtforpython-6/modules.html#
from PySide6 import QtCore, QtWidgets, QtGui

# from ..paths import path_icon
# from ..backup import backup_data_entry_db
# from ..settings_init import settings
# from .settings import bsm
from .app import app, screen_width, screen_height
from .tab_dialog import TabDialog


class MainWindow(QtWidgets.QMainWindow):
    """
    一般任何一个 App 都有一个主窗口. 在这个主窗口里我们可以塞下各种各样的 Widget.
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Prompt Catalog App")
        # self.add_menu()

        self.tab_dialog_wgt = TabDialog()
        self.setCentralWidget(self.tab_dialog_wgt)

    # def add_menu(self):
    #     # Create the tray
    #     self.tray = QtWidgets.QSystemTrayIcon()
    #     self.tray.setIcon(QtGui.QIcon(path_icon.abspath))
    #     self.tray.setVisible(True)
    #
    #     # Create the menu
    #     self.menu = QtWidgets.QMenu()
    #     self.file_menu = self.menu.addMenu("File")
    #
    #     self.backup_action = QtGui.QAction("Backup", self)
    #     self.backup_action.triggered.connect(self.backup)
    #     self.menu.addAction(self.backup_action)
    #
    #     self.tray.setContextMenu(self.menu)

    # @QtCore.Slot()
    # def backup(self):
    #     print("run backup")
    #     try:
    #         backup_data_entry_db(bsm=bsm, settings=settings)
    #         title = "✅ Backup success!"
    #         text = f"See {settings.s3dir_repo.console_url}"
    #     except Exception as e:
    #         print(e)
    #         title = "❌ Backup failed!"
    #         text = f"{e!r}"
    #     # Create a message box
    #     msg_box = QtWidgets.QMessageBox()
    #     msg_box.setWindowTitle(title)
    #     msg_box.setText(text)
    #
    #     # Start a timer to close the message box after 1 second
    #     timer = QtCore.QTimer()
    #     timer.setSingleShot(True)
    #     timer.timeout.connect(msg_box.close)
    #     timer.start(1000)  # 1000 milliseconds = 1 second
    #
    #     # Show the message box
    #     msg_box.exec()


def run_gui():
    # 创建主窗口, 并设置位置和大小
    main_window = MainWindow()
    main_window.setGeometry(
        int(screen_width * 0.1),  # x, at 25% of screen width
        int(screen_height * 0.1),  # y, at 25% of screen height
        int(screen_width * 0.8),  # w, 50% screen width
        int(screen_height * 0.8),  # h, 50% screen height
    )
    main_window.show()

    sys.exit(app.exec())
