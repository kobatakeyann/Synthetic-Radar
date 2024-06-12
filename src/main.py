from datetime import datetime
from plot.rainfall_map import make_continuous_figures


if __name__ == "__main__":
    startdate = datetime(2023,8,23,0,0)
    enddate = datetime(2023,8,25,0,0)
    elevation = False
    make_continuous_figures(startdate,enddate,elevation)
