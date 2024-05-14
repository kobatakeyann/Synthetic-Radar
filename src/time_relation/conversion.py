import datetime

def get_factors_of_datetime(target_datetime) -> tuple:
    year = str(target_datetime.year).zfill(4)
    month = str(target_datetime.month).zfill(2)
    day = str(target_datetime.day).zfill(2)
    hour = str(target_datetime.hour).zfill(2)
    minute = str(target_datetime.minute).zfill(2)
    return year,month,day,hour,minute

def jst_to_utc(jst_datetime) -> datetime.datetime:
    time_difference = datetime.timedelta(hours=9)
    utc_datetime = jst_datetime - time_difference
    return utc_datetime 

def utc_to_jst(utc_datetime) -> datetime.datetime:
    time_difference = datetime.timedelta(hours=9)
    jst_datetime = utc_datetime + time_difference
    return jst_datetime 

