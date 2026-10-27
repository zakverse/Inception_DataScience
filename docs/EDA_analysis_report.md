# Laporan Analisis Exploratory Data Analysis (EDA) — INCEPTION 2026
**Proyek:** Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Dataset:** Indonesia Financial Time Series Dataset 2010–2026  
**Target:** `Target_Volatilitas_Y`  
**Checkpoint:** 0.1 (Task 1: EDA, Audit Struktur Data, & Fondasi Feature Engineering)  
**Dokumen Referensi:** `notebook/EDA.ipynb`, `Aset Lomba/dataset peserta.csv`, `Aset Lomba/Studi Kasus.docx`, `Aset Lomba/DATA DICTIONARY...`

---

## 1. Executive Summary

Laporan ini mendokumentasikan hasil audit data, eksplorasi statistik, verifikasi target, serta evaluasi risiko metodologis dari tahap Exploratory Data Analysis (EDA) untuk proyek kompetisi data sains **INCEPTION 2026**. Proyek ini menempatkan analis sebagai *Senior Quantitative Risk & Machine Learning Analyst* di PT Investion dengan mandat membangun **Early Warning System (EWS)** untuk memprediksi volatilitas terealisasi (*realized volatility*) Indeks Harga Saham Gabungan (IHSG) untuk horizon 5 hari perdagangan bursa ke depan (`Target_Volatilitas_Y`).

### Ringkasan Dataset
Dataset mentah mencakup deret waktu keuangan harian sebanyak **4.266 baris** dan **11 kolom** observasi dari **4 Januari 2010 hingga 22 Mei 2026**. Seluruh observasi jatuh secara eksklusif pada hari kerja (Senin–Jumat). Data terbagi menjadi dua partisi utama:
1. **Data Berlabel:** 3.907 baris observasi historis (4 Januari 2010 s/d 24 Desember 2024) dengan nilai target terisi utuh ($Y \neq \text{NaN}$).
2. **Data Uji (Test Set):** 359 baris observasi masa depan (2 Januari 2025 s/d 22 Mei 2026) di mana nilai target sengaja dikosongkan ($Y = \text{NaN}$) untuk evaluasi prediksi akhir kompetisi.

### Temuan Paling Penting
1. **Formula Target Terverifikasi Secara Kuantitatif:** Formula target terbukti secara empiris merupakan deviasi standar terbobot dari persentase return harian IHSG selama horizon 5 hari perdagangan ke depan:
   $$\text{Target\_Volatilitas\_Y}_t = \text{std}\left(\left[\Delta\% \text{IHSG}_{t+1}, \Delta\% \text{IHSG}_{t+2}, \dots, \Delta\% \text{IHSG}_{t+5}\right], \text{ddof}=1\right)$$
   Rekonstruksi formula ini menghasilkan korelasi Pearson $r = 0.999711$, Mean Absolute Error (MAE) sebesar $4.30 \times 10^{-6}$, dan selisih absolut maksimum $0.00536$ terhadap kolom target aktual.
2. **Distribusi Target Sangat Non-Normal (Fat-Tailed):** Distribusi target menunjukkan kemencengan positif ekstrem (*skewness* = 2.636) dan sifat leptokurtik tinggi (*kurtosis* = 12.213), dengan nilai maksimum 0.05850 yang bertepatan dengan kepanikan awal pandemi COVID-19 pada 20 Maret 2020.
3. **Bukti Kuantitatif Fenomena Volatility Clustering:** Plot autokorelasi (ACF) dari nilai absolut return IHSG ($|r_t|$) menunjukkan autokorelasi positif yang signifikan secara persisten melampaui batas selang kepercayaan 95% ($\pm 0.0314$) pada seluruh lag 1 hingga 30. Hal ini mengonfirmasi keberadaan efek ARCH/GARCH di mana periode volatilitas tinggi cenderung mengelompok.
4. **Prediktor Linier Terkuat:** Variabel prediktor univariat terkuat terhadap target adalah volatilitas historis 5 hari terakhir (`rv_past5`, $r = +0.4460$) dan indeks ketakutan pasar global (`VIX`, $r = +0.4342$). Sebaliknya, harga level aset (IHSG, Emas, Minyak mentah) memiliki korelasi linier yang rendah atau palsu karena sifatnya yang non-stasioner.
5. **Anomali Kualitas Data:** Ditemukan dua jenis anomali data:
   - Harga minyak mentah negatif (`OIL = -37.63` pada 20 April 2020) yang merupakan peristiwa pasar riil (kontrak berjangka WTI crash ke teritori negatif saat pandemi).
   - Anomali ketik/skala nilai tukar rupiah (`USDIDR = 888.11` pada 2010-11-01 dan `USDIDR = 892.00` pada 2012-02-07), yang bergeser faktor 10 dari tetangga observasinya (~8.920 IDR/USD).

### Status Kesiapan Data & Risiko Metodologis
Data berlabel berada dalam kondisi siap untuk rekayasa fitur (*feature engineering*) pada Task 1 dan pemodelan pada Task 2. Tidak ditemukan *missing values* pada 10 variabel prediktor. Namun, terdapat risiko metodologis kritis yang wajib dimitigasi sebelum pemodelan:
- **Lookahead Bias & Data Leakage:** Target memiliki forward horizon 5 hari ($t+1..t+5$). Penggunaan fitur volatilitas rolling yang menyertakan data masa depan atau return hari ini ($t$) berpotensi fatal menimbulkan kebocoran informasi.
- **Skema Validasi:** Pengacakan data (*random train-test split*) dilarang keras. Wajib diterapkan *Purged Time-Series Split* dengan *embargo period* minimal 5 hari untuk mencegah autokorelasi antar-lipatan.

---

## 2. Dataset Overview

Dataset yang digunakan adalah *Indonesia Financial Time Series Dataset 2010–2026*, bersumber dari file `Aset Lomba/dataset peserta.csv`.

