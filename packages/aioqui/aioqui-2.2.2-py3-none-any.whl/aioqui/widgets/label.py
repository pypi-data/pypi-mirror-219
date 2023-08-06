from PySide6.QtGui import QFontMetrics, QPaintEvent
from PySide6.QtWidgets import QLabel

from ..types import Parent, QSS, Alignment, ElideMode, SizePolicy
from ..context import ContextObj


class Label(ContextObj, Alignment, SizePolicy, ElideMode, QLabel):
    __elide_mode: ElideMode.ElideMode
    __pre_elilded_text: str = None

    def __init__(self, parent: Parent, name: str, visible: bool = True, qss: QSS = None):
        QLabel.__init__(self, parent)
        ContextObj.__init__(self, parent, name, visible)
        self.qss = qss

    async def init(
            self, *,
            wrap: bool = False, elide: ElideMode.ElideMode = None,
            **kwargs
    ) -> 'Label':
        self.__elide_mode = elide
        self.setWordWrap(wrap)
        return await self._render(**kwargs)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.is_elided:
            text = self.__pre_elilded_text
            self.setText(QFontMetrics(self.font()).elidedText(self.__pre_elilded_text, self.__elide_mode, self.width() - 10))
            self.__pre_elilded_text = text
        QLabel.paintEvent(self, event)

    @property
    def is_elided(self) -> bool:
        return self.__elide_mode is not None

    def setText(self, text: str) -> None:
        self.__pre_elilded_text = text
        QLabel.setText(self, text)
