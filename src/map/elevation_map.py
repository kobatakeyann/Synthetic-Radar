from io import StringIO
from math import atan, e, log, pi, tan

import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
import matplotlib.axes as maxes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import requests
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from elevation.coordinate_conversion import (
    lonlat_to_tile_coords,
    tile_coords_to_northwest_lonlat,
)
from map.lat_lon_formatter import format_latitude, format_longitude
from mpl_toolkits.axes_grid1 import make_axes_locatable


def load_gis(z, x1, x2, y1, y2):

    a = np.array([])
    for x in range(x1, x2 + 1):
        b = np.array([])
        for y in range(y1, y2 + 1):

            # 地形データを読み込む
            url = "http://cyberjapandata.gsi.go.jp/xyz/dem/{0}/{1}/{2}.txt".format(
                z, x, y
            )
            response = requests.get(url)
            if response.status_code == 404:
                # メッシュデータが無い区画は全ての点が0mのメッシュとしてとりあえず用意する
                Z = np.zeros((256, 256))
            else:
                # 標高値がない点はとりあえず0mに置換する
                #  maptxt = string.replace(response.text, u'e', u'0.0')
                maptxt = response.text.replace("e", "0.0")
                Z = pd.read_csv(StringIO(maptxt), header=None)
                Z = Z.values
                # Z = Z.transpose()
            if len(b) == 0:
                b = Z
            else:
                b = np.append(b, Z, 0)

        if len(a) == 0:
            a = b
        else:
            a = np.append(a, b, 1)

    return a


def make_elevation_map(
    lon_left,
    lon_right,
    lat_lower,
    lat_upper,
    z,
    deg_min_format=True,
    lon_interval=0.5,
    lat_interval=0.5,
    contour_min=150,
    contour_interval=100,
):

    # 緯度経度をタイル座標に変換して、標高データを取得
    x1, y1 = lonlat_to_tile_coords(lon_left, lat_upper, z)
    x2, y2 = lonlat_to_tile_coords(lon_right, lat_lower, z)
    Z = load_gis(z, x1, x2, y1, y2)

    # 県境データを取得
    shpfilename = shapereader.natural_earth(
        resolution="10m", category="cultural", name="admin_1_states_provinces"
    )
    provinces = shapereader.Reader(shpfilename).records()
    prefs = filter(
        lambda province: province.attributes["admin"] == "Japan", provinces
    )

    # 標高を描画するための座標を設定
    left_edge, upper_edge = tile_coords_to_northwest_lonlat(x1, y1, z)
    right_edge, lower_edge = tile_coords_to_northwest_lonlat(x2 + 1, y2 + 1, z)
    xlim = Z.shape[1]
    ylim = Z.shape[0]
    lon_grid = np.linspace(left_edge, right_edge, xlim)
    lat_grid = np.linspace(upper_edge, lower_edge, ylim)
    X, Y = np.meshgrid(lon_grid, lat_grid)  # X,Yグリッドを生成

    # 図のサイズの設定
    aspect = (lat_upper - lat_lower) / (lon_right - lon_left)
    figsize = (10, 9.5 * aspect)
    fig = plt.figure(figsize=figsize)
    proj = ccrs.PlateCarree()
    ax = fig.add_axes((0.08, 0.1, 0.83, 0.83), projection=proj)

    # 国境・県境を描画
    ax.coastlines(linewidths=1, resolution="10m")
    for pref in prefs:
        geometry = pref.geometry
        ax.add_geometries(
            [geometry],
            ccrs.PlateCarree(),
            facecolor="none",
            linestyle="-",
            linewidth=0.1,
        )

    # 等高線プロット
    levels_contour = np.arange(contour_min, 4001, contour_interval)
    cr = ax.contour(
        X,
        Y,
        Z,
        transform=ccrs.PlateCarree(),
        levels=levels_contour,
        linewidths=0.1,
        colors="black",
    )
    ax.clabel(cr, fmt="%.{0[0]}f".format([0]), fontsize=7)

    # 緯度経度の表示
    xloc = np.arange(0, 180 + 0.0001, lon_interval)
    yloc = np.arange(0, 90 + 0.0001, lat_interval)
    ax.set_xticks(xloc, crs=ccrs.PlateCarree())
    ax.set_yticks(yloc, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    if deg_min_format:
        ax.xaxis.set_major_formatter(format_longitude)
        ax.yaxis.set_major_formatter(format_latitude)

    # 描画範囲を設定
    ax.set_extent(
        (lon_left, lon_right, lat_lower, lat_upper), ccrs.PlateCarree()
    )
