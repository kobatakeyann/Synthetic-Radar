import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from calculation import get_cbar_levels
from cartopy.mpl.geoaxes import GeoAxes
from constant import (
    CBAR_EXTENTION,
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_TICKS_BASE,
    CBAR_TICKS_INTERVAL,
    CBAR_UNIT,
    COLOR_MAP_NAME,
    DIVIDE_EVENLY,
    IS_AUTO_TICKS,
    TITLE_SIZE,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import ndarray


class AxesMethod:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def set_title(self, title_name: str) -> None:
        self.ax.set_title(title_name, fontsize=TITLE_SIZE)

    def plot_shading(self, lon: ndarray, lat: ndarray, data: ndarray) -> None:
        self.shade = self.ax.contourf(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=get_cbar_levels(DIVIDE_EVENLY),
            cmap=COLOR_MAP_NAME,
            extend=CBAR_EXTENTION,
        )

    def plot_colorbar(self) -> None:
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.2, axes_class=Axes)
        plt.gcf().add_axes(cax)
        if IS_AUTO_TICKS:
            self.cbar = plt.colorbar(
                self.shade, cax=cax, orientation="vertical"
            )
        else:
            ticks = mticker.IndexLocator(
                base=CBAR_TICKS_BASE, offset=CBAR_TICKS_INTERVAL
            )
            self.cbar = plt.colorbar(
                self.shade, cax=cax, ticks=ticks, orientation="vertical"
            )

    def set_cbar_label(self) -> None:
        self.cbar.set_label(
            CBAR_UNIT,
            labelpad=CBAR_LABEL_LOCATION,
            y=1.08,
            rotation=0,
            fontsize=CBAR_LABEL_SIZE,
        )

    def save_figure(
        self, figure: Figure, save_dir: str, file_name: str
    ) -> None:
        os.makedirs(save_dir, exist_ok=True)
        save_file_path = f"{save_dir}/{file_name}"
        figure.savefig(save_file_path, dpi=300)
