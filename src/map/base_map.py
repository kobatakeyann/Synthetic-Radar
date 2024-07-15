from cartopy.mpl.geoaxes import GeoAxes
from configuration import is_deg_min_format, is_elevation_map, is_grid_line

from .axes import MapAxesMethod


def make_base_map(ax: GeoAxes) -> GeoAxes:
    map_axes = MapAxesMethod(ax)
    print("Now making base map …")
    map_axes.plot_coastline()
    map_axes.plot_pref_border()
    map_axes.set_ticks()
    if is_elevation_map:
        map_axes.plot_elevation_with_contour()
    if is_grid_line:
        map_axes.draw_gridlines()
    if is_deg_min_format:
        map_axes.express_in_deg_min_format()
    map_axes.narrow_down_the_plot_area()
    print("Base map is successfully made!")
    return map_axes.ax
