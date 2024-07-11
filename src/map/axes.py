import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
import numpy as np
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from constant import (
    CONTOUR_COLOR,
    CONTOUR_LABEL_SIZE,
    CONTOUR_WIDTH,
    GRIDLINE_COLOR,
    GRIDLINE_WIDTH,
    LAT_BOTTOM,
    LAT_TICKS_INTERVAL,
    LAT_TOP,
    LON_LEFT,
    LON_RIGHT,
    LON_TICKS_INTERVAL,
    PLOT_ELEVATION_LABEL,
    ZOOM_LEVEL,
)
from elevation.elevation_fetcher import Elevation
from lat_lon_formatter import format_latitude, format_longitude
from level_calculation import get_clabel_levels, get_contour_levels


class MapAxesMethod:
    def __init__(self, ax: GeoAxes) -> None:
        self.ax = ax
        self.xloc = np.arange(0, 180 + 0.00000001, LON_TICKS_INTERVAL)
        self.yloc = np.arange(0, 90 + 0.00000001, LAT_TICKS_INTERVAL)

    def plot_coastline(self) -> None:
        self.ax.coastlines(linewidths=1, resolution="10m")

    def plot_pref_border(self) -> None:
        shpfilename = shapereader.natural_earth(
            resolution="10m",
            category="cultural",
            name="admin_1_states_provinces",
        )
        provinces = shapereader.Reader(shpfilename).records()
        prefs = filter(
            lambda province: province.attributes["admin"] == "Japan", provinces
        )
        for pref in prefs:
            geometry = pref.geometry
            self.ax.add_geometries(
                [geometry],
                ccrs.PlateCarree(),
                facecolor="none",
                linestyle="-",
                linewidth=0.15,
            )

    def plot_elevation_with_contour(self):
        target_area = Elevation(
            LON_LEFT, LON_RIGHT, LAT_BOTTOM, LAT_TOP, ZOOM_LEVEL
        )
        elevation_array = target_area.get_concatted_array()
        lon_coords, lat_coords = target_area.get_coordinates_for_plot()
        self.contours = self.ax.contour(
            lon_coords,
            lat_coords,
            elevation_array,
            transform=ccrs.PlateCarree(),
            levels=get_contour_levels(),
            linewidths=CONTOUR_WIDTH,
            colors=CONTOUR_COLOR,
        )
        if PLOT_ELEVATION_LABEL:
            self.ax.clabel(
                self.contours,
                levels=get_clabel_levels(),
                fmt="%.{0[0]}f".format([0]),
                fontsize=CONTOUR_LABEL_SIZE,
            )

    def set_ticks(self) -> None:
        self.ax.set_xticks(self.xloc, crs=ccrs.PlateCarree())
        self.ax.set_yticks(self.yloc, crs=ccrs.PlateCarree())
        self.ax.xaxis.set_major_formatter(LongitudeFormatter())
        self.ax.yaxis.set_major_formatter(LatitudeFormatter())

    def draw_gridlines(self) -> None:
        gl = self.ax.gridlines(
            draw_labels=True, color=GRIDLINE_COLOR, linewidth=GRIDLINE_WIDTH
        )
        gl.right_labels = False
        gl.top_labels = False
        gl.left_labels = False
        gl.bottom_labels = False

    def express_in_deg_min_format(self) -> None:
        self.ax.xaxis.set_major_formatter(format_longitude)
        self.ax.yaxis.set_major_formatter(format_latitude)

    def narrow_down_the_plot_area(self) -> None:
        self.ax.set_extent(
            (LON_LEFT, LON_RIGHT, LAT_BOTTOM, LAT_TOP), ccrs.PlateCarree()
        )
