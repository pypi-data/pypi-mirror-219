from PySide6.QtGui import QPixmap, QIcon, QImage
from PySide6.QtCore import QSize, QBuffer, QIODevice
from loguru import logger
import base64
import os

from .size import Size


class Icon:
    icon_t: type = QIcon | str | bytes
    size_t: type = QSize | Size | tuple[int, int] | None

    root = os.path.join(os.path.dirname(__file__), os.path.pardir, '.assets', 'icons')
    __icon: QIcon = None
    __size: QSize = None

    def __init__(self, instance: icon_t, size: size_t = None):
        self.icon = instance
        if size:
            self.size = size

    @property
    def icon(self) -> QIcon:
        return self.__icon

    @property
    def size(self) -> QSize:
        return self.__size

    @icon.setter
    def icon(self, instance: icon_t) -> None:
        """

        :param instance: QIcon, string filename with already set Icon.root, icon bytes
        :return:
        """
        def from_bytes(icon_bytes: bytes):
            pixmap = QPixmap()
            png = base64.b64encode(icon_bytes).decode('utf-8')
            pixmap.loadFromData(base64.b64decode(png))
            self.__icon = QIcon(pixmap)

        if isinstance(instance, QIcon):  # directly set
            self.__icon = instance
        elif isinstance(instance, str):  # might be `paths` or `str(bytes)`
            if os.path.exists(filepath := os.path.join(os.path.abspath(self.root), instance)):
                self.__icon = QIcon(filepath)
            else:
                try:  # handle `eval(intance)` for case if instance is invalid `path`
                    if isinstance((icon_bytes := eval(instance)), bytes):
                        from_bytes(icon_bytes)
                except Exception:
                    self.__icon = QIcon()
                    # logger.warning(f'{instance=} is invalid path')
        elif isinstance(instance, bytes):
            from_bytes(instance)
        else:
            self.__icon = QIcon()
            # logger.warning(f'unknown type ({type(instance)}) of instance ({instance}), can not set Icon.icon')
        self.icon.addPixmap(self.__icon.pixmap(1000), mode=QIcon.Disabled)  # fix of `QPushButton.setDisabled()`

    @size.setter
    def size(self, size: size_t) -> None:
        """

        :param size: QSize, qcontextapi.Size, tuple[int, int]
        :return:
        """
        if isinstance(size, tuple):
            self.__size = QSize(*size)
        elif isinstance(size, Size):
            self.__size = QSize(*size.size)
        elif isinstance(size, QSize):
            self.__size = size
        else:
            raise AttributeError(f'unknown type ({type(size)}) of size ({size}), can not set Icon.size')

    def adjusted(self, icon: icon_t = None, size: size_t = None) -> 'Icon':
        if not icon and not size:
            logger.info('Icon.adjusted() called without parameters. Redundant call.')
        if icon:
            self.icon = icon
        if size:
            self.size = size
        return self

    @staticmethod
    def bytes(icon: icon_t, size: size_t = None) -> bytes:
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        Icon(icon, size).icon.pixmap(QSize(512, 512)).save(buffer, 'JPG')
        buffer.close()
        return bytes(buffer.data())

    @classmethod
    def default(cls) -> 'Icon':
        return Icon(instance=QIcon())