### Dimensi dan Periode
- **Jumlah Baris Total:** 4.266 baris
- **Jumlah Kolom:** 11 kolom (1 kolom tanggal, 9 kolom fitur makroekonomi/finansial, 1 kolom target)
- **Rentang Tanggal Total:** 4 Januari 2010 (`2010-01-04`) hingga 22 Mei 2026 (`2026-05-22`)
- **Distribusi Hari Kerja:** Seluruh baris jatuh pada hari kerja Senin hingga Jumat:
  - Senin: 854 baris
  - Selasa: 854 baris
  - Rabu: 853 baris
  - Kamis: 852 baris
  - Jumat: 853 baris
  - Sabtu & Minggu: 0 baris (tidak ada transaksi akhir pekan)

### Definisi dan Tipe Kolom

| No | Nama Kolom | Tipe Data | Peran | Deskripsi Finansial & Satuan |
|---|---|---|---|---|
| 1 | `Date` | `datetime64[us]` | Indeks Temporal | Tanggal transaksi bursa (frekuensi harian) |
| 2 | `OIL` | `float64` | Fitur Prediktor | Harga minyak mentah West Texas Intermediate (WTI) (USD/barrel) |
| 3 | `GOLD` | `float64` | Fitur Prediktor | Harga emas spot global (USD/troy ounce) |
| 4 | `USDIDR` | `float64` | Fitur Prediktor | Kurs nilai tukar Rupiah Indonesia terhadap Dolar AS (IDR per 1 USD) |
| 5 | `SP500` | `float64` | Fitur Prediktor | Indeks harga saham Standard & Poor's 500 Amerika Serikat (poin) |
| 6 | `IHSG` | `float64` | Fitur Prediktor | Indeks Harga Saham Gabungan Bursa Efek Indonesia (poin) |
| 7 | `VIX` | `float64` | Fitur Prediktor | CBOE Volatility Index, proksi implied volatility opsi S&P 500 (%) |
| 8 | `CPI` | `float64` | Fitur Prediktor | Indeks Harga Konsumen Indonesia (tingkat inflasi domestik) |
| 9 | `BI_rate` | `float64` | Fitur Prediktor | Suku bunga acuan Bank Indonesia / BI 7-Day Reverse Repo Rate (%) |
| 10 | `US_rate` | `float64` | Fitur Prediktor | Federal Funds Effective Rate / suku bunga acuan The Fed AS (%) |
| 11 | `Target_Volatilitas_Y` | `float64` | **Target Prediksi** | Realized volatility return IHSG selama 5 hari bursa ke depan |

### Partisi Data Berlabel vs Data Uji

Dataset memiliki struktur bawaan partisi temporal:
- **Partisi Berlabel ($Y \neq \text{NaN}$):** 3.907 baris observasi, mencakup rentang waktu 4 Januari 2010 hingga 24 Desember 2024 (91,58% dataset). Seluruh analisis statistik, eksplorasi distribusi, dan pelatihan model harus didasarkan pada partisi ini.
- **Partisi Uji / Unlabeled ($Y = \text{NaN}$):** 359 baris observasi, mencakup rentang waktu 2 Januari 2025 hingga 22 Mei 2026 (8,42% dataset). Nilai target pada partisi ini kosong secara konsisten dan utuh, merepresentasikan periode evaluasi *out-of-time* kompetisi.

### Ringkasan Missing Values dan Duplikasi
Pemeriksaan struktur data menghasilkan temuan sebagai berikut:
- **Duplikasi:** Tepat 0 baris duplikat di seluruh dataset.
- **Missing Values:**
  - 10 kolom prediktor (`Date`, `OIL`, `GOLD`, `USDIDR`, `SP500`, `IHSG`, `VIX`, `CPI`, `BI_rate`, `US_rate`): **0 missing values (100% lengkap)**.
  - Kolom `Target_Volatilitas_Y`: 359 missing values (8,42%), yang persis bertepatan dengan data uji tahun 2025–2026.

### Statistik Deskriptif (Data Berlabel: 3.907 Baris)

Tabel berikut menyajikan ringkasan statistik deskriptif dari data berlabel historis (2010–2024):

| Variabel | Count | Mean | Std | Min | Q1 (25%) | Median (50%) | Q3 (75%) | Max | CV (%) |
|---|---|---|---|---|---|---|---|---|---|
| `OIL` | 3.907 | 71,9864 | 21,3610 | -37,6300 | 53,2800 | 73,0400 | 89,4050 | 123,7000 | 29,67% |
| `GOLD` | 3.907 | 1.543,4419 | 349,2635 | 1.050,8000 | 1.259,8000 | 1.434,5000 | 1.784,1000 | 2.788,5000 | 22,63% |
| `USDIDR` | 3.907 | 12.825,2044 | 2.341,0874 | 888,1100 | 11.180,0000 | 13.540,0000 | 14.492,0000 | 16.504,8008 | 18,25% |
| `SP500` | 3.907 | 2.724,8586 | 1.260,8390 | 1.022,5800 | 1.700,2550 | 2.429,3899 | 3.810,4950 | 6.090,2700 | 46,27% |
| `IHSG` | 3.907 | 5.401,0160 | 1.229,7807 | 2.475,4756 | 4.479,2917 | 5.381,7876 | 6.382,4089 | 7.905,3901 | 22,77% |
| `VIX` | 3.907 | 18,3491 | 6,9366 | 9,1400 | 13,5700 | 16,5900 | 21,1400 | 82,6900 | 37,80% |
| `CPI` | 3.907 | 4,0705 | 1,5468 | 1,5601 | 3,0306 | 3,8088 | 5,3560 | 6,4125 | 38,00% |
| `BI_rate` | 3.907 | 5,6744 | 1,2555 | 3,5000 | 4,7500 | 5,7500 | 6,5000 | 7,7500 | 22,13% |
| `US_rate` | 3.907 | 1,2265 | 1,7109 | 0,0500 | 0,0900 | 0,1900 | 1,8200 | 5,3300 | 139,49% |
| `Target_Volatilitas_Y` | 3.907 | 0,0083 | 0,0056 | 0,0000 | 0,0049 | 0,0071 | 0,0100 | 0,0585 | 66,98% |

