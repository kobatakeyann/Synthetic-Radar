from io import StringIO
from urllib.error import HTTPError

import numpy as np
import pandas as pd
from api.api_calling import fetch_data
from coordinate_conversion import (
    lonlat_to_tile_coords,
    tile_coords_to_northwest_lonlat,
)
from numpy import ndarray


class Elevation:
    def __init__(
        self,
        lon_left: float,
        lon_right: float,
        lat_bottom: float,
        lat_top: float,
        zoom_level: int,
    ) -> None:
        self.x_upper_left, self.y_upper_left = lonlat_to_tile_coords(
            lon_left, lat_top, zoom_level
        )
        self.x_lower_right, self.y_lower_right = lonlat_to_tile_coords(
            lon_right, lat_bottom, zoom_level
        )
        self.zoom_level = zoom_level

    def get_elevation_array(self, x: int, y: int) -> ndarray:
        """Acquire elevation array of one tile from Geographical Survey Institute.

        Args:
            x (int): x-coodinate in Tile Coordinates
            y (int): y-coodinate in Tile Coordinates
            zoom_level (int): Zoom level in Tile Coordinates

        Returns:
            ndarray: elevation array of the tile designated by coordinate(x,y)
        """
        url = f"http://cyberjapandata.gsi.go.jp/xyz/dem/{self.zoom_level}/{x}/{y}.txt"
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
        self,
    ) -> ndarray:

        array_concatted_in_x = np.array([])
        for x in range(self.x_upper_left, self.x_lower_right + 1):
            array_concatted_in_y = np.array([])
            for y in range(self.y_upper_left, self.y_lower_right + 1):
                elevation = self.get_elevation_array(x, y)
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
        self.elevation_array = array_concatted_in_x
        return self.elevation_array

    def get_coordinates_for_plot(self) -> tuple[ndarray, ndarray]:
        lon_left_edge, lat_top_edge = tile_coords_to_northwest_lonlat(
            self.x_upper_left, self.y_upper_left, self.zoom_level
        )
        lon_right_edge, lat_bottom_edge = tile_coords_to_northwest_lonlat(
            self.x_lower_right + 1, self.y_lower_right + 1, self.zoom_level
        )
        tile_num_x = self.elevation_array.shape[1]
        tile_num_y = self.elevation_array.shape[0]
        lon_deviation = ((lon_right_edge - lon_left_edge) / tile_num_x) * 0.5
        lat_deviation = ((lat_bottom_edge - lat_top_edge) / tile_num_y) * 0.5
        lon_coords = np.linspace(
            lon_left_edge + lon_deviation,
            lon_right_edge + lon_deviation,
            tile_num_x,
        )
        lat_coords = np.linspace(
            lat_top_edge + lat_deviation,
            lat_bottom_edge + lat_deviation,
            tile_num_y,
        )
        lon_coords, lat_coords = np.meshgrid(lon_coords, lat_coords)
        return lon_coords, lat_coords
