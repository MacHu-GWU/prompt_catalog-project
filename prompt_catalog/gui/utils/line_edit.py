# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore


class LineEdit(QtWidgets.QLineEdit):
    """
    代表一个 Line Edit Widget. 里面的文本如果发生变化, 通常会触发一个信号.

    :param parent: 父级 widget.
    :param connect_text_changed_signal: 默认为 True, 如果为 False, 则不会连接 text changed signal.
    """

    def __init__(
        self,
        parent,
        connect_text_changed_signal: bool = True,
    ):
        super().__init__(parent)
        self.text_change_signal_on = True
        if connect_text_changed_signal:
            self.textChanged.connect(self._text_changed_event_handler)

    @QtCore.Slot()
    def _text_changed_event_handler(self):
        """
        内部方法.
        """
        if self.text_change_signal_on:
            print("📣 LineEdit.text_changed_event_handler")
            self.text_changed_event_handler()

    def text_changed_event_handler(self):
        """
        当输入框的内容发生变化时会调用这个方法, 你可以在这里实现你的自定义逻辑.
        """
        raise NotImplementedError

    def set_text(
        self,
        text: str,
        text_change_signal_on: bool = True,
    ):
        if text_change_signal_on is False:  # 临时关闭 signal
            self.text_change_signal_on = False
        self.setText(text)
        if text_change_signal_on is False:  # 重新打开 signal
            self.text_change_signal_on = True