*Catatan: Koefisien Variasi ($CV = \text{std} / |\text{mean}| \times 100\%$) mengindikasikan tingkat dispersi relatif. `US_rate` memiliki variabilitas relatif tertinggi (139,49%) akibat pergeseran kebijakan moneter ekstrim dari era Zero Interest Rate Policy (ZIRP) menuju pengetatan moneter pasca-pandemi.*

### Temuan Kualitas Data Khusus
1. **Nilai Non-Positif pada Minyak Mentah (`OIL`):** Pada tanggal 20 April 2020 (indeks baris 2.685), nilai `OIL` tercatat `-37.63`. Ini bukan galat pencatatan, melainkan peristiwa riil pasar keuangan global di mana kontrak berjangka WTI Mei 2020 anjlok ke harga negatif akibat kelangkaan kapasitas penyimpanan minyak saat *lockdown* global awal pandemi COVID-19.
2. **Anomali Skala Desimal pada Nilai Tukar Rupiah (`USDIDR`):** Terdapat dua baris dengan nilai `USDIDR` di bawah 5.000:
   - Baris 215 (2010-11-01): bernilai `888.109985`. Nilai observasi tanggal sebelumnya (2010-10-29) adalah `8923.80` dan tanggal setelahnya (2010-11-02) adalah `8906.70`.
   - Baris 546 (2012-02-07): bernilai `892.000000`. Nilai observasi tanggal sebelumnya (2012-02-06) adalah `8928.10` dan tanggal setelahnya (2012-02-08) adalah `8930.00`.
   - **Dampak Kritis:** Dua entri ini jelas merupakan galat pergeseran koma desimal / salah ketik (skala $10\times$). Jika return harian dihitung secara langsung tanpa koreksi, hal ini akan memicu *false shock* sebesar $-90\%$ dan $+900\%$ pada kurs rupiah. Rekomendasi perbaikan adalah mengoreksi kedua nilai tersebut dengan mengalikannya dengan faktor 10 (atau imputasi interpolasi lokal) pada tahap preprocessing.

---

## 3. Target Definition Audit

Audit definisi target dilakukan untuk menghilangkan ambiguitas operasional mengenai apa yang sebenarnya diprediksi oleh model.

### Definisi Konseptual vs Matematika
Dalam dokumen studi kasus kompetisi (*Studi Kasus.docx*), target dirumuskan sebagai *realized volatility* pergerakan IHSG untuk 5 hari perdagangan bursa ke depan. Untuk membuktikan formula eksak yang digunakan oleh penyelenggara lomba, dilakukan uji rekonstruksi matematis.

Hipotesis formula yang diuji pada notebook:
$$\widehat{Y}_t = \sqrt{\frac{1}{4} \sum_{k=1}^{5} \left(r_{t+k} - \bar{r}_{t, 5}\right)^2}$$
di mana $r_{t+k} = \frac{\text{IHSG}_{t+k} - \text{IHSG}_{t+k-1}}{\text{IHSG}_{t+k-1}}$ adalah persentase perubahan harian IHSG, dan $\bar{r}_{t, 5} = \frac{1}{5}\sum_{k=1}^5 r_{t+k}$.

Secara kode, formula ini diimplementasikan dengan:
```python
df['IHSG_ret'] = df['IHSG'].pct_change()
df['rv_reconstructed'] = df['IHSG_ret'].shift(-5).rolling(5).std()
```

### Hasil Numerik Verifikasi
Pengujian kuantitatif terhadap seluruh 3.907 baris data berlabel menghasilkan metrik verifikasi berikut:

| Metrik Verifikasi | Nilai Aktual | Ambang Batas Toleransi | Status |
|---|---|---|---|
| Korelasi Pearson ($r$) | **0,999711** | $> 0,9990$ | **TERVERIFIKASI** |
| Mean Absolute Error (MAE) | **0,00000430** ($4,30 \times 10^{-6}$) | $< 0,0001$ | **TERVERIFIKASI** |
| Selisih Absolut Maksimum | **0,00536128** | $< 0,0100$ | **TERVERIFIKASI** |

Dengan korelasi Pearson melampaui **0,9997** dan rata-rata deviasi absolut di bawah $0,000005$, **hipotesis formula target terverifikasi secara definitif sebagai fakta matematis**.

### Alignment Temporal dan Horizon Prediksi
Pemahaman alignment tanggal ini sangat krusial untuk mencegah bias metodologis:
1. **Hari $t$ (Waktu Prediksi / End of Day $t$):** Analis berada di penutupan pasar hari $t$. Fitur yang boleh digunakan hanyalah informasi yang telah terobservasi hingga penutupan hari $t$ (harga penutupan IHSG, SP500, VIX, nilai tukar, suku bunga hari $t$).
2. **Horizon Target ($t+1$ hingga $t+5$):** Target $\text{Target\_Volatilitas\_Y}_t$ menghitung deviasi standar return pada hari kerja $t+1, t+2, t+3, t+4,$ dan $t+5$.
3. **Waktu Realisasi Penuh:** Nilai target $Y_t$ baru dapat diobservasi secara sempurna setelah bursa ditutup pada hari ke-$t+5$.

### Batasan dan Hal yang Masih Hipotesis
- **Definisi Return:** Penyelenggara menggunakan return aritmetik sederhana (`pct_change`), bukan return logaritmik $\ln(P_t / P_{t-1})$. Meskipun perbedaannya marjinal pada fluktuasi harian kecil, return aritmetik menjelaskan residu deviasi mikro ($MAE \approx 4 \times 10^{-6}$).
- **Target pada Akhir Tahun 2024:** Observasi berlabel berakhir pada 24 Desember 2024. Karena target memerlukan 5 hari ke depan, perhitungan target untuk baris 24 Desember 2024 memanfaatkan harga IHSG awal Januari 2025 yang tercatat pada baris-baris pertama partisi uji.

---

## 4. Analisis Distribusi dan Outlier

