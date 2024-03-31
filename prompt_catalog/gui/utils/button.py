# -*- coding: utf-8 -*-

import typing as T
import os
import subprocess

import pyperclip
from PySide6 import QtWidgets, QtCore

from ...exc import ProgrammingError
from ...vendor.os_platform import IS_WINDOWS

if T.TYPE_CHECKING:
    from .line_edit import LineEdit
    from .single_and_multi_select import CheckBox


class CopyButton(QtWidgets.QPushButton):
    """
    代表一个 Copy Button Widget. 点击这个按钮会将一些文本复制到剪贴板中.
    这个类是一个抽象类, 你需要继承这个类并实现 get_text 方法. 虽然在大多数情况下这个按钮是
    用来复制某个 QLabel 或 QLineEdit 中的文本, 但由于这个抽象层的存在, 你可以做任何事.

    :param parent: 父级 widget.
    :param label: Copy button 上的 label, 通常是 "Copy".
    """

    def __init__(
        self,
        parent,
        label: str,
    ):
        super().__init__(label, parent=parent)
        self.label = label
        self.clicked.connect(self.clicked_event_handler)

    def get_text(self):
        """
        从相关的 widget 中获取要复制的文本
        """
        raise NotImplementedError

    def post_copy_handler(self):
        """
        你可以在这个方法中实现一些当 Button 被点击并成功 Copy 之后的一些逻辑. 一个常用的例子是
        在复制成功之后显示一个 "Copied" 的 label, 然后 2 秒后隐藏这个 label.
        下面是一个例子:

        .. code-block:: python

            class MainWindow(QWidget):
                def __init__(self):
                    super().__init__()

                    self.copy_button = QPushButton("Copy")
                    self.copy_button.clicked.connect(self.copy_clicked)

                    self.copied_label = QLabel("Copied")
                    self.copied_label.hide()

                    layout = QVBoxLayout()
                    layout.addWidget(self.copy_button)
                    layout.addWidget(self.copied_label)

                    self.setLayout(layout)

                def copy_clicked(self):
                    self.copied_label.show()
                    QTimer.singleShot(2000, self.hide_copied_label)  # Hide the label after 2000 milliseconds (2 seconds)

                def hide_copied_label(self):
                    self.copied_label.hide()
        """
        pass

    @QtCore.Slot()
    def clicked_event_handler(self):
        print("📣 CopyButton.clicked_event_handler")
        text = self.get_text()
        if text:
            pyperclip.copy(text)
        self.post_copy_handler()


class CopyLabelButton(CopyButton):
    """
    一个能将 QLabel 中的文本复制到剪贴板的按钮.

    :param parent: 父级 widget.
    :param label: Copy button 上的 label, 通常是 "Copy".
    """

    def __init__(
        self,
        parent,
        label: str,
    ):
        super().__init__(label=label, parent=parent)
        self.label_wgt = None

    def connect_label_widget(self, label_wgt: QtWidgets.QLabel):
        """
        连接一个 QLabel widget 对象. 之所以不将其作为一个 __init__ 中的参数是因为
        你可能在创建 button 对象时, label 对象还没有被创建.

        :param label_wgt: QLabel widget 对象.
        """
        self.label_wgt = label_wgt

    def get_text(self):
        if self.label_wgt is None:
            raise ProgrammingError(
                f"You have to call {self.__class__.__name__}.connect_label_widget(label_wgt=...)"
                f"to connect a QLabel widget!"
            )
        return self.label_wgt.text()


class CopyLineEditButton(CopyButton):
    """
    一个能将 QLabel 中的文本复制到剪贴板的按钮.

    :param parent: 父级 widget.
    :param label: Copy button 上的 label, 通常是 "Copy".
    """

    def __init__(
        self,
        parent,
        label: str,
    ):
        super().__init__(label=label, parent=parent)
        self.line_edit_wgt = None

    def connect_line_edit_widget(self, line_edit_wgt: QtWidgets.QLineEdit):
        """
        连接一个 QLineEdit widget 对象. 之所以不将其作为一个 __init__ 中的参数是因为
        你可能在创建 button 对象时, line_edit 对象还没有被创建.

        :param line_edit_wgt: QLineEdit widget 对象.
        """
        self.line_edit_wgt = line_edit_wgt

    def get_text(self):
        if self.line_edit_wgt is None:
            raise ProgrammingError(
                f"You have to call {self.__class__.__name__}.connect_line_edit_widget(line_edit_wgt=...)"
                f"to connect a QLineEdit widget!"
            )
        return self.line_edit_wgt.text()


