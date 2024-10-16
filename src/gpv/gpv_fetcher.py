from datetime import datetime
from tempfile import NamedTemporaryFile

from nakametpy.jma import load_jmara_grib2
from numpy.ma import MaskedArray

from api.data_fetcher import fetch_data
from helper.time import PaddingDatetime


def get_jma_gpv(utc_datetime: datetime) -> MaskedArray:
    """
    Return an array of synthetic radar grid point value.
    """
    target_datetime = PaddingDatetime(utc_datetime)
    year, month, day, hour, minute = (
        target_datetime.year,
        target_datetime.month,
        target_datetime.day,
        target_datetime.hour,
        target_datetime.minute,
    )
    base_url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/{year}/{month}/{day}"
    if utc_datetime <= datetime(2024, 2, 29, 14, 0):
        filename = f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV__grib2.tar"
        is_tar = True
        time_resolution = 10
    else:
        filename = f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr05lv_ANAL_grib2.bin"
        is_tar = False
        time_resolution = 5
    end_point = f"{base_url}/{filename}"
    res_data = fetch_data(end_point)
    # Due to the nature of the library, data cannot be retrieved without writing to a file.
    with NamedTemporaryFile(mode="wb") as f:
        f.write(res_data)
        gpv_array: MaskedArray = load_jmara_grib2(
            file=f.name,
            tar_flag=is_tar,
            tar_contentname=f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr{str(time_resolution).zfill(2)}lv_ANAL_grib2.bin",
        )
    return gpv_array