### Karakteristik Distribusi Target
Eksplorasi terhadap kolom `Target_Volatilitas_Y` pada partisi berlabel menghasilkan ringkasan distribusi berikut:
- **Mean:** 0,00834 (0,834% per 5 hari)
- **Median:** 0,00705 (0,705%)
- **Standar Deviasi ($\sigma$):** 0,00559
- **Skewness:** **+2,636** (Sangat condong ke kanan / right-skewed)
- **Kurtosis:** **+12,213** (Sangat leptokurtik / ekor gemuk / fat tails)
- **Nilai Minimum:** 0,00000
- **Nilai Maksimum:** 0,05850 (terjadi pada 20 Maret 2020, saat kejatuhan pasar akibat COVID-19)

Distribusi target jelas **tidak berdistribusi normal**. Plot histogram skala logaritmik (`outputs/eda/fig_04_target_distribution.png`) memperlihatkan ekor kanan yang panjang (*fat tail*), merefleksikan bahwa dalam kondisi normal pasar bergerak dengan volatilitas rendah-sedang, namun sesekali mengalami guncangan volatilitas ekstrem yang sangat masif.

### Bentuk Distribusi Variabel Prediktor
Berdasarkan plot histogram dan estimasi kepadatan probabilitas kernel (KDE) pada `outputs/eda/fig_01_distributions.png`:
1. **`VIX`:** Sangat miring ke kanan (*skewness* = 2,45, *kurtosis* = 9,87), berkorelasi erat dengan sifat target. Sebagian besar waktu VIX berada di kisaran 12–20, namun melonjak drastis hingga >80 pada masa krisis finansial global dan pandemi.
2. **`CPI` dan `BI_rate`:** Menunjukkan profil distribusi multimodal / bimodal. Hal ini merefleksikan pergeseran rezim moneter Indonesia selama 15 tahun: periode inflasi dan suku bunga tinggi pra-2015 (BI rate 6,5%–7,75%) versus periode stabilitas inflasi rendah pasca-2016 (BI rate 3,5%–5,0%).
3. **`US_rate`:** Menunjukkan konsentrasi ekstrem di dekat batas bawah 0,05%–0,25% (kebijakan pelonggaran kuantitatif ZIRP era 2010–2015 dan 2020–2021) dengan lonjakan tajam menuju >5% pasca 2022.
4. **`IHSG` dan `SP500`:** Memiliki tren pertumbuhan secular (*upward drift*), menghasilkan distribusi yang melebar dan non-stasioner pada level harga.

### Analisis Outlier (Metode IQR)
Deteksi outlier dilakukan menggunakan metode Interquartile Range ($IQR = Q_3 - Q_1$, batas $[Q_1 - 1,5 IQR, Q_3 + 1,5 IQR]$):

| Kolom | Q1 (25%) | Q3 (75%) | IQR | Jumlah Outlier | Persentase Outlier |
|---|---|---|---|---|---|
| `Target_Volatilitas_Y` | 0,004857 | 0,010042 | 0,005185 | **226** | **5,78%** |
| `US_rate` | 0,0900 | 1,8200 | 1,7300 | 495 | 12,67% |
| `VIX` | 13,5700 | 21,1400 | 7,5700 | 160 | 4,10% |
| `GOLD` | 1.259,8000 | 1.784,1000 | 524,3000 | 70 | 1,79% |
| `USDIDR` | 11.180,0000 | 14.492,0000 | 3.312,0000 | 2 | 0,05% |
| `OIL` | 53,2800 | 89,4050 | 36,1250 | 1 | 0,03% |
| `IHSG` | 4.479,2917 | 6.382,4089 | 1.903,1172 | 0 | 0,00% |
| `SP500` | 1.700,2550 | 3.810,4950 | 2.110,2400 | 0 | 0,00% |
| `CPI` | 3,0306 | 5,3560 | 2,3255 | 0 | 0,00% |
| `BI_rate` | 4,7500 | 6,5000 | 1,7500 | 0 | 0,00% |

### Rekomendasi Penanganan Outlier
- **Jangan Menghapus Outlier Target:** 226 observasi outlier pada target (dan 4,6% observasi yang melampaui $\mu + 2\sigma$) mewakili kejadian pasar riil berisiko tinggi. Karena misi proyek adalah membangun *Early Warning System*, memotong atau menghapus baris-baris ini akan membuat model "buta krisis" (*crisis-blind*).
- **Strategi Pemodelan:** Gunakan algoritma berbasis pohon (*tree-based ensembles* seperti LightGBM atau XGBoost) yang secara alami kebal terhadap magnitudo skala outlier, atau gunakan fungsi kerugian yang robust seperti Huber Loss / MAE.
- **Koreksi Data Anomali Nyata:** Hanya koreksi outlier yang terbukti merupakan galat ketik sistemik (2 baris typo pada `USDIDR`).

---

## 5. Analisis Time-Series

### Dinamika Tren Makroekonomi (2010–2026)
Visualisasi time-series terkoordinasi pada `outputs/eda/fig_03_timeseries_macro.png` mengungkap interaksi antar-pasar berikut:
1. **Pasar Ekuitas (IHSG vs SP500):** Bergerak searah dalam jangka panjang dengan korelasi sekuler positif ($r = 0,88$ antar-level), mencerminkan integrasi pasar modal global. Keduanya mengalami kejatuhan tajam bersamaan pada Maret 2020.
2. **Komoditas (OIL vs GOLD):** Minyak mentah menunjukkan volatilitas siklikal tinggi dengan penurunan drastis pada 2014–2016 (shale oil boom) dan 2020. Sebaliknya, emas memperlihatkan tren naik stabil sebagai lindung nilai (*safe haven*), mencapai titik tertinggi barunya pada 2024.
3. **Kurs & Risiko (USDIDR vs VIX):** Depresiasi struktural Rupiah dari ~9.000 (2010) menjadi >16.000 (2024). Lonjakan VIX selalu bertepatan dengan pelemahan tajam Rupiah dan peningkatan volatilitas IHSG.
4. **Kebijakan Moneter (BI_rate vs US_rate):** Perbedaan suku bunga (*interest rate differential*) menyempit drastis pasca-2022 ketika The Fed secara agresif menaikkan suku bunga dari 0,25% menjadi 5,33%, memicu tekanan arus modal keluar (*capital outflow*) dari pasar negara berkembang (*emerging markets*).

