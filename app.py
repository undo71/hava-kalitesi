from flask import Flask, render_template_string, request
import folium
import json

app = Flask(__name__)

SEHIRLER = {
    "İstanbul": {"lat": 41.01, "lon": 28.97, "AQI": 95, "PM25": 35, "PM10": 65, "CO2": 420, "nufus": 15840900},
    "Ankara": {"lat": 39.93, "lon": 32.85, "AQI": 88, "PM25": 28, "PM10": 55, "CO2": 415, "nufus": 5747325},
    "İzmir": {"lat": 38.42, "lon": 27.14, "AQI": 72, "PM25": 22, "PM10": 40, "CO2": 408, "nufus": 4394694},
    "Bursa": {"lat": 40.18, "lon": 29.06, "AQI": 105, "PM25": 42, "PM10": 78, "CO2": 425, "nufus": 3147818},
    "Van": {"lat": 38.50, "lon": 43.38, "AQI": 142, "PM25": 68, "PM10": 120, "CO2": 430, "nufus": 1136959},
    "Erzurum": {"lat": 39.90, "lon": 41.27, "AQI": 158, "PM25": 75, "PM10": 135, "CO2": 435, "nufus": 762321},
    "Diyarbakır": {"lat": 37.91, "lon": 40.22, "AQI": 118, "PM25": 52, "PM10": 95, "CO2": 428, "nufus": 1084000},
    "Konya": {"lat": 37.87, "lon": 32.49, "AQI": 78, "PM25": 25, "PM10": 48, "CO2": 412, "nufus": 2277017},
    "Kocaeli": {"lat": 40.77, "lon": 29.94, "AQI": 112, "PM25": 45, "PM10": 85, "CO2": 432, "nufus": 1830772},
    "Gaziantep": {"lat": 37.06, "lon": 37.38, "AQI": 98, "PM25": 38, "PM10": 72, "CO2": 422, "nufus": 2101000},
}

def aqi_bilgi(aqi):
    if aqi <= 50: return "İyi", "#00e400", "Hava kalitesi tatmin edici."
    elif aqi <= 100: return "Orta", "#ffff00", "Hassas gruplar için orta düzeyde risk."
    elif aqi <= 150: return "Hassas", "#ff7e00", "Hassas gruplar etkilenebilir."
    elif aqi <= 200: return "Sağlıksız", "#ff0000", "Herkes etkilenmeye başlayabilir."
    else: return "Tehlikeli", "#8f3f97", "Acil önlem alınmalı!"