class InteractiveCopyButtonMixin:
    def reset_button_label(self: "CopyButton"):
        self.setText(self.label)

    def post_copy_handler(self: T.Union["CopyButton", "InteractiveCopyButtonMixin"]):
        self.setText(f"✅")
        # Hide the copied label after 2000 milliseconds (2 seconds)
        QtCore.QTimer.singleShot(2000, self.reset_button_label)


class InteractiveCopyLabelButton(InteractiveCopyButtonMixin, CopyLabelButton):
    """
    这个 Copy button 可以在你点击之后, 暂时显示一个 "✅" 的 label, 2 秒后隐藏.
    """

    pass


class InteractiveCopyLineEditButton(InteractiveCopyButtonMixin, CopyLineEditButton):
    """
    这个 Copy button 可以在你点击之后, 暂时显示一个 "✅" 的 label, 2 秒后隐藏.
    """

    pass


class ClearButton(QtWidgets.QPushButton):
    """
    代表一个 Clear Button Widget. 点击这个按钮会将一些文本或是其他什么东西清除.
    例如你可以实现将一个 QLineEdit 中的文本清除, 也可以实现将许多 checkbox uncheck.

    :param parent: 父级 widget.
    :param label: Clear button 上的 label, 通常是 "Clear".
    """

    def __init__(
        self,
        parent,
        label: str,
    ):
        super().__init__(label, parent=parent)
        self.clicked.connect(self.clicked_event_handler)

    def clear(self):
        """
        从相关的 widget 清除一些东西.
        """
        raise NotImplementedError

    def post_clear_handler(self):
        """
        todo
        """
        pass

    @QtCore.Slot()
    def clicked_event_handler(self):
        print("📣 ClearButton.clicked_event_handler")
        self.clear()
        self.post_clear_handler()


class ClearLineEditButton(ClearButton):
    """
    一个能将 LineEdit 中的文本清除的按钮.

    :param parent: 父级 widget.
    :param label: Clear button 上的 label, 通常是 "Clear".
    """

    def __init__(
        self,
        parent,
        label: str,
        line_edit_text_change_signal_on: bool = True,
    ):
        super().__init__(parent=parent, label=label)
        self.line_edit_text_change_signal_on = line_edit_text_change_signal_on
        self.line_edit_wgt: T.Optional["LineEdit"] = None

    def connect_line_edit_widget(self, line_edit_wgt: "LineEdit"):
        self.line_edit_wgt = line_edit_wgt

    def clear(self):
        if self.line_edit_wgt is None:
            raise ProgrammingError(
                f"You have to call {self.__class__.__name__}.connect_line_edit_widget(line_edit_wgt=...)"
                f"to connect a ``video_search.gui.utils.line_edit.LineEdit`` widget!"
            )
        self.line_edit_wgt.set_text(
            "",
            text_change_signal_on=self.line_edit_text_change_signal_on,
        )


class BatchCheckButton(QtWidgets.QPushButton):
    def __init__(
        self,
        parent,
        label: str,
    ):
        super().__init__(label, parent=parent)
        self.checkbox_wgt_list: T.Optional[list["CheckBox"]] = None
        self.clicked.connect(self.clicked_event_handler)

    def connect_many_checkbox_widgets(self, checkbox_wgt_list: T.List["CheckBox"]):
        self.checkbox_wgt_list = checkbox_wgt_list

    def post_clear_handler(self):
        """
        todo
        """
        pass

    @QtCore.Slot()
    def clicked_event_handler(self):
        print("📣 ClearButton.clicked_event_handler")
        self.clear()
        self.post_clear_handler()


class OpenFileButton(QtWidgets.QPushButton):
    """
    代表一个可以用于打开本地文件的 Button.

    :param parent: 父级 widget.
    :param label: Open File button 上的 label, 通常是 "Open".
    :param path: 要打开的文件的路径. 点击 button 后会用操作系统的默认方式打开对应的文件,
        相当于你在文件管理器中双击.
    """

    def __init__(self, parent, label: str, path: str):
        super().__init__(label, parent=parent)
        self.label = label
        self.path = path
        self.clicked.connect(self.clicked_event_handler)

    @QtCore.Slot()
    def clicked_event_handler(self):
        print("📣 OpenFileButton.clicked_event_handler")
        if IS_WINDOWS:
            # note: looks like the ["star", self.path] method is not working on Windows properly
            # os.startfile is more robust
            os.startfile(str(self.path))
            # subprocess.run(["start", self.path], shell=True)
        else:
            subprocess.run(["open", self.path])