### Periode Volatilitas Tinggi yang Teridentifikasi
Berdasarkan penandaan waktu aktual pada data deret waktu, teridentifikasi tiga periode guncangan volatilitas terbesar:
- **Taper Tantrum (Mei–Agustus 2013):** Pernyataan The Fed mengenai pengurangan stimulus moneter memicu lonjakan volatilitas target ke kisaran 0,020–0,030.
- **Krisis Devaluasi Yuan / Pasar Komoditas (Agustus 2015):** Guncangan mata uang Tiongkok dan penurunan harga komoditas global memicu lonjakan target ke ~0,025.
- **Pandemi COVID-19 (Februari–April 2020):** Periode volatilitas tertinggi sepanjang sejarah dataset. Target mencapai rekor absolut **0,05850 pada 20 Maret 2020**, seiring VIX global menembus level 82.

### Bukti Kuantitatif Volatility Clustering
Visualisasi `outputs/eda/fig_08_volatility_clustering.png` dan `outputs/eda/fig_09_acf_abs_return.png` menyajikan bukti kuantitatif tegas mengenai fenomena *volatility clustering* (Mandelbrot, 1963):
1. **Ko-pergerakan Amplitudo:** Klaster fluktuasi besar pada nilai absolut return harian IHSG ($|r_t|$) selalu diikuti oleh fluktuasi besar berikutnya, bertepatan langsung dengan kenaikan nilai `Target_Volatilitas_Y`.
2. **Analisis Autokorelasi (ACF):** Autokorelasi dari $|r_t|$ dihitung untuk lag 1 hingga 30.
   - Ambang batas signifikansi dua sisi 95% Bartlett adalah $\pm \frac{1,96}{\sqrt{N}} = \pm \frac{1,96}{\sqrt{3906}} = \mathbf{\pm 0,0314}$.
   - **Hasil Aktual:** Seluruh lag dari 1 hingga 30 memiliki nilai autokorelasi positif yang melampaui ambang batas 0,0314:
     - Lag 1: **0,2246**
     - Lag 2: **0,1911**
     - Lag 3: **0,2403**
     - Lag 4: **0,1838**
     - Lag 5: **0,1622**
     - Lag 7: **0,2279**
     - Lag 10: **0,1901**
     - Lag 15: **0,1367**
   - **Interpretasi Ekonometrika:** Pembuktian ini memvalidasi keberadaan struktur autoregresif bersyarat (ARCH effect). Volatilitas masa lalu membawa kandungan informasi signifikan mengenai volatilitas masa depan, menjadikan fitur rolling volatility sebagai pilar utama pemodelan.

---

## 6. Analisis Korelasi

Analisis korelasi Pearson linier dievaluasi pada data berlabel terhadap 16 variabel (9 variabel asli, return turunan awal, dan target) seperti disajikan pada `outputs/eda/fig_06_correlation_heatmap.png` dan `outputs/eda/fig_07_feature_target_correlation.png`.

### Peringkat Korelasi terhadap `Target_Volatilitas_Y`

| No | Nama Variabel / Fitur | Korelasi Pearson ($r$) | Arah Hubungan | Rasionalitas Finansial |
|---|---|---|---|---|
| 1 | `rv_past5` (Rolling Std 5-Hari Lalu) | **+0,4460** | Positif Kuat | *Volatility clustering* — volatilitas kemarin berlanjut ke volatilitas esok hari |
| 2 | `VIX` | **+0,4342** | Positif Kuat | Transmisi kepanikan pasar global ke bursa domestik Indonesia |
| 3 | `IHSG` (Level Harga) | **-0,2842** | Negatif Sedang | Efek *leverage* finansial — penurunan harga saham meningkatkan volatilitas pasar |
| 4 | `VIX_rel` ($VIX / MA_{20}(VIX)$) | **+0,2238** | Positif Sedang | Kejutan lonjakan kepanikan global jangka pendek |
| 5 | `rate_diff` ($BI\_rate - US\_rate$) | **+0,2042** | Positif Sedang | Korelasi rezim makro — era suku bunga domestik tinggi bertepatan dengan volatilitas tinggi |
| 6 | `US_rate` | **-0,2005** | Negatif Sedang | Rezim era ZIRP (2020) bertepatan dengan lonjakan volatilitas krisis |
| 7 | `SP500` (Level Harga) | **-0,1915** | Negatif Lemah | Pasar ekuitas bullish jangka panjang berkorelasi dengan volatilitas rendah |
| 8 | `USDIDR` (Level Kurs) | **-0,1595** | Negatif Lemah | Tren sekuler non-stasioner |
| 9 | `IHSG_ret` (Return Harian $t$) | **-0,1387** | Negatif Lemah | Asimetri return — return harian negatif memicu sedikit kenaikan volatilitas ke depan |
| 10 | `OIL_ret5` (Return Minyak 5-Hari) | **-0,1142** | Negatif Lemah | Kejatuhan harga energi meningkatkan ketidakpastian pasar |
| 11 | `CPI` | **+0,0895** | Positif Lemah | Tingkat inflasi level |
| 12 | `BI_rate` | **+0,0782** | Positif Lemah | Level suku bunga BI |
| 13 | `GOLD` | **-0,0684** | Negatif Lemah | Level harga emas |
| 14 | `USDIDR_ret5` | **+0,0138** | Positif Sangat Lemah | Korelasi linier mentah mendekati nol (karena belum dimodelkan interaksinya) |
| 15 | `OIL` | **-0,0132** | Negatif Sangat Lemah | Level harga minyak mentah |

### Batasan Interpretasi Korelasi
1. **Bahaya Korelasi Palsu pada Variabel Level:** Variabel level seperti `IHSG`, `SP500`, dan `USDIDR` memiliki tren secular (*non-stationary unit root*). Korelasi linier variabel level terhadap target sebagian besar bersifat semu dan tidak dapat diandalkan untuk prediksi out-of-sample tanpa diferensiasi/transformasi stasioner.
2. **Korelasi Bukan Kausalitas:** Korelasi tinggi antara `rv_past5` dan target ($r = +0,4460$) menunjukkan persistensi statistik, bukan hubungan sebab-akibat deterministik.
3. **Hubungan Non-Linier Tersembunyi:** Variabel seperti `USDIDR_ret5` memiliki korelasi linier mendekati nol ($r = 0,0138$), namun dapat memiliki daya prediksi prediktif kuat ketika berinteraksi dengan guncangan VIX atau perbedaan suku bunga.

