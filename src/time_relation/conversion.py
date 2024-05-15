from datetime import datetime, timedelta

def split_datetime(target_dt) -> tuple:
    year = str(target_dt.year).zfill(4)
    month = str(target_dt.month).zfill(2)
    day = str(target_dt.day).zfill(2)
    hour = str(target_dt.hour).zfill(2)
    minute = str(target_dt.minute).zfill(2)
    return year,month,day,hour,minute

def jst_to_utc(jst_datetime) -> datetime:
    time_difference = timedelta(hours=9)
    utc_datetime = jst_datetime - time_difference
    return utc_datetime 

def utc_to_jst(utc_datetime) -> datetime:
    time_difference = timedelta(hours=9)
    jst_datetime = utc_datetime + time_difference
    return jst_datetime 

