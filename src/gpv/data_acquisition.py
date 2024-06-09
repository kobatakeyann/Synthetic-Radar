import os

from datetime import datetime
from numpy.ma import MaskedArray

from nakametpy.jma import load_jmara_grib2

from api.api_calling import request_to_api, read_response, write_down_res
from time_relation.conversion import PaddingDate, jst_to_utc


def load_jma_gpv(jst_datetime:datetime) -> MaskedArray:
    '''全国合成レーダーGPVの値の配列を返す関数
    '''

    # 0補完された日付文字列の取得
    utc_datetime = jst_to_utc(jst_datetime)
    target_datetime = PaddingDate(utc_datetime)
    year, month, day, hour, minute = (
        target_datetime.year,
        target_datetime.month,
        target_datetime.day,
        target_datetime.hour,
        target_datetime.minute,
    )

    # API calling
    url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/{year}/{month}/{day}/Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV__grib2.tar"
    req = request_to_api(url)
    res_data = read_response(req)
    data_file = write_down_res(res_data)

    tar_contentfile = f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    gpv_array : MaskedArray = load_jmara_grib2(data_file,tar_flag=True,tar_contentname=tar_contentfile)
    os.remove(data_file)
    return gpv_array