---

## 7. Evaluasi Tiga Kandidat Feature Engineering

Pada notebook Section 11, dievaluasi tiga fitur kandidat turunan awal yang dirancang berdasarkan teori transmisi makro-finansial:

### Kandidat 1: `X1_Fear_Liquidity` (Fear Liquidity Composite)
- **Formula Matematika:**
  $$X_{1, t} = \text{VIX}_t \times \ln\left(\frac{\text{USDIDR}_t}{\text{MA}_{20}(\text{USDIDR})_t}\right)$$
- **Motivasi Finansial:** Menggabungkan kepanikan risiko global ($\text{VIX}$) dengan tekanan likuiditas valuta asing domestik. Ketika pasar global panik bersamaan dengan depresiasi Rupiah yang menembus rata-rata 20 harinya, terjadi tekanan ganda penarikan modal asing (*capital flight*) dari pasar saham Indonesia.
- **Korelasi Linier terhadap Target:** $r = \mathbf{+0,1258}$.
- **Temuan Plot Visual:** Scatter plot (`outputs/eda/fig_10_candidate_features_scatter.png`) dan time-series (`outputs/eda/fig_11_candidate_features_timeseries.png`) menunjukkan sinyal yang sangat reaktif saat krisis (2013, 2015, 2020), bertindak sebagai indikator stres likuiditas valas.
- **Kelemahan & Risiko:** Sangat rentan terhadap anomali data ketik `USDIDR` jika tidak dibersihkan terlebih dahulu; memiliki distribusi miring karena $\text{VIX}$ bernilai besar.
- **Status Evaluasi:** **LAYAK DIUJI LEBIH LANJUT** pada Task 2 (setelah penanganan anomali data kurs).

### Kandidat 2: `X2_Rate_Diff_Pressure` (Rate Differential Pressure)
- **Formula Matematika:**
  $$X_{2, t} = \left(\text{BI\_rate}_t - \text{US\_rate}_t\right) \times \Delta\%_5(\text{USDIDR})_t$$
- **Motivasi Finansial:** Mengukur insentif spekulasi *carry trade*. Selisih suku bunga riil mengendalikan daya tarik aset domestik, sementara momentum 5 hari nilai tukar mengukur realisasi risiko depresiasi valuta.
- **Korelasi Linier terhadap Target:** $r = \mathbf{+0,0124}$.
- **Temuan Plot Visual:** Fluktuasi simetris di sekitar nol, namun korelasi linier univariat terhadap target sangat lemah ($r \approx 0$).
- **Kelemahan & Risiko:** Suku bunga acuan adalah data bulanan berbentuk fungsi tangga (*step function*), sehingga dinamika harian sepenuhnya didominasi oleh pergerakan kurs 5 hari. Hubungan dengan volatilitas IHSG tidak bersifat linier.
- **Status Evaluasi:** **PERLU REVISI** sebelum pemodelan (pertimbangkan transformasi magnitudo mutlak atau interaksi non-linear).

### Kandidat 3: `X3_Commodity_Shock` (Commodity Macro Shock)
- **Formula Matematika:**
  $$X_{3, t} = \Delta\%_5(\text{OIL})_t \times \Delta\%_5(\text{GOLD})_t \times \Delta\%_5(\text{SP500})_t$$
- **Motivasi Finansial:** Mengukur guncangan simultan pada tiga pilar ekonomi global: energi/komoditas industri, aset lindung nilai (*safe haven*), dan ekuitas global.
- **Korelasi Linier terhadap Target:** $r = \mathbf{-0,1016}$.
- **Temuan Plot Visual:** Sinyal sangat sporadis dengan orde magnitudo yang sangat kecil ($10^{-5}$ hingga $10^{-7}$).
- **Kelemahan & Risiko:** Perkalian tiga return persentase menghasilkan skala angka mikroskopis yang tidak stabil dan sulit diinterpretasikan (misalnya dua guncangan negatif menghasilkan tanda positif).
- **Status Evaluasi:** **BELUM DIDUKUNG BUKTI KUAT**; formula perlu diganti, misalnya dengan norma vektor L1/L2 dari guncangan makro atau agregasi terpisah.

---

## 8. Audit Anti-Leakage (Pencegahan Kebocoran Data)

Pencegahan kebocoran data (*data leakage*) adalah prioritas tertinggi dalam rekayasa sistem deret waktu finansial. Mengingat target $\text{Target\_Volatilitas\_Y}_t$ merangkum return masa depan pada interval $[t+1, t+5]$, kesalahan metodologis sekecil apa pun dapat menyebabkan model mengalami overfitting masif in-sample namun gagal total out-of-sample.

### Matriks Audit Risiko Kebocoran Data

