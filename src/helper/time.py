from datetime import datetime, timedelta


class PaddingDatetime:
    def __init__(self, target_dt: datetime) -> None:
        self.year, self.month, self.day, self.hour, self.minute = (
            self.pad_with_zero(target_dt.year, 4),
            self.pad_with_zero(target_dt.month, 2),
            self.pad_with_zero(target_dt.day, 2),
            self.pad_with_zero(target_dt.hour, 2),
            self.pad_with_zero(target_dt.minute, 2),
        )

    def pad_with_zero(self, datatime_factor: int, digit: int) -> str:
        return str(datatime_factor).zfill(digit)


def jst_to_utc(jst_dt) -> datetime:
    TIME_DIFFERENCE = 9
    difference = timedelta(hours=TIME_DIFFERENCE)
    utc_dt = jst_dt - difference
    return utc_dt
