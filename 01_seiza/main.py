from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
import matplotlib.pyplot as plt
import cv2
import numpy as np
from datetime import datetime

# --- 設定 ---
# 撮影地（高嶺展望台付近）
location = EarthLocation(lat=35.3711*u.deg, lon=137.7482*u.deg, height=1600*u.m)

# 撮影日時（JST）
time = Time('2025-10-13 10:21:00')  # UTCに変換（JST-9時間）

# 撮影方向（方位角180度：南、仰角5度）
az = 180 * u.deg
alt = 5 * u.deg

# 視野角（35mm換算で計算、36mm焦点距離）
fov_deg = 40  # おおよその視野角（水平）を仮定

# 画像読み込み
img = cv2.imread("C:\\Users\\d503i\\Desktop\\100NCD90\\100NCD90\\100NCD90\\DSC_0293.JPG")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img.shape

# 星のカタログから明るい星を取得
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = 1000
stars = Vizier(columns=["RA_ICRS", "DEJ2000", "Vmag"]).query_constraints(Vmag="<5", catalog="I/239/hip_main")[0]

# 星ごとの天球座標→地平座標→画像座標へ変換
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img_rgb)
ax.axis('off')

for star in stars:
    ra = star["RA_ICRS"]
    dec = star["DEJ2000"]
    vmag = star["Vmag"]

    coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg)
    altaz = coord.transform_to(AltAz(obstime=time, location=location))

    # 星が地平線より上にあるか確認
    if altaz.alt.deg > 0:
        delta_az = (altaz.az - az).wrap_at(180*u.deg).deg
        delta_alt = altaz.alt - alt
        if abs(delta_az) < fov_deg/2 and abs(delta_alt.deg) < fov_deg/2:
            # 星の位置を画像座標に変換（簡易的な線形マッピング）
            x = int(w / 2 + (delta_az / (fov_deg/2)) * (w / 2))
            y = int(h / 2 - (delta_alt.deg / (fov_deg/2)) * (h / 2))

            ax.plot(x, y, 'o', color='yellow', markersize=max(1, 6 - vmag/1.5))
            ax.text(x+3, y, f"{ra:.1f}", fontsize=6, color='white')  # 本来は星の名前を出したいところ

plt.title("星座・星の表示")
plt.show()


from astroquery.vizier import Vizier

# 星のデータ取得
Vizier.ROW_LIMIT = 1000
catalog = Vizier(columns=["**"])  # すべてのカラムを取得
result = catalog.query_constraints(Vmag="<5", catalog="I/239/hip_main")

# 結果が存在するかチェック
if not result:
    raise ValueError("星表の取得に失敗しました。インターネット接続を確認してください。")

stars = result[0]

# 利用可能なカラム名を表示（デバッグ用）
print("取得されたカラム名：", stars.colnames)

# 正しいカラム名に修正（例：RA_ICRS, DE_ICRS など）
ra_col = "RA_ICRS"
dec_col = "DE_ICRS"
vmag_col = "Vmag"

# 例：1つ目の星を確認
print("1つ目の星のRA（赤経）:", stars[0][ra_col])
