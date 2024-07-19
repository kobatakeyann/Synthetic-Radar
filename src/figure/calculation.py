import numpy as np
from matplotlib.colors import BoundaryNorm

from configuration import LAT_BOTTOM, LAT_TOP, LON_LEFT, LON_RIGHT
from constant import SHADE_INTERVAL, SHADE_MAX, SHADE_MIN


def calculate_figsize() -> tuple:
    lat_dif = LAT_TOP - LAT_BOTTOM
    lon_dif = LON_RIGHT - LON_LEFT
    figsize = (7, 7 * float(float(lat_dif) / float(lon_dif)))
    return figsize


def get_cbar_levels(is_even_intervals: bool) -> np.ndarray:
    if is_even_intervals:
        levels = np.arange(
            float(SHADE_MIN),
            float(SHADE_MAX) + 0.000000000000001,
            float(SHADE_INTERVAL),
        )
    else:
        levels = np.array([1, 2, 4, 8, 16, 25, 32, 48, 64, 81, 100])
    return levels


def get_normalization_object(
    is_divided_evenly: bool,
    levels: np.ndarray,
) -> None | BoundaryNorm:
    if is_divided_evenly:
        return
    else:
        return BoundaryNorm(levels, 256)
