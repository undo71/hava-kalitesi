# hava-kalitesi
# Turkiye Hava Kalitesi Takip Sistemi

Turkiye'nin buyuk sehirlerindeki hava kalitesini analiz eden,
interaktif harita ve detayli istatistikler sunan web uygulamasi.

## Motivasyon

Turkiye'de hava kirliligi ciddi bir halk sagligi sorunu.
Ozellikle dogu sehirlerinde kis aylarinda komur yakimi nedeniyle
hava kalitesi WHO sinirlarini kat kat asiyor.
Van ve Erzurum gibi sehirlerde yasayan insanlar farkinda olmadan
sagliklarini tehlikeye atiyor. Bu proje bu farkindaligi yaratmayi amacliyor.

## Ozellikler

- 10 buyuk Turkiye sehri icin hava kalitesi analizi
- AQI, PM2.5, PM10 ve CO2 verileri
- Interaktif Turkiye haritasi (renk kodlu risk gostergesi)
- Sehir bazli detayli analiz sayfasi
- WHO sinir deger karsilastirmasi
- Saglik onerileri sistemi
- 4 farkli grafik (AQI, PM2.5, PM10, dagilim)

## Sonuclar

En kirli sehir: Erzurum (AQI: 158 - Sagliksiz)
En temiz sehir: Izmir (AQI: 72 - Orta)
Turkiye ortalamasi: AQI 107 (Hassas)

Sehinlerin %50si WHO PM2.5 sinirini asiyor!
Van PM2.5: 68 ug/m3 (WHO siniri: 35 ug/m3 - 2x ASILDI)
Erzurum PM2.5: 75 ug/m3 (WHO siniri: 35 ug/m3 - 2.1x ASILDI)

## AQI Kategorileri

- 0-50: Iyi (yesil)
- 51-100: Orta (sari)
- 101-150: Hassas (turuncu)
- 151-200: Sagliksiz (kirmizi)
- 200+: Tehlikeli (mor)

## Kullanilan Teknolojiler

- Python
- Flask (web framework)
- Folium (interaktif harita)
- Pandas + Matplotlib + Seaborn (veri analizi)

## Nasil Calistirilir

pip install flask folium pandas matplotlib seaborn
python app.py

Tarayicida ac: http://127.0.0.1:5000

## Gelistirici

Van dogumlu bir yazilim gelistirici olarak bu projeyi
kendi sehrimde yasadigim hava kirliligi sorununa dikkat cekmek icin gelistirdim.
MIT hedefli proje portfolyosu icin gelistirilmistir.
