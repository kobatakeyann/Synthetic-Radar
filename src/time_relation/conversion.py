from datetime import datetime, timedelta

class PaddingDate:
    def __init__(self,target_dt:datetime) -> None:
        self.year, self.month, self.day, self.hour, self.minute = (
            self.pad_with_zero(target_dt.year,4),
            self.pad_with_zero(target_dt.month,2),
            self.pad_with_zero(target_dt.day,2),
            self.pad_with_zero(target_dt.hour,2),
            self.pad_with_zero(target_dt.minute,2)
        )

    def pad_with_zero(self,datatime_fator:int,digit:int) -> str:
        return str(datatime_fator).zfill(digit)

def jst_to_utc(datetime) -> datetime:
    time_difference = timedelta(hours=9)
    utc_dt = datetime - time_difference
    return utc_dt

def utc_to_jst(datetime) -> datetime:
    time_difference = timedelta(hours=9)
    jst_dt = datetime + time_difference
    return jst_dt 

