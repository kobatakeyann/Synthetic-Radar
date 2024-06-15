from datetime import datetime
from numpy.ma import MaskedArray
from tempfile import TemporaryFile

from nakametpy.jma import load_jmara_grib2

from api.api_calling import fetch_data
from time_relation.conversion import PaddingDate


def get_jma_gpv(utc_datetime: datetime) -> MaskedArray:
    """全国合成レーダーGPVの値の配列を返す関数"""
    target_datetime = PaddingDate(utc_datetime)
    year, month, day, hour, minute = (
        target_datetime.year,
        target_datetime.month,
        target_datetime.day,
        target_datetime.hour,
        target_datetime.minute,
    )
    url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/{year}/{month}/{day}/Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV__grib2.tar"
    res_data = fetch_data(url)
    # ライブラリの特性上、ファイルに書き込みを行わないと、データを取得できない
    with TemporaryFile(mode="wb") as f:
        f.write(res_data)
        gpv_array: MaskedArray = load_jmara_grib2(
            file=f.name,
            tar_flag=True,
            tar_contentname=f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin",
        )
    return gpv_array
