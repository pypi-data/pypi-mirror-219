from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon
from typing import Callable, Awaitable

from ..button import Button
from ...types import Icon
from ...asynq import asyncSlot


class StateButton(Button):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True, state: bool = False):
        super().__init__(parent, name if name else self.__class__.__name__, visible)
        self.__state: bool = state
        self.icon_true: Icon = Icon('star-fill.svg', (30, 30))
        self.icon_false: Icon = Icon('star.svg', (30, 30))

    async def init(
            self, *,
            icon_true: Icon = None, icon_false: Icon = None, event: Callable[..., bool],
            **kwargs
    ) -> 'StateButton':
        self.icon_true = icon_true or self.icon_true
        self.icon_false = icon_false or self.icon_false
        self.state = False
        return await super().init(on_click=lambda: self.__event(event), **kwargs)

    @asyncSlot()
    async def __event(self, event: Callable[..., Awaitable[bool]]) -> None:
        if await event():
            self.state = not self.state

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        if state:
            self.setIcon(self.icon_true.icon)
            self.setIconSize(self.icon_true.size)
        else:
            self.setIcon(self.icon_false.icon)
            self.setIconSize(self.icon_false.size)
        self.__state = state
