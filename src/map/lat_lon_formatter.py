def format_longitude(lon: float, _) -> str:
    """Function passed as the argument of 'set_major_formatter'.
    The second argument must be explicitly stated for the use of the function.
    Return a label of longitude in [degree°minute'E] format.

    Args:
        lon (float): longitude in float format.
        _ : necessary for the use of set_major_formatter

    Returns:
        str: longitude in [degree°minute'E] format
    """
    degrees = int(lon)
    minutes = abs(int((lon - degrees) * 60))
    if minutes == 0:
        minutes = "00"
    return f"{degrees}°{minutes}'E"


def format_latitude(lat: float, _) -> str:
    """Function passed as the argument of 'set_major_formatter'.
    The second argument must be explicitly stated for the use of the function.
    Return a label of latitude in [degree°minute'E] format.

    Args:
        lat (float): latitude in float format.
        _ : necessary for the use of set_major_formatter

    Returns:
        str: latitude in [degree°minute'E] format
    """
    degrees = int(lat)
    minutes = abs(int((lat - degrees) * 60))
    if minutes == 0:
        minutes = "00"
    return f"{degrees}°{minutes}'N"
