"""
Модуль с вспомогательными функциями для формирования времени datetime.
"""

from datetime import (
    datetime,
    timezone,
)
from zoneinfo import ZoneInfo


def datetime_convert_to_local(
    dt_utc: datetime,
    tz_name: str = "Europe/Moscow",
    str_convert: bool = False,
    str_format: str | None = "%Y-%m-%d %H:%M",
) -> datetime | str:
    """
    Конвертирует UTC datetime в указанный часовой пояс (ZoneInfo).

    Например:
        - на входе было "2025-01-01 12:30:00.123456+00:00" | "UTC"
        - на выходе будет "2025-02-26 15:30:00.123456+03:00" | "Europe/Moscow"

    Временные зоны ZoneInfo для РФ:
        UTC+0   'UTC'
        UTC+2:  'Europe/Kaliningrad'
        UTC+3:  'Europe/Moscow'
        UTC+4:  'Europe/Samara'
        UTC+5:  'Asia/Yekaterinburg'
        UTC+6:  'Asia/Omsk'
        UTC+7:  'Asia/Krasnoyarsk'
        UTC+8:  'Asia/Irkutsk'
        UTC+9:  'Asia/Yakutsk'
        UTC+10: 'Asia/Vladivostok'
        UTC+11: 'Asia/Magadan'
        UTC+12: 'Asia/Kamchatka'
    """
    dt_local: datetime = dt_utc.astimezone(tz_name)
    if str_convert:
        return dt_local.strftime(str_format)
    return dt_local


def datetime_from_str(
    dt_str: str,
    dt_tz_name: str,
    str_format: str = "%Y-%m-%d %H:%M:%S",
) -> datetime:
    """Конвертирует строковое представление даты и времени в объект datetime."""
    return (
        datetime
        .strptime(dt_str, str_format)
        .replace(tzinfo=ZoneInfo(dt_tz_name))
        .astimezone(ZoneInfo("UTC"))
    )


def datetime_now_utc(
    str_convert: bool = False,
    str_format: str | None = "%Y-%m-%d %H:%M",
) -> datetime | str:
    """Возвращает объект datetime.now() с часовым поясом UTC."""
    value: datetime = datetime.now(timezone.utc)
    if str_convert:
        value: str = value.strftime(str_format)
    return value
