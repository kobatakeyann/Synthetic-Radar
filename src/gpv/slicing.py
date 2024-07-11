from bisect import bisect_left
from datetime import datetime

import numpy as np
from constant import LAT_BOTTOM, LAT_TOP, LON_LEFT, LON_RIGHT
from gpv_fetcher import get_jma_gpv
from nakametpy.jma import get_jmara_lat, get_jmara_lon
from numpy import ndarray


class GPV:
    def __init__(self) -> None:
        self.jmara_lat_array = get_jmara_lat()
        self.jmara_lon_array = get_jmara_lon()
        self.get_range_of_index()

    def get_range_of_index(self) -> None:
        self.x_index_start = bisect_left(self.jmara_lon_array, LON_LEFT) - 10
        self.x_index_end = bisect_left(self.jmara_lon_array, LON_RIGHT) + 10
        self.y_index_start = bisect_left(self.jmara_lat_array, LAT_BOTTOM) - 10
        self.y_index_end = bisect_left(self.jmara_lat_array, LAT_TOP) + 10

    def get_coords_for_plot(self) -> tuple[ndarray, ndarray]:
        sliced_lat = self.jmara_lat_array[
            self.y_index_start : self.y_index_end
        ]
        sliced_lon = self.jmara_lon_array[
            self.x_index_start : self.x_index_end
        ]
        lon_coords, lat_coords = np.meshgrid(sliced_lon, sliced_lat)
        return lon_coords, lat_coords

    def get_sliced_precipitation_array(
        self, utc_datetime: datetime
    ) -> ndarray:
        precipitation_array = get_jma_gpv(utc_datetime)
        sliced_precipitation = precipitation_array[
            self.y_index_start : self.y_index_end,
            self.x_index_start : self.x_index_end,
        ]
        return sliced_precipitation
