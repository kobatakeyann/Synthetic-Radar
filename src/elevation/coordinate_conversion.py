from math import atan, e, log, pi, tan


def lonlat_to_tile_coords(
    lon: float, lat: float, zoom_level: int
) -> tuple[int, int]:
    """Return the Geographical Survey Institute Tile Coordinates corresponding to the point designated by longitude and latitude.

    Args:
        lon (float): longitude of the point
        lat (float): latitude of the pount
        zoom_level (int): Zoom level in the Tile Coordinates

    Returns:
        tuple[int, int]: (x-coodinate, y-coodinate) in Tile Coordinates
    """
    x = int((lon / 180 + 1) * 2**zoom_level / 2)
    y = int(
        (
            (-log(tan((45 + lat / 2) * pi / 180)) + pi)
            * 2**zoom_level
            / (2 * pi)
        )
    )
    return x, y


def tile_coords_to_northwest_lonlat(
    x: int, y: int, zoom_level: int
) -> tuple[float, float]:
    """Return longitude and latitude of northwestern egde of the Geographical Survey Institute Tile Coordinates.

    Args:
        x (int): x-coodinate in Tile Coordinates
        y (int): y-coodinate in Tile Coordinates
        zoom_level (int): Zoom level in Tile Coordinates

    Returns:
        tuple[float, float]: (longitude, latitude) at the northwestern edge of the Tile Coordinates
    """
    lon_left = (x / 2.0**zoom_level) * 360 - 180
    mapy = (y / 2.0**zoom_level) * 2 * pi - pi
    lat_upper = 2 * atan(e ** (-mapy)) * 180 / pi - 90
    return lon_left, lat_upper
