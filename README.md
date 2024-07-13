# Synthetic Radar
10分毎の雨雲レーダー図を作成します。

![](sample_image.jpg)


## 仮想環境のactivate
```
python -m venv .venv
```

```
#Unix
source .venv/bin/activate
#Windows
source .venv/Scripts/activate
```

## Installation
パッケージのインストール
```
pip install -r requirements.txt
```


## Usage
`/src/constant.py`で描画範囲等を設定
```
python src/main.py
```
で画像やGifを作成します。
作成された画像は `/img`下に出力されます。
 
# Features
 
Physics_S
 
 
# Note
 
I don't test environments under Linux and Mac.
er : https://twitter.com/Cpp_Learning
 
# License
 
"Physics_Sim_Py" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).