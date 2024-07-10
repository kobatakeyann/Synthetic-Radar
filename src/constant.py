import numpy as np

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


# 描画領域の設定
LON_LEFT, LON_RIGHT = 129.97696, 130.7594
LAT_BOTTOM, LAT_TOP = 33.006493, 33.797226

# colorbarの設定
LABEL_LOCATION = 3
LABEL_SIZE = 12
# LEVELS = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45])
LEVELS = np.arange(1, 51, 5)

# 標高データの設定
ELEVATION = True
ELEVATION_MIN = 150
ELEVATION_INTERVAL = 100
ZOOM_LEVEL = 8


# 緯度経度目盛りの設定
IS_DEG_MIN_FORMAT = False
TICKS_INTERVAL = 0.1

# タイトルのfontsize
TITLE_FONTSIZE = 20