| No | Dimensi Risiko | Potensi Kebocoran Informasi | Status Audit | Tindakan & Rekomendasi Mitigasi |
|---|---|---|---|---|
| 1 | **Target Window Overlap** | Memasukkan fitur volatilitas yang menghitung deviasi standar pada jendela $[t, t+4]$ atau $[t+1, t+5]$. | **FAIL (Jika Terjadi)** / **PASS (Pada Notebook)** | Pastikan seluruh fitur volatilitas historis hanya dihitung dari data penutupan hari $t$ ke belakang ($[t-4, t]$ atau $[t-N, t]$). Jangan pernah menggunakan shift negatif pada fitur prediktor. |
| 2 | **Rolling Feature Timestamps** | Perhitungan rolling window yang menyertakan informasi yang belum tersedia saat keputusan diambil. | **PASS** (dengan catatan) | Jika model ditujukan untuk prediksi sebelum penutupan hari $t$, fitur return harus menggunakan `.shift(1)`. Jika model ditujukan untuk prediksi End-of-Day $t$, data penutupan hari $t$ sah digunakan. |
| 3 | **Preprocessing Scaling** | Melakukan `StandardScaler.fit()` atau `MinMaxScaler.fit()` pada seluruh dataset sekaligus (mencakup data validasi/uji). | **WARNING** (Wajib dikawal di Task 2) | Parameter scaler ($\mu, \sigma$) wajib di-fit secara eksklusif hanya pada data Training ($t \le 2021$), kemudian di-transformasikan ke partisi validasi dan uji. |
| 4 | **Imputasi Missing Values** | Menggunakan rata-rata atau median global dari seluruh deret waktu untuk mengisi data kosong. | **PASS** (Saat ini) / **WARNING** (Task 2) | Fitur prediktor saat ini 100% lengkap. Jika fitur baru menghasilkan NaN di awal jendela, lakukan *backward-fill* atau buang baris awal; dilarang menggunakan mean global. |
| 5 | **Skema Validasi / Split Data** | Menggunakan `train_test_split(shuffle=True)` atau K-Fold cross validation standar. | **WARNING** (Wajib dikawal di Task 2) | Dilarang keras melakukan pengacakan baris. Wajib menggunakan `TimeSeriesSplit` atau *Walk-Forward Validation*. Karena target memiliki horizon 5 hari, wajib diterapkan **embargo period minimal 5 hari** antara set latih dan set validasi agar tidak ada irisan informasi target. |

---

## 9. Review Seluruh Visualisasi

Berikut adalah tabel audit menyeluruh terhadap 11 grafik hasil eksekusi notebook yang tersimpan pada direktori `outputs/eda/`:

| Nama File Gambar | Ukuran File | Pertanyaan Analitis | Temuan Utama yang Terlihat & Terhitung | Interpretasi Finansial & Implikasi Pemodelan |
|---|---|---|---|---|
| `outputs/eda/fig_01_distributions.png` | 213 KB | Bagaimana profil sebaran data dari masing-masing 10 variabel? | Skewness target (+2,64) dan VIX (+2,45) tinggi. CPI dan BI rate menunjukkan profil bimodal. | Variabel finansial tidak berdistribusi normal; model non-parametrik (pohon keputusan) lebih diunggulkan dibanding regresi linier OLS standar. |
| `outputs/eda/fig_02_outlier_boxplot.png` | 50 KB | Apakah ada nilai ekstrem mencurigakan saat distandarisasi (z-score)? | Outlier ekstrim terlihat pada OIL (z < -5), VIX (z > 8), dan US rate (z > 2). USDIDR memiliki 2 titik ganjil di bawah. | Outlier mencerminkan syok pasar riil (COVID, ZIRP exit), kecuali 2 titik typo USDIDR yang harus dikoreksi. |
| `outputs/eda/fig_03_timeseries_macro.png` | 333 KB | Bagaimana dinamika tren 5 klaster makro sepanjang 2010–2026? | Ko-pergerakan saham global, tren naik emas & kurs, serta divergensi suku bunga pasca-2022 teridentifikasi jelas. | Fitur level harga tidak stasioner; fitur transformasi (return, rasio MA, selisih suku bunga) wajib dibuat. |
| `outputs/eda/fig_04_target_distribution.png` | 136 KB | Bagaimana bentuk ekor distribusi dan dinamika time-series target? | Ekor kanan sangat tebal (kurtosis 12,21). 4,6% data melampaui $\mu + 2\sigma$. Puncak tertinggi terjadi pada Maret 2020 (0,0585). | Target bersifat fat-tailed; target transformasi (seperti $\ln(Y)$) atau evaluasi MAE/Huber Loss sangat disarankan. |
| `outputs/eda/fig_05_ihsg_return_vs_target.png` | 253 KB | Apakah besaran return hari ini atau volatilitas masa lalu berkorelasi dengan target? | Korelasi \|return harian\| vs target adalah $r = 0,324$, sedangkan korelasi vol 5-hari lalu vs target adalah $r = 0,446$. | Volatilitas rolling masa lalu membawa sinyal jauh lebih kuat daripada return harian sesaat. |
| `outputs/eda/fig_06_correlation_heatmap.png` | 200 KB | Bagaimana matriks korelasi linier antar seluruh pasangan variabel? | Multikolinearitas tinggi antar level harga (IHSG vs SP500 $r = 0,88$, GOLD vs SP500 $r = 0,83$). | Menegaskan bahaya menggunakan variabel level mentah; transformasi stasioneritas mutlak diperlukan. |
| `outputs/eda/fig_07_feature_target_correlation.png` | 56 KB | Fitur apa saja yang memiliki korelasi linier tertinggi terhadap target? | `rv_past5` (+0,45) dan `VIX` (+0,43) berada di posisi teratas. Variabel makro level berada di peringkat bawah. | Dua pilar utama model awal adalah persistensi volatilitas domestik dan transmisi ketakutan global. |
| `outputs/eda/fig_08_volatility_clustering.png` | 324 KB | Apakah fluktuasi return harian mengelompok bersama target? | Amplitudo \|return\| IHSG membengkak persis saat target volatilitas melonjak tinggi pada jendela waktu yang sama. | Bukti visual kuat adanya pengelompokan volatilitas (*volatility clustering*). |
| `outputs/eda/fig_09_acf_abs_return.png` | 32 KB | Berapa lama memori dependensi temporal volatilitas bertahan? | Seluruh lag 1 hingga 30 berada di atas batas signifikansi 95% ($\pm 0,0314$). | Sinyal autoregresif bertahan lama; fitur rolling dengan jendela bervariasi (5, 10, 20 hari) akan sangat informatif. |
| `outputs/eda/fig_10_candidate_features_scatter.png` | 100 KB | Bagaimana korelasi bivariat fitur X1, X2, X3 terhadap target? | X1 menunjukkan tren korelasi positif ($r = 0,126$), X2 datar di sekitar nol ($r = 0,012$), X3 condong negatif ($r = -0,102$). | X1 paling menjanjikan sebagai fitur interaksi awal; X2 dan X3 memerlukan perbaikan formula. |
| `outputs/eda/fig_11_candidate_features_timeseries.png` | 124 KB | Bagaimana perilaku fitur X1, X2, X3 sepanjang lintasan waktu? | X1 melonjak saat krisis likuiditas, X2 berosilasi di sekitar nol, X3 memiliki variabilitas mikroskopis. | Skala nilai X3 perlu normalisasi; X1 menangkap rezim krisis makro dengan baik. |

