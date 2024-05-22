import os
import pickle
import datetime
import urllib.request
import urllib.error
import nakametpy.jma

import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.axes as maxes
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from mpl_toolkits.axes_grid1 import make_axes_locatable
from bisect import bisect_left

from util.path_complement import generate_path
from util.tempfile_name import generate_random_strings
from time_relation.conversion import PaddingDate, jst_to_utc
from map.blank_map import make_blank_map
from map.elevation_map import make_elevation_map
from gif.gif import convert_jpg_to_gif


#描画領域の設定
# lon_left, lon_right = 120, 150
# lat_bottom, lat_top = 22.4, 47.6
# lon_left, lon_right = 129.2, 132.2
# lat_bottom, lat_top = 30.9, 34.1
# lon_left, lon_right = 129.68, 130.94
# lat_bottom, lat_top = 33.14, 34
lon_left, lon_right = 129.88, 130.74
lat_bottom, lat_top = 33.34, 34

#colorbarの設定
label_loc = 3
label_size = 12
# levels = np.arange(1,51,5)
# levels = np.array([1,5,10,16,25,32,48,64,81])
levels = np.array([1,5,10,15,20,25,30,35,40,45])

# 標高データの設定
elevation = True
elevation_min = 150
elevation_interval = 100
zoom_level = 8


# 緯度経度目盛りの設定
deg_min_format = False
latlon_ticks_interval = 0.5

# タイトルのfontsize
title_size = 20


# 設定項目の説明
"""
lon_left, lon_right         (float)     : 描画したい経度の左端と右端 
lat_bottom, lat_top         (float)     : 描画したい緯度の下端と上端 
label_loc                   (float)     : カラーバーの凡例の水平方向の位置
label_size                  (float)     : カラーバーの凡例の文字の大きさ       
levels                      (ndarray)   : カラーバーの目盛りを表すnumpy.ndarray
elevation                   (bool)      : 標高について等高線をplotする場合はTrue、しない場合はFalse
elevation_min               (int)       : 等高線をひく標高の最小値
elevation_interval          (int)       : 等高線をひく標高の間隔
zoom_level                  (int)       : 標高地図にプロットする際のズームレベル(国土地理院マップ参照)
　　　　　　　　　　　　　　　　           　 0~18の整数で、大きいほど解像度が高い(目安8~11)
deg_min_format              (bool)      : 図の緯度経度目盛りについて、
                                          度分表記する際はTrueに、度表記にする際はFalseに
latlon_ticks_interval       (float)     : 緯線経線の目盛りの間隔
title_fontsize              (float)     : 図のタイトルの文字の大きさ
"""

####################################################################################

def load_jma_gpv(jst_datetime):
    '''全国合成レーダーGPVの値の配列を返す関数

    Arg:
      jst_datetime (datetime)  
    '''
    
    # 0補完された日付文字列の取得
    utc_datetime = jst_to_utc(jst_datetime)
    target_datetime = PaddingDate(utc_datetime)
    year = target_datetime.year
    month = target_datetime.month
    day = target_datetime.day
    hour = target_datetime.hour
    minute = target_datetime.minute

    _url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/"\
           f"{year}/{month}/{year}/Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV__grib2.tar"

    # url先から配列を取得
    try:
        random_strings = generate_random_strings(5)
        _tmpfile = f"/tmp/tmp{random_strings}"
        _req = urllib.request.Request(_url)
        with urllib.request.urlopen(_req) as _res:
            _urlData = _res.read()
            with open(_tmpfile, mode='wb') as f:
                f.write(_urlData)
                _tar_contentname = f"Z__C_RJTD_{year}{month}{day}{hour}{minute}00_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
                _data = nakametpy.jma.load_jmara_grib2(_tmpfile,tar_flag=True,tar_contentname=_tar_contentname)
                os.remove(_tmpfile)
                return _data
            
    except urllib.error.HTTPError as err:
        print(f"{jst_datetime}: {err.code}")

    except urllib.error.URLError as err:
        print(f"{jst_datetime}: {err.reason}")


