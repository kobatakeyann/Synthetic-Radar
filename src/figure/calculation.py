import numpy as np
from constant import (
    LAT_BOTTOM,
    LAT_TOP,
    LON_LEFT,
    LON_RIGHT,
    SHADE_INTERVAL,
    SHADE_MAX,
    SHADE_MIN,
)
from numpy import ndarray


def calculate_figsize() -> tuple:
    lat_dif = LAT_TOP - LAT_BOTTOM
    lon_dif = LON_RIGHT - LON_LEFT
    figsize = (7, 7 * float(float(lat_dif) / float(lon_dif)))
    return figsize


def get_cbar_levels(is_divided_evenly: bool) -> ndarray:
    if is_divided_evenly:
        levels = np.arange(
            float(SHADE_MIN),
            float(SHADE_MAX) + 0.000000000000001,
            float(SHADE_INTERVAL),
        )
    else:
        levels = np.logspace(start=0, stop=7, num=8, base=2)
    return levels
