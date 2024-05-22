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