def make_precipitation_figure(jst_datetime,elevation):
    '''全国合成レーダーGPVの値を用いて雨雲レーダーの図を作る関数

    Arg:
      jst_datetime (datetime) : 描画したい日時
      elevation    (bool)     : 標高の等高線をplotする場合はTrue、しない場合はFalse
    '''

    # 降水量の配列と緯度経度情報の取得
    data = load_jma_gpv(jst_datetime)
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()

    # # 降水量の最大値とその緯度・経度の取得
    # max_precipitation = np.max(data)
    # lat_idx, lon_idx, = np.unravel_index(np.argmax(data), data.shape)
    # print(f"max:{max_precipitation}, lat:{lat_list[lat_idx]}, lon:{lon_list[lon_idx]}")

    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(lon_left,lon_right,lat_bottom,lat_top,zoom_level,
                           deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval,
                           contour_min=elevation_min,contour_interval=elevation_interval)
        print("Data loading has been completed!")
    else:
        make_blank_map(lon_left,lon_right,lat_bottom,lat_top,
                       deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval)

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list,lon_left)
    x_right = bisect_left(lon_list,lon_right)
    y_bottom = bisect_left(lat_list,lat_bottom)
    y_top = bisect_left(lat_list,lat_top)

    # 図の描画
    fig = plt.gcf()
    ax = plt.gca()
    lon, lat = np.meshgrid(lon_list,lat_list)
    # shadeplot
    shade = ax.contourf(lon[y_bottom-10:y_top+10,x_left-10:x_right+10],
                        lat[y_bottom-10:y_top+10,x_left-10:x_right+10],
                        data[y_bottom-10:y_top+10,x_left-10:x_right+10],
                        transform=ccrs.PlateCarree(),
                        cmap=cm.jet, levels=levels, extend='max')

    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.2, axes_class=maxes.Axes)
    fig.add_axes(cax)
    cbar = plt.colorbar(shade, cax=cax, orientation='vertical',extendfrac='auto')
    cbar.set_label(r"[$\mathrm{mm\,h^{-1}}$]", labelpad=label_loc, y=1.15, rotation=0, fontsize=label_size)

    # 観測時間のプロット
    print(jst_datetime)
    target_datetime = PaddingDate(jst_datetime)
    year = target_datetime.year
    month = target_datetime.month
    day = target_datetime.day
    hour = target_datetime.hour
    minute = target_datetime.minute
    ax = plt.gcf().get_axes()[0]
    ax.set_title(f"{year}/{month}/{day} {hour}{minute}JST", fontsize=title_size)

    # 図の保存
    save_dir = generate_path(f"/img/{year}/{month}/{day}")
    filename = f"{year}{month}{day}{hour}{minute}.jpg"
    os.makedirs(save_dir,exist_ok=True)
    fig.savefig(f"{save_dir}/{filename}", dpi=600, pad_inches=0.1)

    print("Figure is successfully made.")
    plt.clf()
    plt.close()


def make_continuous_figures(startdate,enddate,elevation):
    '''複数の連続した日の雨雲レーダー図を作る関数

    Arg:
      startdate (datetime) : 描画する期間の最初の日
      enddate   (datetime) : 描画する期間の最後の日
      elevation  (bool)    : 標高の等高線をplotする場合はTrue、しない場合はFalse
    '''
    
    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(lon_left,lon_right,lat_bottom,lat_top,zoom_level,
                           deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval,
                           contour_min=elevation_min,contour_interval=elevation_interval)
        print("Data loading has been completed!")
    else:
        make_blank_map(lon_left,lon_right,lat_bottom,lat_top,
                       deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval)

    # 緯度経度情報の取得
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()
    lon, lat = np.meshgrid(lon_list,lat_list)

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list,lon_left)
    x_right = bisect_left(lon_list,lon_right)
    y_bottom = bisect_left(lat_list,lat_bottom)
    y_top = bisect_left(lat_list,lat_top)
    
    # 下地となる地図を保存
    fig = plt.gcf()
    basefig = pickle.dumps(fig)

    exe_jsttime = startdate
    while startdate <= exe_jsttime <= enddate:
        # 下地の地図を取得
        copied_fig = pickle.loads(basefig)
        ax = plt.gcf().get_axes()[0]

        # shadeplot
        data = load_jma_gpv(exe_jsttime)
        shade = ax.contourf(lon[y_bottom-10:y_top+10,x_left-10:x_right+10],
                            lat[y_bottom-10:y_top+10,x_left-10:x_right+10],
                            data[y_bottom-10:y_top+10,x_left-10:x_right+10],
                            transform=ccrs.PlateCarree(),
                            cmap=cm.jet, levels=levels, extend='max')
        # colorbarplot
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="4%", pad=0.2, axes_class=maxes.Axes)
        copied_fig.add_axes(cax)
        cbar = plt.colorbar(shade, cax=cax, orientation='vertical',extendfrac='auto')
        cbar.set_label(r"[$\mathrm{mm\,h^{-1}}$]", labelpad=label_loc, y=1.15, rotation=0, fontsize=label_size)
        # 観測時間のプロット
        print(exe_jsttime)
        target_datetime = PaddingDate(exe_jsttime)
        year = target_datetime.year
        month = target_datetime.month
        day = target_datetime.day
        hour = target_datetime.hour
        minute = target_datetime.minute
        ax.set_title(f"{year}/{month}/{day} {hour}{minute}JST", fontsize=title_size)

        # 図の保存
        save_dir = generate_path(f"/img/{year}/{month}/{day}")
        filename = f"{year}{month}{day}{hour}{minute}.jpg"
        os.makedirs(save_dir,exist_ok=True)
        copied_fig.savefig(f"{save_dir}/{filename}", dpi=100, pad_inches=0.1)

        plt.clf()
        plt.close()

        # gifの作成
        if int(hour) == 23 and int(minute) == 50:
            gif_title = f"{year}{month}{day}.gif"
            print("Converting figures into gif…")
            convert_jpg_to_gif(save_dir,save_dir,gif_title)
            print("Gif is successfully made.")

        exe_jsttime += datetime.timedelta(minutes=10)

    print("Figures are successfully made.")

    
