from PySide6.QtWidgets import QDateTimeEdit
from datetime import datetime, timezone

from ..context import ContextObj
from ..types import Parent, QSS


class DateTime(ContextObj, QDateTimeEdit):
    format: str = '%d.%m.%Y %H:%M'

    def __init__(
            self, parent: Parent, name: str, visible: bool = True, qss: QSS = None,
            *,
            calendar: bool = True
    ):
        QDateTimeEdit.__init__(self, datetime.now(), parent, calendarPopup=calendar)
        ContextObj.__init__(self, parent, name, visible)
        self.qss = qss

    async def init(
            self, *,
            format: str = 'dd.MM.yyyy hh:mm',
            **kwargs
    ) -> 'DateTime':
        self.setDisplayFormat(format)
        return await self._render(**kwargs)

    def dateTime(self, tz: bool = False) -> datetime:
        dt = super().dateTime().toPython()
        dt.replace(tzinfo=timezone.utc if tz else None)
        return dt
