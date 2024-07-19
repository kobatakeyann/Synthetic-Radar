import numpy as np

from constant import (
    CONTOUR_LABEL_INTERVAL,
    ELEVATION_INTERVAL,
    ELEVATION_MAX,
    ELEVATION_MIN,
)


def get_contour_levels() -> np.ndarray:
    levels = np.arange(
        float(ELEVATION_MIN),
        float(ELEVATION_MAX) + 0.000000000000001,
        float(ELEVATION_INTERVAL),
    )
    return levels


def get_clabel_levels() -> np.ndarray:
    levels = np.arange(
        float(ELEVATION_MIN),
        float(ELEVATION_MAX) + 0.000000000000001,
        float(CONTOUR_LABEL_INTERVAL),
    )
    return levels