def make_figures_of_group(date_list,group_name,elevation):
    # 地図情報の取得
    if elevation:
        print("Elevation data is now loading…")
        make_elevation_map(lon_left,lon_right,lat_bottom,lat_top,zoom_level,
                           deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval,
                           contour_min=elevation_min,contour_interval=elevation_interval)
        print("Data loading has been completed!")
    else:
        make_blank_map(lon_left,lon_right,lat_bottom,lat_top,
                       deg_min_format,lon_interval=latlon_ticks_interval,lat_interval=latlon_ticks_interval)

    # 緯度経度情報の取得
    lat_list = nakametpy.jma.get_jmara_lat()
    lon_list = nakametpy.jma.get_jmara_lon()
    lon, lat = np.meshgrid(lon_list,lat_list)

    # スライスのためのindexを取得
    x_left = bisect_left(lon_list,lon_left)
    x_right = bisect_left(lon_list,lon_right)
    y_bottom = bisect_left(lat_list,lat_bottom)
    y_top = bisect_left(lat_list,lat_top)
    
    # 下地となる地図を保存
    fig = plt.gcf()
    basefig = pickle.dumps(fig)

    for exe_date in date_list:
        exe_jsttime = datetime.datetime(exe_date.year,exe_date.month,exe_date.day,0,0)
        for i in range(144):
            # 下地の地図を取得
            copied_fig = pickle.loads(basefig)
            ax = plt.gcf().get_axes()[0]

            # shadeplot
            data = load_jma_gpv(exe_jsttime)
            shade = ax.contourf(lon[y_bottom-10:y_top+10,x_left-10:x_right+10],
                                lat[y_bottom-10:y_top+10,x_left-10:x_right+10],
                                data[y_bottom-10:y_top+10,x_left-10:x_right+10],
                                transform=ccrs.PlateCarree(),
                                cmap=cm.jet, levels=levels, extend='max')
            # colorbarplot
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="4%", pad=0.2, axes_class=maxes.Axes)
            copied_fig.add_axes(cax)
            cbar = plt.colorbar(shade, cax=cax, orientation='vertical',extendfrac='auto')
            cbar.set_label(r"[$\mathrm{mm\,h^{-1}}$]", labelpad=label_loc, y=1.15, rotation=0, fontsize=label_size)
            # 観測時間のプロット
            print(exe_jsttime)
            target_datetime = PaddingDate(exe_jsttime)
            year = target_datetime.year
            month = target_datetime.month
            day = target_datetime.day
            hour = target_datetime.hour
            minute = target_datetime.minute
            ax.set_title(f"{year}/{month}/{day} {hour}{minute}JST", fontsize=title_size)

            # 図の保存
            save_dir = generate_path(f"/img/{group_name}/{year}{month}{day}")
            filename = f"{year}{month}{day}{hour}{minute}.jpg"
            os.makedirs(save_dir,exist_ok=True)
            copied_fig.savefig(f"{save_dir}/{filename}", dpi=100, pad_inches=0.1)

            plt.clf()
            plt.close()

            # gifの作成
            if int(hour) == 23 and int(minute) == 50:
                gif_title = f"{year}{month}{day}.gif"
                print("Converting figures into gif…")
                convert_jpg_to_gif(save_dir,save_dir,gif_title)
                print("Gif is successfully made.")

            exe_jsttime += datetime.timedelta(minutes=10)

    print("Figures are successfully made.")



##############################################################################


# 以下で実行
startdate = datetime.datetime(2023,8,23,0,0)
enddate = datetime.datetime(2023,8,25,0,0)
elevation = False
# make_continuous_figures(startdate,enddate,elevation)