def harita_olustur(secili=None):
    m = folium.Map(location=[39.0, 35.0], zoom_start=6)
    for sehir, veri in SEHIRLER.items():
        kategori, renk, _ = aqi_bilgi(veri["AQI"])
        kalinlik = 4 if sehir == secili else 1
        folium.CircleMarker(
            location=[veri["lat"], veri["lon"]],
            radius=veri["AQI"] / 8,
            color="black" if sehir == secili else renk,
            weight=kalinlik,
            fill=True,
            fill_color=renk,
            fill_opacity=0.85,
            popup=folium.Popup(f"<b>{sehir}</b><br>AQI: {veri['AQI']}<br>Kategori: {kategori}<br>PM2.5: {veri['PM25']} μg/m³", max_width=200),
            tooltip=f"{sehir}: AQI {veri['AQI']}"
        ).add_to(m)
    return m._repr_html_()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Hava Kalitesi</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial; background: #f0f4f8; }
        .header { background: #1565c0; color: white; padding: 20px 40px; }
        .header h1 { font-size: 22px; }
        .header p { opacity: 0.8; font-size: 13px; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .ozet-kart { background: white; border-radius: 10px; padding: 18px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .ozet-kart .sayi { font-size: 30px; font-weight: bold; }
        .ozet-kart .label { color: #888; font-size: 12px; margin-top: 4px; }
        .card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }
        .card h2 { color: #1565c0; margin-bottom: 15px; font-size: 17px; }
        .sehir-listesi { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
        .sehir-btn { padding: 10px; border-radius: 8px; text-align: center; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; text-decoration: none; display: block; }
        .sehir-btn:hover { transform: scale(1.05); border-color: #1565c0; }
        .sehir-btn.secili { border-color: #1565c0; box-shadow: 0 0 0 3px rgba(21,101,192,0.3); }
        .sehir-adi { font-weight: bold; font-size: 13px; }
        .sehir-aqi { font-size: 18px; font-weight: bold; margin-top: 3px; }
        .detay-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 15px; }
        .detay-kart { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
        .detay-kart .deger { font-size: 24px; font-weight: bold; color: #1565c0; }
        .detay-kart .birim { font-size: 11px; color: #888; }
        .aqi-bar { height: 12px; border-radius: 6px; background: linear-gradient(to right, #00e400, #ffff00, #ff7e00, #ff0000, #8f3f97); margin: 10px 0; position: relative; }
        .aqi-indicator { position: absolute; top: -4px; width: 20px; height: 20px; background: white; border: 3px solid #333; border-radius: 50%; transform: translateX(-50%); }
        .map-container iframe { width: 100%; height: 420px; border: none; border-radius: 8px; }
        .legend { display: flex; gap: 15px; flex-wrap: wrap; margin-top: 10px; }
        .legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; }
        .legend-dot { width: 12px; height: 12px; border-radius: 50%; }
        .saglik-oneri { padding: 12px 15px; border-radius: 8px; margin-top: 10px; font-size: 13px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌤️ Türkiye Hava Kalitesi Takip Sistemi</h1>
        <p>Şehir bazlı AQI, PM2.5, PM10 ve CO2 analizi</p>
    </div>

    <div class="container">

        <!-- Özet kartlar -->
        <div class="grid">
            <div class="ozet-kart">
                <div class="sayi" style="color:#ff0000">{{ en_kirli.isim }}</div>
                <div class="label">En Kirli Şehir (AQI: {{ en_kirli.aqi }})</div>
            </div>
            <div class="ozet-kart">
                <div class="sayi" style="color:#00aa00">{{ en_temiz.isim }}</div>
                <div class="label">En Temiz Şehir (AQI: {{ en_temiz.aqi }})</div>
            </div>
            <div class="ozet-kart">
                <div class="sayi" style="color:#ff7e00">{{ ortalama }}</div>
                <div class="label">Türkiye Ortalaması AQI</div>
            </div>
        </div>

        <!-- Şehir seçimi -->
        <div class="card">
            <h2>🏙️ Şehir Seçin</h2>
            <div class="sehir-listesi">
                {% for sehir, veri in sehirler.items() %}
                {% set kat, renk, acik = aqi_bilgi(veri.AQI) %}
                <a href="/sehir/{{ sehir }}" class="sehir-btn {{ 'secili' if sehir == secili else '' }}"
                   style="background: {{ renk }}22; border-color: {{ renk if sehir == secili else 'transparent' }}">
                    <div class="sehir-adi">{{ sehir }}</div>
                    <div class="sehir-aqi" style="color:{{ renk if renk != '#ffff00' else '#aa8800' }}">{{ veri.AQI }}</div>
                    <div style="font-size:10px; color:#666">{{ kat }}</div>
                </a>
                {% endfor %}
            </div>

            <div class="legend">
                <div class="legend-item"><div class="legend-dot" style="background:#00e400"></div> İyi (0-50)</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ffff00; border:1px solid #ccc"></div> Orta (51-100)</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ff7e00"></div> Hassas (101-150)</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ff0000"></div> Sağlıksız (151-200)</div>
                <div class="legend-item"><div class="legend-dot" style="background:#8f3f97"></div> Tehlikeli (200+)</div>
            </div>
        </div>

        {% if secili and secili_veri %}
        <!-- Seçili şehir detayı -->
        <div class="card">
            <h2>📊 {{ secili }} — Detaylı Analiz</h2>

            <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                <div style="font-size:48px; font-weight:bold; color:{{ secili_renk }}">{{ secili_veri.AQI }}</div>
                <div>
                    <div style="font-size:18px; font-weight:bold; color:{{ secili_renk }}">{{ secili_kat }}</div>
                    <div style="font-size:13px; color:#666;">{{ secili_acik }}</div>
                </div>
            </div>

            <div class="aqi-bar">
                <div class="aqi-indicator" style="left: {{ [secili_veri.AQI / 3, 95] | min }}%"></div>
            </div>

            <div class="detay-grid">
                <div class="detay-kart">
                    <div class="deger" style="color:purple">{{ secili_veri.PM25 }}</div>
                    <div class="birim">PM2.5 μg/m³</div>
                    <div style="font-size:11px; color:{{ '#dc3545' if secili_veri.PM25 > 35 else '#28a745' }}">
                        WHO sınırı: 35 μg/m³ {{ '⚠️ AŞILDI' if secili_veri.PM25 > 35 else '✅ Normal' }}
                    </div>
                </div>
                <div class="detay-kart">
                    <div class="deger" style="color:brown">{{ secili_veri.PM10 }}</div>
                    <div class="birim">PM10 μg/m³</div>
                    <div style="font-size:11px; color:{{ '#dc3545' if secili_veri.PM10 > 50 else '#28a745' }}">
                        WHO sınırı: 50 μg/m³ {{ '⚠️ AŞILDI' if secili_veri.PM10 > 50 else '✅ Normal' }}
                    </div>
                </div>
                <div class="detay-kart">
                    <div class="deger" style="color:#1565c0">{{ secili_veri.CO2 }}</div>
                    <div class="birim">CO2 ppm</div>
                    <div style="font-size:11px; color:#888">Normal: 400-450 ppm</div>
                </div>
                <div class="detay-kart">
                    <div class="deger">{{ "{:,}".format(secili_veri.nufus) }}</div>
                    <div class="birim">Nüfus</div>
                </div>
                <div class="detay-kart">
                    <div class="deger" style="color:{{ '#dc3545' if secili_veri.PM25 > 35 else '#28a745' }}">
                        {{ ((secili_veri.PM25 / 35) * 100) | int }}%
                    </div>
                    <div class="birim">WHO PM2.5 Sınırı Kullanımı</div>
                </div>
                <div class="detay-kart">
                    <div class="deger" style="color:{{ '#dc3545' if secili_veri.PM10 > 50 else '#28a745' }}">
                        {{ ((secili_veri.PM10 / 50) * 100) | int }}%
                    </div>
                    <div class="birim">WHO PM10 Sınırı Kullanımı</div>
                </div>
            </div>

            <div class="saglik-oneri" style="background:{{ secili_renk }}22; border-left: 4px solid {{ secili_renk }}">
                <strong>💊 Sağlık Önerisi:</strong>
                {% if secili_veri.AQI <= 50 %}
                    Hava kalitesi iyi. Dış mekan aktiviteleri için uygun.
                {% elif secili_veri.AQI <= 100 %}
                    Hassas gruplar (astım, kalp hastaları) dikkatli olmalı.
                {% elif secili_veri.AQI <= 150 %}
                    Uzun süreli dış mekan aktivitelerini azaltın. Maske takın.
                {% else %}
                    Dış mekandan kaçının! Pencere açmayın. Hava temizleyici kullanın.
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- Harita -->
        <div class="card">
            <h2>🗺️ Hava Kalitesi Haritası</h2>
            {{ harita | safe }}
        </div>

    </div>
</body>
</html>
"""

@app.route("/")
def anasayfa():
    en_kirli = max(SEHIRLER.items(), key=lambda x: x[1]["AQI"])
    en_temiz = min(SEHIRLER.items(), key=lambda x: x[1]["AQI"])
    ort = sum(v["AQI"] for v in SEHIRLER.values()) / len(SEHIRLER)
    harita = harita_olustur()
    return render_template_string(HTML,
        sehirler=SEHIRLER, secili=None, secili_veri=None,
        secili_renk=None, secili_kat=None, secili_acik=None,
        en_kirli={"isim": en_kirli[0], "aqi": en_kirli[1]["AQI"]},
        en_temiz={"isim": en_temiz[0], "aqi": en_temiz[1]["AQI"]},
        ortalama=f"{ort:.0f}", harita=harita,
        aqi_bilgi=aqi_bilgi)

@app.route("/sehir/<sehir_adi>")
def sehir(sehir_adi):
    en_kirli = max(SEHIRLER.items(), key=lambda x: x[1]["AQI"])
    en_temiz = min(SEHIRLER.items(), key=lambda x: x[1]["AQI"])
    ort = sum(v["AQI"] for v in SEHIRLER.values()) / len(SEHIRLER)
    harita = harita_olustur(sehir_adi)
    veri = SEHIRLER.get(sehir_adi)
    kat, renk, acik = aqi_bilgi(veri["AQI"]) if veri else ("", "", "")
    return render_template_string(HTML,
        sehirler=SEHIRLER, secili=sehir_adi, secili_veri=veri,
        secili_renk=renk, secili_kat=kat, secili_acik=acik,
        en_kirli={"isim": en_kirli[0], "aqi": en_kirli[1]["AQI"]},
        en_temiz={"isim": en_temiz[0], "aqi": en_temiz[1]["AQI"]},
        ortalama=f"{ort:.0f}", harita=harita,
        aqi_bilgi=aqi_bilgi)

if __name__ == "__main__":
    app.run(debug=True)