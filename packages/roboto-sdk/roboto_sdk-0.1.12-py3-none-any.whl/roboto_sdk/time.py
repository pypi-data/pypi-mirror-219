import datetime


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
