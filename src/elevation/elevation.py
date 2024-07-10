from datetime import datetime
from io import StringIO
from urllib.error import HTTPError

import numpy as np
import pandas as pd
from api.api_calling import fetch_data
from numpy import ndarray
from numpy.ma import MaskedArray


def get_elevation_array(
    x_upper_left: int,
    x_lower_right: int,
    y_upper_left: int,
    y_lower_right: int,
    zoom_level: int,
) -> ndarray:

    a = np.array([])
    for x in range(x_upper_left, x_lower_right + 1):
        b = np.array([])
        for y in range(y_upper_left, y_lower_right + 1):
            # 地形データを読み込む
            url = f"http://cyberjapandata.gsi.go.jp/xyz/dem/{zoom_level}/{x}/{y}.txt"
            try:
                res_data = fetch_data(url)
            except HTTPError as http_err:
                if http_err.code == 404:
                    Z = np.zeros((256, 256))
                else:
                    raise HTTPError(
                        http_err.url,
                        http_err.code,
                        http_err.reason,
                        http_err.headers,
                        http_err.fp,
                    )
            # 標高値がない点はとりあえず0mに置換する
            maptxt = res_data.read().replace("e", "0.0")
            # maptxt = response.text.replace("e", "0.0")
            Z = pd.read_csv(StringIO(maptxt), header=None)
            Z = Z.values
            if len(b) == 0:
                b = Z
            else:
                b = np.append(b, Z, 0)
        if len(a) == 0:
            a = b
        else:
            a = np.append(a, b, 1)
    return a


# response = requests.get(url)
# if response.status_code == 404:
#     # メッシュデータが無い区画は全ての点が0mのメッシュとしてとりあえず用意する
#     Z = np.zeros((256, 256))
# else:
# 標高値がない点はとりあえず0mに置換する
# maptxt = response.text.replace("e", "0.0")
# Z = pd.read_csv(StringIO(maptxt), header=None)
# Z = Z.values


def get_jma_gpv(utc_datetime: datetime) -> MaskedArray:
    """
    Return an array of synthetic radar grid point value.
    """
    url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/{year}/{month}/{day}/Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV__grib2.tar"
    res_data = fetch_data(url)
    # Due to the nature of the library, data cannot be retrieved without writing to a file.
    with NamedTemporaryFile(mode="wb") as f:
        f.write(res_data)
        gpv_array: MaskedArray = load_jmara_grib2(
            file=f.name,
            tar_flag=True,
            tar_contentname=f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin",
        )
    return gpv_array
