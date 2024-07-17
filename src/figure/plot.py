import pickle
from datetime import datetime

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from configuration import is_mp4_making
from gif.gif import make_gif_from_imgs
from gpv.slicing import GPV
from map.base_map import make_base_map
from pandas import DatetimeIndex
from time_relation.conversion import jst_to_utc
from video.mp4 import make_mp4_from_imgs

from .calculation import calculate_figsize
from .method import AxesMethod
from .text_handling import TextAquisition


class FigureFactory:
    def __init__(self, jst_datetimes: DatetimeIndex) -> None:
        fig = plt.figure(figsize=calculate_figsize())
        ax = fig.add_axes(
            (0.11, 0.15, 0.8, 0.8),
            projection=ccrs.PlateCarree(),
        )
        make_base_map(ax)
        self.basefig = pickle.dumps(fig, protocol=pickle.HIGHEST_PROTOCOL)
        self.gpv_dataset = GPV()
        self.lon, self.lat = self.gpv_dataset.get_coords_for_plot()
        self.datetimes = jst_datetimes

    def make_figure(self, jst_datetime: datetime) -> None:
        basefig = pickle.loads(self.basefig)
        target_ax = AxesMethod(plt.gca())
        utc_datetime = jst_to_utc(jst_datetime)
        precipitation = self.gpv_dataset.get_sliced_precipitation_array(
            utc_datetime
        )
        target_ax.plot_shading(self.lon, self.lat, precipitation)
        target_ax.plot_colorbar()
        target_ax.set_cbar_label()
        text_generator = TextAquisition(jst_datetime)
        title = text_generator.get_title_text()
        self.save_dir = text_generator.get_save_dir()
        filename = text_generator.get_save_filename()
        target_ax.set_title(title)
        target_ax.save_figure(basefig, self.save_dir, filename)
        plt.cla()
        plt.close()

    def make_continuous_figures(self):
        for datetime in self.datetimes:
            print(f"Now making {datetime} figure …")
            self.make_figure(
                jst_datetime=datetime,
            )
            text_generator = TextAquisition(datetime)
            if datetime.hour == 23 and datetime.minute == 50:
                gif_filename = text_generator.get_save_gifname()
                video_filename = text_generator.get_save_videoname()
                print("Now making gif …")
                make_gif_from_imgs(
                    self.save_dir, f"{self.save_dir}/{gif_filename}"
                )
                if is_mp4_making:
                    print("Now making mp4 …")
                    make_mp4_from_imgs(
                        self.save_dir, f"{self.save_dir}/{video_filename}"
                    )
                print("Successfully Completed!")
        print("All Images are successfully made!")
