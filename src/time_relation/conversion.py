import datetime

def acquire_factors_of_datetime(_datetime_) -> tuple:
    year = str(_datetime_.year).zfill(4)
    month = str(_datetime_.month).zfill(2)
    day = str(_datetime_.day).zfill(2)
    hour = str(_datetime_.hour).zfill(2)
    minute = str(_datetime_.minute).zfill(2)
    return year,month,day,hour,minute

def jst_to_utc(jst_datetime) -> datetime.datetime:
    time_difference = datetime.timedelta(hours=9)
    utc_datetime = jst_datetime - time_difference
    return utc_datetime 

def utc_to_jst(utc_datetime) -> datetime.datetime:
    time_difference = datetime.timedelta(hours=9)
    jst_datetime = utc_datetime + time_difference
    return jst_datetime 

