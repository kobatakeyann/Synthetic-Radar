import os
import pickle
import nakametpy.jma

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.axes as maxes

from datetime import datetime, timedelta
from mpl_toolkits.axes_grid1 import make_axes_locatable
from bisect import bisect_left

from util.path_complement import generate_path
from gpv.data_acquisition import load_jma_gpv
from time_relation.conversion import PaddingDate, jst_to_utc
from map.blank_map import make_blank_map
from map.elevation_map import make_elevation_map
from gif.gif import make_gif_from_imgs
from ..constant import (
    LON_LEFT,
    LON_RIGHT,
    LAT_BOTTOM,
    LAT_TOP,
    LABEL_LOCATION,
    LABEL_SIZE,
    LEVELS,
    ELEVATION,
    ELEVATION_MIN,
    ELEVATION_INTERVAL,
    ZOOM_LEVEL,
    IS_DEG_MIN_FORMAT,
    TICKS_INTERVAL,
    TITLE_FONTSIZE,
)


def make_precipitation_figure(jst_datetime, elevation):
    """全国合成レーダーGPVの値を用いて雨雲レーダーの図を作る関数

    Arg:
      jst_datetime (datetime) : 描画したい日時
      elevation    (bool)     : 標高の等高線をplotする場合はTrue、しない場合はFalse
    """

    # 降水量の配列と緯度経度情報の取得
    utc_datetime = jst_to_utc(jst_datetime)
    data = load_jma_gpv(utc_datetime)
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()

    # # 降水量の最大値とその緯度・経度の取得
    # max_precipitation = np.max(data)
    # lat_idx, lon_idx, = np.unravel_index(np.argmax(data), data.shape)
    # print(f"max:{max_precipitation}, lat:{lat_list[lat_idx]}, lon:{lon_list[lon_idx]}")

    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            ZOOM_LEVEL,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
            contour_min=ELEVATION_MIN,
            contour_interval=ELEVATION_INTERVAL,
        )
        print("Data loading has been completed!")
    else:
        make_blank_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
        )

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list, LON_LEFT)
    x_right = bisect_left(lon_list, LON_RIGHT)
    y_bottom = bisect_left(lat_list, LAT_BOTTOM)
    y_top = bisect_left(lat_list, LAT_TOP)

    # 図の描画
    fig = plt.gcf()
    ax = plt.gca()
    lon, lat = np.meshgrid(lon_list, lat_list)
    # shadeplot
    shade = ax.contourf(
        lon[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
        lat[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
        data[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
        transform=ccrs.PlateCarree(),
        cmap=cm.jet,
        levels=LEVELS,
        extend="max",
    )

    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(
        "right", size="4%", pad=0.2, axes_class=maxes.Axes
    )
    fig.add_axes(cax)
    cbar = plt.colorbar(
        shade, cax=cax, orientation="vertical", extendfrac="auto"
    )
    cbar.set_label(
        r"[$\mathrm{mm\,h^{-1}}$]",
        labelpad=LABEL_LOCATION,
        y=1.15,
        rotation=0,
        fontsize=LABEL_SIZE,
    )

    # 観測時間のプロット
    print(jst_datetime)
    target_datetime = PaddingDate(jst_datetime)
    year, month, day, hour, minute = (
        target_datetime.year,
        target_datetime.month,
        target_datetime.day,
        target_datetime.hour,
        target_datetime.minute,
    )
    ax = plt.gcf().get_axes()[0]
    ax.set_title(
        f"{year}/{month}/{day} {hour}{minute}JST", fontsize=TITLE_FONTSIZE
    )

    # 図の保存
    save_dir = generate_path(f"/img/{year}/{month}/{day}")
    filename = f"{year}{month}{day}{hour}{minute}.jpg"
    os.makedirs(save_dir, exist_ok=True)
    fig.savefig(f"{save_dir}/{filename}", dpi=600, pad_inches=0.1)

    print("Figure is successfully made.")
    plt.clf()
    plt.close()


def make_continuous_figures(startdate, enddate, elevation):
    """複数の連続した日の雨雲レーダー図を作る関数

    Arg:
      startdate (datetime) : 描画する期間の最初の日
      enddate   (datetime) : 描画する期間の最後の日
      elevation  (bool)    : 標高の等高線をplotする場合はTrue、しない場合はFalse
    """

    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            ZOOM_LEVEL,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
            contour_min=ELEVATION_MIN,
            contour_interval=ELEVATION_INTERVAL,
        )
        print("Data loading has been completed!")
    else:
        make_blank_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
        )

    # 緯度経度情報の取得
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()
    lon, lat = np.meshgrid(lon_list, lat_list)

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list, LON_LEFT)
    x_right = bisect_left(lon_list, LON_RIGHT)
    y_bottom = bisect_left(lat_list, LAT_BOTTOM)
    y_top = bisect_left(lat_list, LAT_TOP)

    # 下地となる地図を保存
    fig = plt.gcf()
    basefig = pickle.dumps(fig)

    exe_jsttime = startdate
    while startdate <= exe_jsttime <= enddate:
        # 下地の地図を取得
        copied_fig = pickle.loads(basefig)
        ax = plt.gcf().get_axes()[0]

        # shadeplot
        # 引数はutc時刻
        exe_utctime = jst_to_utc(exe_jsttime)
        data = load_jma_gpv(exe_utctime)
        shade = ax.contourf(
            lon[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
            lat[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
            data[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
            transform=ccrs.PlateCarree(),
            cmap=cm.jet,
            levels=LEVELS,
            extend="max",
        )
        # colorbarplot
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(
            "right", size="4%", pad=0.2, axes_class=maxes.Axes
        )
        copied_fig.add_axes(cax)
        cbar = plt.colorbar(
            shade, cax=cax, orientation="vertical", extendfrac="auto"
        )
        cbar.set_label(
            r"[$\mathrm{mm\,h^{-1}}$]",
            labelpad=LABEL_LOCATION,
            y=1.15,
            rotation=0,
            fontsize=LABEL_SIZE,
        )
        # 観測時間のプロット
        print(exe_jsttime)
        target_datetime = PaddingDate(exe_jsttime)
        year, month, day, hour, minute = (
            target_datetime.year,
            target_datetime.month,
            target_datetime.day,
            target_datetime.hour,
            target_datetime.minute,
        )
        ax.set_title(
            f"{year}/{month}/{day} {hour}{minute}JST", fontsize=TITLE_FONTSIZE
        )

        # 図の保存
        save_dir = generate_path(f"/img/{year}/{month}/{day}")
        filename = f"{year}{month}{day}{hour}{minute}.jpg"
        os.makedirs(save_dir, exist_ok=True)
        # copied_fig.savefig(f"{save_dir}/{filename}", dpi=100, pad_inches=0.1)
        # copied_fig.savefig(f"{filename}", dpi=100, pad_inches=0.1)

        plt.clf()
        plt.close()

        # gifの作成
        # if int(hour) == 23 and int(minute) == 50:
        #     gif_title = f"{year}{month}{day}.gif"
        #     print("Converting figures into gif…")
        #     convert_jpg_to_gif(save_dir,save_dir,gif_title)
        #     print("Gif is successfully made.")

        exe_jsttime += timedelta(minutes=10)

    print("Figures are successfully made.")


def make_figures_of_group(date_list, group_name, elevation):
    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            ZOOM_LEVEL,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
            contour_min=ELEVATION_MIN,
            contour_interval=ELEVATION_INTERVAL,
        )
        print("Data loading has been completed!")
    else:
        make_blank_map(
            LON_LEFT,
            LON_RIGHT,
            LAT_BOTTOM,
            LAT_TOP,
            IS_DEG_MIN_FORMAT,
            lon_interval=TICKS_INTERVAL,
            lat_interval=TICKS_INTERVAL,
        )

    # 緯度経度情報の取得
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()
    lon, lat = np.meshgrid(lon_list, lat_list)

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list, LON_LEFT)
    x_right = bisect_left(lon_list, LON_RIGHT)
    y_bottom = bisect_left(lat_list, LAT_BOTTOM)
    y_top = bisect_left(lat_list, LAT_TOP)

    # 下地となる地図を保存
    fig = plt.gcf()
    basefig = pickle.dumps(fig)

    for exe_date in date_list:
        exe_jsttime = datetime.datetime(
            exe_date.year, exe_date.month, exe_date.day, 0, 0
        )
        for i in range(144):
            # 下地の地図を取得
            copied_fig = pickle.loads(basefig)
            ax = plt.gcf().get_axes()[0]

            # shadeplot
            exe_utctime = jst_to_utc(exe_jsttime)
            data = load_jma_gpv(exe_utctime)
            shade = ax.contourf(
                lon[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
                lat[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
                data[y_bottom - 10 : y_top + 10, x_left - 10 : x_right + 10],
                transform=ccrs.PlateCarree(),
                cmap=cm.jet,
                levels=LEVELS,
                extend="max",
            )
            # colorbarplot
            divider = make_axes_locatable(ax)
            cax = divider.append_axes(
                "right", size="4%", pad=0.2, axes_class=maxes.Axes
            )
            copied_fig.add_axes(cax)
            cbar = plt.colorbar(
                shade, cax=cax, orientation="vertical", extendfrac="auto"
            )
            cbar.set_label(
                r"[$\mathrm{mm\,h^{-1}}$]",
                labelpad=LABEL_LOCATION,
                y=1.15,
                rotation=0,
                fontsize=LABEL_SIZE,
            )
            # 観測時間のプロット
            print(exe_jsttime)
            target_datetime = PaddingDate(exe_jsttime)
            year, month, day, hour, minute = (
                target_datetime.year,
                target_datetime.month,
                target_datetime.day,
                target_datetime.hour,
                target_datetime.minute,
            )
            ax.set_title(
                f"{year}/{month}/{day} {hour}{minute}JST",
                fontsize=TITLE_FONTSIZE,
            )

            # 図の保存
            save_dir = generate_path(f"/img/{group_name}/{year}{month}{day}")
            filename = f"{year}{month}{day}{hour}{minute}.jpg"
            os.makedirs(save_dir, exist_ok=True)
            copied_fig.savefig(
                f"{save_dir}/{filename}", dpi=100, pad_inches=0.1
            )

            plt.clf()
            plt.close()

            # gifの作成
            if int(hour) == 23 and int(minute) == 50:
                gif_filename = f"{year}{month}{day}.gif"
                gif_file_path = f"{save_dir}/{gif_filename}"
                print("Converting figures into gif…")
                make_gif_from_imgs(save_dir, gif_file_path)
                print("Gif is successfully made.")

            exe_jsttime += datetime.timedelta(minutes=10)

    print("Figures are successfully made.")
