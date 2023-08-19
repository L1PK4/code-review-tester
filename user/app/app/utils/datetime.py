import datetime
from typing import Any


def adapt_datetime(obj: Any) -> datetime.datetime:
    if isinstance(obj, datetime.datetime):
        dt = obj
    elif isinstance(obj, datetime.time):
        dt = datetime.datetime(
            year=0,
            month=0,
            day=0,
            hour=obj.hour,
            minute=obj.minute,
            second=obj.second,
            tzinfo=obj.tzinfo
        )
    elif isinstance(obj, datetime.date):
        dt = datetime.datetime(
            year=obj.year,
            month=obj.month,
            day=obj.day,
            hour=0,
            minute=0,
            second=0
        )
    else:
        dt = datetime.datetime(
            year=getattr(obj, 'year', 0),
            month=getattr(obj, 'month', 0),
            day=getattr(obj, 'day', 0),
            hour=getattr(obj, 'hour', 0),
            minute=getattr(obj, 'minute', 0),
            second=getattr(obj, 'second', 0),
            tzinfo=getattr(obj, 'tzinfo', None)
        )

    return dt


def to_unix_timestamp(d: Any) -> int | None:

    """
    Конвертирует любой время подобный объект в unix-метку

    :param d: время подобный объект. Это может быть `None`, `int`, `float` или объект, у которого есть поля `day`,
    `month`, `year`, `hour`, `minute` или `second`
    :return: unix-метка или `None`. Значение `None` возвращается только для аргумента `None`
    """

    if d is None or isinstance(d, int):
        return d

    if isinstance(d, float):
        return int(d)

    dt = adapt_datetime(d)

    result = int(dt.timestamp())
    return result


def from_unix_timestamp(stamp: Any):
    
    if stamp is None or isinstance(stamp, datetime.datetime):
        return stamp

    if isinstance(stamp, float) or isinstance(stamp, int):
        return datetime.datetime.fromtimestamp(stamp)

    return adapt_datetime(stamp)

    

