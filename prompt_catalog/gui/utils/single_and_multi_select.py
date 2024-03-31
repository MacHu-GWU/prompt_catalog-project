# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from PySide6 import QtCore, QtWidgets


@dataclasses.dataclass
class DisplayValue:
    """
    在 GUI 中经常会有一些 Widget 用于显示某个值, 但是实际上参与运算的是另一个值.

    例如 Ratio Button 中用于显示一个 Label, 例如是一个 Status (Pending, In progress, Complete).
    当你选中这个 Ratio Button 的时候参与计算的值却是 Status Code, 也就是 1, 2, 3 ...

    :param label: 用于在 GUI 中显示.
    :param value: 参与计算时所用到的值.
    """

    label: str
    value: str


class RadioButton(QtWidgets.QRadioButton):
    """
    用于单选的 radio button. 通常多个 radio button 会合并成一个逻辑上的 Group. 当你选中
     其中一个 button 时, 其他的 button 会自动被取消选中.

    :param parent: 父级 widget.
    :param display_value: 用于显示的值, 参见 :class:`DisplayValue`.
    :param connect_toggled_signal: 默认为 True, 如果为 False, 则不会连接 toggled signal.

    Reference:

    - https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QRadioButton.html
    """

    def __init__(
        self,
        parent,
        display_value: DisplayValue,
        connect_toggled_signal: bool = True,
    ):
        super().__init__(display_value.label, parent)
        self.display_value = display_value
        self.toggled_event_signal_on = True
        if connect_toggled_signal:
            self.toggled.connect(self._toggled_event_handler)

    @QtCore.Slot()
    def _toggled_event_handler(self):
        """
        内部方法.
        """
        if self.toggled_event_signal_on is False:
            return
        if self.isChecked():
            print("📣 RadioButton.toggled_event_handler")
            self.toggled_event_handler()

    def toggled_event_handler(self):
        """
        当 RadioButton 被选中时会调用这个方法 (被取消时不会), 你可以在这里实现你的自定义逻辑.
        """
        raise NotImplementedError()

    def set_state(
        self,
        checked: bool,
        toggled_event_signal_on: bool = True,
    ):
        """
        设置 toggled 的状态, 并且可以选择是否发送 toggled event signal.

        :param checked: True 为选中, False 为取消
        :param toggled_event_signal_on: 默认为 True; 如果为 False, 则该次设置
            Ratio state 的时候会使得 :meth:`RadioButton.toggle_event_handler` 不会被调用.
        """
        if toggled_event_signal_on is False:  # 临时关闭 signal
            self.toggled_event_signal_on = False
        self.setChecked(checked)
        if toggled_event_signal_on is False:  # 重新打开 signal
            self.toggled_event_signal_on = True


class CheckBox(QtWidgets.QCheckBox):
    """
    用于多选的 checkbox.

    Reference:

    - https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QCheckBox.html
    """

    def __init__(
        self,
        parent,
        display_value: DisplayValue,
        connect_state_changed_signal: bool = True,
    ):
        super().__init__(display_value.label, parent)
        self.display_value = display_value
        self.state_change_event_signal_on = True
        if connect_state_changed_signal:
            self.stateChanged.connect(self.state_changed_event_handler)

    @QtCore.Slot()
    def _state_changed_event_handler(self):
        """
        内部方法.
        """
        if self.state_change_event_signal_on:
            print("📣 CheckBox.state_changed_event_handler")
            self.state_changed_event_handler()

    def state_changed_event_handler(self):
        """
        当 CheckBox 的状态发生变化时会调用这个方法, 你可以在这里实现你的自定义逻辑.
        """
        raise NotImplementedError

    def set_state(
        self,
        checked: bool,
        state_change_event_signal_on: bool = True,
    ):
        """
        设置 checkbox 的状态, 并且可以选择是否发送 state change event signal.

        :param checked: True 为选中, False 为取消
        :param state_change_event_signal_on: 默认为 True; 如果为 False, 则该次改变
            check state 的时候会使得 :meth:`CheckBox.state_changed_event_handler` 不会被调用.

        """
        if state_change_event_signal_on is False:  # 临时关闭 signal
            self.state_change_event_signal_on = False
        if checked:
            self.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.setCheckState(QtCore.Qt.CheckState.Unchecked)
        if state_change_event_signal_on is False:  # 重新打开 signal
            self.state_change_event_signal_on = True


def update_delimited_list(
    text: str,
    item: str,
    add_item: bool,
    delimiter: str = ", ",
) -> str:
    """
    更新一个以 delimiter 分隔的字符串, 你可以选择添加或者删除 item.

    :param text: 以 delimiter 分隔的字符串. 例如 "alice, bob, charlie",
        也可以是 "alice,bob,charlie" (中间没有空格).
    :param item: 你要添加或者删除的 item. 例如 "david".
    :param add_item: True 为添加, False 为删除. 注意, 添加的时候只会添加一次,
        而如果这个 item 在 text 中出现了多次, 则只会删除一次.
    :param delimiter: 默认为 ", ". 最终的 text 会用这个 delimiter 连接.
        为了好看, 这个 delimiter 一般是一个字符加一个空格. 例如 ", " 或者 "& ".
    """
    raw_delimiter = delimiter.strip()
    items = [v.strip() for v in text.split(raw_delimiter) if v.strip()]
    if add_item:
        if item not in items:
            items.append(item)
    else:
        if item in items:
            items.remove(item)
    return delimiter.join(items)
