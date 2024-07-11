from datetime import datetime

import pandas as pd
from figure.plot import FigureFactory

if __name__ == "__main__":
    start_datetime = datetime(2023, 7, 27, 0, 0)
    end_datetime = datetime(2023, 7, 27, 23, 50)
    jst_datetimes = pd.date_range(start_datetime, end_datetime, freq="10min")
    factory = FigureFactory(jst_datetimes)
    factory.make_continuous_figures()
