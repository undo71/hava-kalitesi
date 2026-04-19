import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from collections import defaultdict

# Türkiye şehirleri hava kalitesi verisi (AQI - Hava Kalitesi İndeksi)
veri = {
    "sehir": ["İstanbul", "Ankara", "İzmir", "Bursa", "Van", "Erzurum", 
              "Diyarbakır", "Konya", "Kocaeli", "Gaziantep"],
    "lat": [41.01, 39.93, 38.42, 40.18, 38.50, 39.90, 37.91, 37.87, 40.77, 37.06],
    "lon": [28.97, 32.85, 27.14, 29.06, 43.38, 41.27, 40.22, 32.49, 29.94, 37.38],
    "AQI": [95, 88, 72, 105, 142, 158, 118, 78, 112, 98],
    "PM25": [35, 28, 22, 42, 68, 75, 52, 25, 45, 38],
    "PM10": [65, 55, 40, 78, 120, 135, 95, 48, 85, 72],
    "CO2": [420, 415, 408, 425, 430, 435, 428, 412, 432, 422],
    "nufus": [15840900, 5747325, 4394694, 3147818, 1136959, 762321, 1084000, 2277017, 1830772, 2101000],
}

df = pd.DataFrame(veri)

# AQI kategorisi
def aqi_kategori(aqi):
    if aqi <= 50: return "İyi", "#00e400"
    elif aqi <= 100: return "Orta", "#ffff00"
    elif aqi <= 150: return "Hassas", "#ff7e00"
    elif aqi <= 200: return "Sağlıksız", "#ff0000"
    else: return "Tehlikeli", "#8f3f97"

df["kategori"] = df["AQI"].apply(lambda x: aqi_kategori(x)[0])
df["renk"] = df["AQI"].apply(lambda x: aqi_kategori(x)[1])

print("=== Türkiye Hava Kalitesi Analizi ===")
print(df[["sehir", "AQI", "PM25", "kategori"]].to_string(index=False))
print()
print(f"En kirli şehir: {df.loc[df['AQI'].idxmax(), 'sehir']} (AQI: {df['AQI'].max()})")
print(f"En temiz şehir: {df.loc[df['AQI'].idxmin(), 'sehir']} (AQI: {df['AQI'].min()})")
print(f"Türkiye ortalaması: {df['AQI'].mean():.1f}")

# Grafik
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Türkiye Hava Kalitesi Analizi", fontsize=16, fontweight="bold")

# AQI grafiği
renkler = df["renk"].tolist()
axes[0,0].barh(df["sehir"], df["AQI"], color=renkler, edgecolor="gray")
axes[0,0].axvline(x=100, color="red", linestyle="--", label="Güvenli sınır")
axes[0,0].set_title("Şehirlere Göre AQI")
axes[0,0].set_xlabel("AQI")
axes[0,0].legend()

# PM2.5 grafiği
axes[0,1].bar(df["sehir"], df["PM25"], color="purple", alpha=0.7)
axes[0,1].axhline(y=35, color="red", linestyle="--", label="WHO sınırı")
axes[0,1].set_title("PM2.5 Partiküller (μg/m³)")
axes[0,1].tick_params(axis="x", rotation=45)
axes[0,1].legend()

# PM10 grafiği
axes[1,0].bar(df["sehir"], df["PM10"], color="brown", alpha=0.7)
axes[1,0].axhline(y=50, color="red", linestyle="--", label="WHO sınırı")
axes[1,0].set_title("PM10 Partiküller (μg/m³)")
axes[1,0].tick_params(axis="x", rotation=45)
axes[1,0].legend()

# Kategori dağılımı
kategori_sayisi = df["kategori"].value_counts()
axes[1,1].pie(kategori_sayisi.values, labels=kategori_sayisi.index,
              autopct="%1.0f%%", colors=["#ff0000", "#ff7e00", "#ffff00", "#00e400"])
axes[1,1].set_title("Hava Kalitesi Dağılımı")

plt.tight_layout()
plt.savefig("hava_grafik.png", dpi=150)
plt.show()
print("Grafik kaydedildi!")

# Harita
harita = folium.Map(location=[39.0, 35.0], zoom_start=6)
for _, satir in df.iterrows():
    folium.CircleMarker(
        location=[satir["lat"], satir["lon"]],
        radius=satir["AQI"] / 10,
        color=satir["renk"],
        fill=True,
        fill_color=satir["renk"],
        fill_opacity=0.8,
        popup=f"{satir['sehir']}\nAQI: {satir['AQI']}\nKategori: {satir['kategori']}\nPM2.5: {satir['PM25']}"
    ).add_to(harita)

harita.save("hava_haritasi.html")
print("Harita kaydedildi!")