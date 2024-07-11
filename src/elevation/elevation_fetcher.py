from datetime import datetime
from io import StringIO
from urllib.error import HTTPError

import numpy as np
import pandas as pd
from api.api_calling import fetch_data
from numpy import ndarray
from numpy.ma import MaskedArray


def get_elevation_array(x: int, y: int, zoom_level: int) -> ndarray:
    """Acquire elevation array of one tile from Geographical Survey Institute.

    Args:
        x (int): x-coodinate in Tile Coordinates
        y (int): y-coodinate in Tile Coordinates
        zoom_level (int): Zoom level in Tile Coordinates

    Returns:
        ndarray: elevation array of the tile designated by coordinate(x,y)
    """
    url = f"http://cyberjapandata.gsi.go.jp/xyz/dem/{zoom_level}/{x}/{y}.txt"
    try:
        res_data = fetch_data(url)
        elevation_text = res_data.read().replace("e", "0.0")
        elevation_df = pd.read_csv(StringIO(elevation_text), header=None)
        elevation_array = elevation_df.values
    except HTTPError as http_err:
        if http_err.code == 404:
            elevation_array = np.zeros((256, 256))
        else:
            raise HTTPError(
                http_err.url,
                http_err.code,
                http_err.reason,
                http_err.headers,
                http_err.fp,
            )
    return elevation_array


def get_concatted_array(
    x_upper_left: int,
    x_lower_right: int,
    y_upper_left: int,
    y_lower_right: int,
    zoom_level: int,
) -> ndarray:

    array_concatted_in_x = np.array([])
    for x in range(x_upper_left, x_lower_right + 1):
        array_concatted_in_y = np.array([])
        for y in range(y_upper_left, y_lower_right + 1):
            elevation = get_elevation_array(x, y, zoom_level)
            if len(array_concatted_in_y) == 0:
                array_concatted_in_y = elevation
            else:
                array_concatted_in_y = np.append(
                    array_concatted_in_y, elevation, 0
                )
        if len(array_concatted_in_x) == 0:
            array_concatted_in_x = array_concatted_in_y
        else:
            array_concatted_in_x = np.append(
                array_concatted_in_x, array_concatted_in_y, 1
            )
    elevation = array_concatted_in_x
    return elevation