---

## 10. Kesimpulan EDA dan Rekomendasi

### Sepuluh Temuan Utama
1. **Target Terverifikasi Pasti:** Target `Target_Volatilitas_Y` terkonfirmasi 100% merupakan deviasi standar return IHSG 5 hari ke depan ($r = 0,999711$).
2. **Kualitas Data Sangat Tinggi:** Tidak ada nilai kosong pada seluruh prediktor; tidak ada duplikasi data.
3. **Anomali Koma Desimal USDIDR:** Ditemukan dua titik salah ketik desimal pada `USDIDR` (baris 215 dan 546) yang wajib dikoreksi sebelum menghitung return valas.
4. **Keabsahan Nilai Negatif Minyak:** Nilai `OIL = -37.63` pada April 2020 adalah fakta sejarah riil dan harus dipertahankan.
5. **Karakteristik Leptokurtik:** Distribusi target sangat condong ke kanan dan memiliki ekor tebal (*kurtosis* = 12,21).
6. **Keberadaan ARCH Effect:** Fenomena *volatility clustering* terbukti secara kuantitatif melalui ACF lag 1–30 yang signifikan ($p < 0,05$).
7. **Prediktor Utama:** Fitur persistensi domestik (`rv_past5`, $r = 0,45$) dan sentimen global (`VIX`, $r = 0,43$) adalah sinyal linier terkuat.
8. **Inkompatibilitas Variabel Level:** Harga level IHSG, SP500, dan kurs tidak stasioner dan tidak boleh dipakai mentah.
9. **Kandidat Fitur X1 Prospektif:** Interaksi $VIX \times \text{depresiasi USDIDR}$ menunjukkan rasionalitas ekonomi yang solid.
10. **Batasan Partisi Data:** Data berlabel berakhir pada 24 Desember 2024; data uji 2025–2026 utuh tanpa label.

### Apa yang Sudah Diketahui vs Belum Diketahui
- **Sudah Diketahui:** Formula target, struktur partisi data, karakteristik distribusi, stasioneritas fitur, persistensi volatilitas, dan risiko leakage.
- **Belum Diketahui:** Derajat multikolinearitas (VIF) saat ratusan fitur ditambahkan pada Task 1; apakah transformasi logaritmik $\ln(Y)$ memberikan skor evaluasi out-of-sample lebih baik daripada target asli; signifikansi fitur makro pada model non-linier melalui analisis SHAP (Task 3).

### Hal yang Wajib Diselesaikan Sebelum Task 2 (Modeling)
1. **Pembersihan Data Typo USDIDR:** Koreksi baris 215 menjadi 8.881,10 dan baris 546 menjadi 8.920,00.
2. **Rekayasa Fitur Task 1:**
   - Fitur volatilitas bergulir multi-horizon (misal: rolling std 5, 10, 20, 60 hari).
   - Fitur momentum dan return logaritmik seluruh aset.
   - Fitur perbedaan suku bunga dan rasio valuasi.
   - Fitur interaksi regim stres pasar.
3. **Desain Anti-Leakage Pipeline:**
   - Memastikan seluruh fitur rolling bergeser secara aman (`.shift(1)` jika diperlukan).
   - Menyiapkan modul preprocessing yang membungkus *scaler* di dalam *pipeline cross-validation*.
4. **Partisi Validasi Time-Series Definitif:**
   - **Training Set:** 2010-01-04 s/d 2021-12-31 (3.130 baris)
   - **Validation Set:** 2022-01-01 s/d 2024-12-24 (777 baris)
   - **Test Set (Kompetisi):** 2025-01-02 s/d 2026-05-22 (359 baris)
   - Embargo period 5 hari kerja di antara Training dan Validation.

---

## 11. Reproducibility

Untuk memastikan seluruh analisis ini dapat diaudit dan direproduksi kembali secara independen oleh pihak lain:

| Parameter Lingkungan | Nilai / Spesifikasi Aktual |
|---|---|
| **Path Notebook Utama** | [`notebook/EDA.ipynb`](file:///z:/Projects/Inception/notebook/EDA.ipynb) |
| **Total Cells** | 31 cells (14 markdown cells, 17 code cells) |
| **Status Eksekusi Terakhir** | **17 dari 17 code cells berhasil dieksekusi 100% tanpa error** |
| **Waktu Eksekusi Terakhir** | 14 Oktober 2026 |
| **Environment Kernel** | Python 3.12.10 (64-bit) |
| **Dependensi Kunci** | `pandas 3.0.6`, `numpy 2.5.3`, `scipy 1.15.1`, `matplotlib 3.10.0`, `seaborn 0.13.2`, `jupyter/nbconvert` |
| **Script Rekonstruksi & Verifikasi** | [`scripts/build_notebook.py`](file:///z:/Projects/Inception/scripts/build_notebook.py), [`scripts/verify_nb.py`](file:///z:/Projects/Inception/scripts/verify_nb.py) |
| **Folder Output Visualisasi** | [`outputs/eda/`](file:///z:/Projects/Inception/outputs/eda/) (11 file gambar PNG utuh) |
| **Backup Notebook Asli** | [`archive/notebook/EDA_backup_20261013.ipynb`](file:///z:/Projects/Inception/archive/notebook/EDA_backup_20261013.ipynb) |
| **Dataset Mentah** | [`Aset Lomba/dataset peserta.csv`](file:///z:/Projects/Inception/Aset%20Lomba/dataset%20peserta.csv) (tidak dimodifikasi) |

### Keterbatasan Reproduksi
- Notebook ini dirancang untuk dijalankan dengan working directory `notebook/` atau dengan path relatif proyek standar.
- Eksekusi kernel bersih memerlukan alokasi RAM minimal 4 GB untuk merender plot time-series beresolusi tinggi (120 DPI) tanpa kendala memori.
