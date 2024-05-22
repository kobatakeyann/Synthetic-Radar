from datetime import datetime, timedelta


class Date:
    def __init__(self,target_dt):
        self.target_dt = target_dt
        self.year = str(target_dt.year).zfill(4)
        self.month = str(target_dt.month).zfill(2)
        self.day = str(target_dt.day).zfill(2)
        self.hour = str(target_dt.hour).zfill(2)
        self.minute = str(target_dt.minute).zfill(2)

    def jst_to_utc(self) -> datetime:
        time_difference = timedelta(hours=9)
        self.utc_dt = self.target_dt - time_difference
        return self.utc_dt 

    def utc_to_jst(self) -> datetime:
        time_difference = timedelta(hours=9)
        self.jst_dt = self.target_dt + time_difference
        return self.jst_dt 

