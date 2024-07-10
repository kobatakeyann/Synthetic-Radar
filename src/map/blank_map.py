from axes import MapAxesMethod
from cartopy.mpl.geoaxes import GeoAxes
from constant import IS_DEG_MIN_FORMAT


def make_blank_map(ax: GeoAxes) -> GeoAxes:
    map_axes = MapAxesMethod(ax)
    map_axes.plot_coastline()
    map_axes.plot_pref_border()
    map_axes.set_ticks()
    if IS_DEG_MIN_FORMAT:
        map_axes.express_in_deg_min_format()
    map_axes.narrow_down_the_plot_area()
    return map_axes.ax
