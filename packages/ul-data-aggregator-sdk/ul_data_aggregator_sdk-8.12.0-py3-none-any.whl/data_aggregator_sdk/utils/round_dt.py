from datetime import datetime, timedelta


def round_dt(dt: datetime, round_delta: timedelta) -> datetime:
    dt_timezone = dt.tzinfo
    dt = dt.replace(tzinfo=None)
    rounded_dt = datetime.min + round((dt - datetime.min) / round_delta) * round_delta
    return rounded_dt.replace(tzinfo=dt_timezone)
