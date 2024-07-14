from cartopy.mpl.geoaxes import GeoAxes
from constant import IS_DEG_MIN_FORMAT, PLOT_ELEVATION, PLOT_GRID_LINE

from .axes import MapAxesMethod


def make_base_map(ax: GeoAxes) -> GeoAxes:
    map_axes = MapAxesMethod(ax)
    print("Now making base map …")
    map_axes.plot_coastline()
    map_axes.plot_pref_border()
    map_axes.set_ticks()
    if PLOT_ELEVATION:
        map_axes.plot_elevation_with_contour()
    if PLOT_GRID_LINE:
        map_axes.draw_gridlines()
    if IS_DEG_MIN_FORMAT:
        map_axes.express_in_deg_min_format()
    map_axes.narrow_down_the_plot_area()
    print("Base map is successfully made!")
    return map_axes.ax
