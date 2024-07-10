from datetime import datetime
from plot.rainfall_map import make_continuous_figures


if __name__ == "__main__":
    startdate = datetime(2023, 8, 21, 9, 0)
    enddate = datetime(2023, 8, 21, 21, 0)
    elevation = True
    make_continuous_figures(startdate, enddate, elevation)
