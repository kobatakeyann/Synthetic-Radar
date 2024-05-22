from datetime import datetime, timedelta

class PaddingDate:
    def __init__(self,target_dt):
        self.target_dt = target_dt
        self.year = str(target_dt.year).zfill(4)
        self.month = str(target_dt.month).zfill(2)
        self.day = str(target_dt.day).zfill(2)
        self.hour = str(target_dt.hour).zfill(2)
        self.minute = str(target_dt.minute).zfill(2)

def jst_to_utc(datetime) -> datetime:
    time_difference = timedelta(hours=9)
    utc_dt = datetime - time_difference
    return utc_dt

def utc_to_jst(datetime) -> datetime:
    time_difference = timedelta(hours=9)
    jst_dt = datetime + time_difference
    return jst_dt 

