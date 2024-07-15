import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from configuration import DPI, TITLE_SIZE, is_even_intervals
from constant import (
    CBAR_EXTENTION,
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_UNIT,
    COLOR_MAP_NAME,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy import ndarray

from .calculation import get_cbar_levels, get_normalization_object


class AxesMethod:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax
        self.levels = get_cbar_levels(is_even_intervals)

    def set_title(self, title_name: str) -> None:
        self.ax.set_title(title_name, fontsize=TITLE_SIZE)

    def plot_shading(self, lon: ndarray, lat: ndarray, data: ndarray) -> None:
        self.shade = self.ax.contourf(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=self.levels,
            cmap=COLOR_MAP_NAME,
            extend=CBAR_EXTENTION,
            norm=get_normalization_object(is_even_intervals, self.levels),
        )

    def plot_colorbar(self) -> None:
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.2, axes_class=Axes)
        plt.gcf().add_axes(cax)
        self.cbar = plt.colorbar(
            self.shade,
            cax=cax,
            orientation="vertical",
            ticks=self.levels,
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
        figure.savefig(save_file_path, dpi=DPI)
