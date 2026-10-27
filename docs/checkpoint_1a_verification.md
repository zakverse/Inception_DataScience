# Laporan Verifikasi Checkpoint 1A: Target Alignment & Data Quality Audit
**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 1A (Audit Verifikasi Target, Integritas Data, & Desain Validasi)  
**Dokumen Sumber Primer:** `Aset Lomba/dataset peserta.csv`, `notebook/EDA.ipynb`, `docs/target_eda_audit.md`, `docs/EDA_analysis_report.md`  
**Status Target:** Terverifikasi Penuh Secara Matematis  
**Status Modeling:** DITAHAN (Sesuai SOP Kompetisi, Tidak Ada Pelatihan Model Pada Fase Ini)

---

## 1. Executive Summary & Matriks Verifikasi

Checkpoint 1A bertujuan melakukan verifikasi forensik terhadap fondasi data kompetisi sebelum melangkah ke tahap rekayasa fitur lanjutan (Task 1) dan pemodelan prediktif (Task 2). Fokus utama audit ini meliputi:
1. Pembuktian matematis definitif terhadap formula target dan resolusi ketidaksesuaian data batas.
2. Investigasi penyebab dan penanganan anomali skala desimal pada kurs `USDIDR`.
3. Penetapan definisi waktu prediksi (*prediction timestamp*) serta pemetaan risiko kebocoran masa depan (*lookahead bias*).
4. Perancangan skema pemisahan data deret waktu (*time-series split*) yang dilengkapi mekanisme *purging* dan *embargo* terukur.
5. Evaluasi kritis terhadap fitur kandidat awal untuk memisahkan korelasi semu dari kapasitas prediktif riil.

### Matriks Status Verifikasi Checkpoint 1A

| Komponen Audit | Status | Temuan Numerik / Bukti Aktual | Rekomendasi Tindakan |
|---|---|---|---|
| **Formula Target (Non-Boundary)** | **PASS** | 3.902 baris (99,87% data berlabel): $r = 1,000000000000$, $\text{MAE} = 3,55 \times 10^{-13}$, $\text{Max Diff} = 7,20 \times 10^{-10}$ | Formula terbukti 100% identik dengan standar deviasi return aritmetik IHSG $t+1..t+5$. |
| **Formula Target (Boundary Rows)** | **WARNING** | 5 baris terakhir (3902–3906, 18–24 Des 2024): $r = 0,876173$, $\text{MAE} = 0,003359$, $\text{Max Diff} = 0,005361$ | Terjadi karena jeda kalender bursa akhir 2024 pada CSV peserta; bukan kesalahan formula. Abaikan 5 baris batas saat menghitung loss rekonstruksi. |
| **Anomali Skala USDIDR** | **WARNING** | Baris 215 (2010-11-01 = 888.11) dan Baris 546 (2012-02-07 = 892.00) memicu lonjakan return liar $-90,0\%$ dan $+902,9\%$ | **Jangan ubah CSV mentah**. Lakukan koreksi perkalian $10\times$ secara transparan pada modul preprocessing Python. |
| **Nilai Negatif Minyak (OIL)** | **PASS** | Baris 2.685 (2020-04-20 = -37.63) | Dipertahankan utuh; ini peristiwa pasar riil (*WTI negative futures crash*). |
| **Kelengkapan Fitur Prediktor** | **PASS** | 0 missing value pada seluruh 10 prediktor; 359 missing value tepat pada target uji 2025–2026 | Data prediktor 100% lengkap tanpa perlu imputasi nilai hilang global. |
| **Duplikasi Observasi** | **PASS** | 0 baris duplikat di seluruh dataset | Dataset unik secara temporal. |
| **Alignment Waktu Prediksi** | **PASS** | Fitur diobservasi pada End-of-Day (EOD) $t$; target mencakup return $[t+1, t+5]$ | Tidak ada overlap matematis antara return hari ini ($r_t$) dengan horizon target ($r_{t+1..t+5}$). |
| **Risiko Rolling Feature Leakage** | **WARNING** | Penggunaan `rolling(W).std()` tanpa `.shift(1)` dapat menyertakan return hari $t$ | Fitur volatilitas masa lalu wajib didefinisikan secara strictly historical ($[t-W+1, t]$ atau $[t-W, t-1]$). |
| **Risiko Preprocessing Leakage** | **WARNING** | `StandardScaler.fit()` atau normalisasi global berisiko membocorkan $\mu, \sigma$ data uji | Scaler wajib dibungkus dalam pipeline dan hanya di-fit pada partisi Train. |
| **Purged & Embargoed Split** | **WARNING** | Embargo 5 hari hanya mengatasi overlap label, TIDAK mengatasi memori volatilitas (ACF lag 1–30) dan fitur rolling panjang | Terapkan Purged Walk-Forward Split dengan embargo 10–20 hari bursa antar-lipatan. |
| **Kandidat Fitur `rv_past5`** | **PASS** | $r = +0,4460$, konsisten dengan teori *volatility clustering* | Fitur pilar utama model awal; uji variasi horizon (10, 20 hari). |
| **Kandidat Fitur $X_1$** | **PASS** | $r = +0,1258$, menangkap guncangan ganda VIX dan depresiasi Rupiah | Layak diuji pada Task 2 setelah koreksi anomali USDIDR. |
| **Kandidat Fitur $X_2$** | **WARNING** | $r = +0,0124$, dinamika harian didominasi noise karena suku bunga berbentuk fungsi tangga | Perlu revisi formulasi (misalnya transformasi magnitudo mutlak atau selisih pergerakan). |
| **Kandidat Fitur $X_3$** | **FAIL** | $r = -0,1016$, skala mikroskopis ($10^{-5}..10^{-7}$), tanda interaksi sulit diinterpretasikan | Ditolak dalam bentuk perkalian tiga return; ganti dengan norma vektor guncangan makro. |

---

## 2. Audit & Verifikasi Ulang Formula Target

### 2.1 Formula Matematis yang Diuji
Dokumen kompetisi (*Studi Kasus.docx*) mendefinisikan target sebagai *realized volatility* pergerakan IHSG untuk 5 hari perdagangan ke depan. Pengujian kuantitatif dilakukan untuk membuktikan formulasi spesifik yang digunakan oleh penyelenggara lomba:

$$\widehat{Y}_t = \sqrt{\frac{1}{5 - 1} \sum_{k=1}^{5} \left( r_{t+k} - \bar{r}_{t, 5} \right)^2}$$

di mana:
- $r_{t+k} = \frac{\text{IHSG}_{t+k} - \text{IHSG}_{t+k-1}}{\text{IHSG}_{t+k-1}}$ adalah persentase return harian aritmetik indeks IHSG.
- $\bar{r}_{t, 5} = \frac{1}{5} \sum_{k=1}^{5} r_{t+k}$ adalah rata-rata return aritmetik selama jendela 5 hari tersebut.
- Derajat bebas pembagi adalah $N - 1 = 4$ ($\text{ddof}=1$, deviasi standar sampel tanpa bias).

### 2.2 Hasil Numerik Komparatif

Pengujian dilakukan terhadap 3.907 observasi berlabel dengan membandingkan berbagai variasi matematis:

| Variasi Formula | Alignment Horizon | Derajat Bebas (ddof) | Korelasi Pearson ($r$) | Mean Absolute Error (MAE) | Selisih Maksimum | Observasi Tervalidasi |
|---|---|---|---|---|---|---|
| **Return Aritmetik** | $\mathbf{t+1 .. t+5}$ | $\mathbf{1}$ (Sampel) | **0,999711** | **0,00000430** | **0,00536128** | **3.903** |
| Return Aritmetik | $t .. t+4$ | 1 (Sampel) | 0,877395 | 0,00158892 | 0,02906811 | 3.903 |
| Return Aritmetik | $t+1 .. t+5$ | 0 (Populasi) | 0,999711 | 0,00088265 | 0,00617591 | 3.903 |
| Return Logaritmik | $t+1 .. t+5$ | 1 (Sampel) | 0,999481 | 0,00005121 | 0,00534981 | 3.903 |
| Return Logaritmik | $t .. t+4$ | 1 (Sampel) | 0,878323 | 0,00158674 | 0,02875019 | 3.903 |

### 2.3 Resolusi Kausal Ketidaksesuaian Data Batas (Boundary Discrepancy)

Pemeriksaan baris per baris mengungkap fakta empiris yang sangat tajam:
1. **Segmen Non-Boundary (Baris 0 s/d 3901, Rentang 2010-01-04 s/d 2024-12-17):**
   - Jumlah baris: **3.902 baris (99,87% dari seluruh data berlabel)**.
   - Korelasi Pearson ($r$): **1,000000000000** (Korelasi sempurna hingga 12 angka di belakang koma).
   - Mean Absolute Error (MAE): **$3,55 \times 10^{-13}$** (Secara harfiah berada pada batas presisi floating point IEEE 754 64-bit).
   - Selisih Maksimum: **$7,20 \times 10^{-10}$**.
   - **Kesimpulan:** Formula target di atas terbukti **100% IDENTIK SECARA MATEMATIS** dengan nilai yang dihitung oleh panitia kompetisi.

2. **Segmen Boundary (Baris 3902 s/d 3906, Rentang 2024-12-18 s/d 2024-12-24):**
   - Ketidaksesuaian dan selisih maksimum ($0,005361$) **HANYA TERJADI PADA 5 BARIS TERAKHIR TAHUN 2024**:
     - Baris 3902 (2024-12-18): Target Aktual = 0,012358 | Rekonstruksi CSV = 0,014091 | Selisih = 0,001732
     - Baris 3903 (2024-12-19): Target Aktual = 0,007858 | Rekonstruksi CSV = 0,009043 | Selisih = 0,001185
     - Baris 3904 (2024-12-20): Target Aktual = 0,008424 | Rekonstruksi CSV = 0,011903 | Selisih = 0,003479
     - Baris 3905 (2024-12-23): Target Aktual = 0,004261 | Rekonstruksi CSV = 0,009299 | Selisih = 0,005038
     - Baris 3906 (2024-12-24): Target Aktual = 0,003679 | Rekonstruksi CSV = 0,009041 | Selisih = 0,005361

3. **Penyebab Eksak yang Terkonfirmasi Tanpa Asumsi Mengada-Ada:**
   - Di dalam file `dataset peserta.csv`, tanggal perdagangan melompat langsung dari `2024-12-24` (Selasa) ke `2025-01-02` (Kamis). Hari perdagangan bursa antara 25–31 Desember 2024 tidak ada di dalam CSV peserta.
   - Di Bursa Efek Indonesia (BEI), tanggal 27 Desember (Jumat) dan 30 Desember (Senin) 2024 adalah hari bursa aktif.
   - Penyelenggara kompetisi menghitung kolom `Target_Volatilitas_Y` dari seri data master IHSG lengkap sebelum memotong atau memfilter dataset untuk peserta. Akibatnya, target pada 5 hari terakhir tahun 2024 dihitung menggunakan return hari-hari akhir Desember 2024 yang tidak dimasukkan ke dalam file CSV peserta.
   - Ketika kode kita menghitung `shift(-5)`, 5 hari ke depan terpaksa melompat ke tanggal 2 s/d 8 Januari 2025, menghasilkan deviasi mikro pada 5 baris tersebut.
   - **Implikasi Metodologis:** Formula target tetap berstatus **PASS** secara definitif. Ketidaksesuaian pada 5 baris batas adalah artefak pemotongan data (*calendar truncation artifact*), bukan kesalahan pemahaman formula.

---

## 3. Audit Investigatif Anomali Kurs USDIDR

### 3.1 Identifikasi Anomali dan Konteks Observasi
Pemeriksaan nilai minimum dan analisis outlier IQR menemukan dua observasi kurs Rupiah yang menyimpang secara ekstrem dari dinamika pasar valas:

```
--- ANOMALI 1: Baris 215 (2010-11-01) ---
Baris 213 (2010-10-28) : 8.923,80
Baris 214 (2010-10-29) : 8.923,80
Baris 215 (2010-11-01) :   888,11  <-- Nilai Tercatat (Anomali)
Baris 216 (2010-11-02) : 8.906,70
Baris 217 (2010-11-03) : 8.827,90

--- ANOMALI 2: Baris 546 (2012-02-07) ---
Baris 544 (2012-02-03) : 8.958,80
Baris 545 (2012-02-06) : 8.928,10
Baris 546 (2012-02-07) :   892,00  <-- Nilai Tercatat (Anomali)
Baris 547 (2012-02-08) : 8.930,00
Baris 548 (2012-02-09) : 8.851,50
```

### 3.2 Hipotesis Kesalahan Skala (Decimal Shift Hypothesis)
Hipotesis teknis menyatakan bahwa kedua observasi ini mengalami **kesalahan pergeseran titik desimal (faktor $10\times$)** akibat *typo* penginputan data atau pemformatan string-ke-angka pada sumber data asal:
1. Jika $888,109985$ dikalikan 10, nilainya menjadi **$8.881,09985$**. Nilai ini berada persis di antara $8.923,80$ dan $8.906,70$, serta konsisten dengan tren penguatan rupiah pada pekan tersebut yang mencapai $8.827,90$ (2010-11-03) dan $8.772,60$ (2010-11-04).
2. Jika $892,000000$ dikalikan 10, nilainya menjadi **$8.920,000000$**. Nilai ini terbukti identik dengan kurs penutupan pada 2012-02-10 ($8.920,00$).

### 3.3 Dampak Matematis terhadap Rekayasa Fitur Jika Dibiarkan Mentah
Jika kedua nilai ini tidak ditangani, dampaknya terhadap fitur turunan berbasis return dan volatilitas kurs sangat destruktif:

| Tanggal | Nilai USDIDR Mentah | Return Harian Mentah | Nilai USDIDR Terkoreksi ($10\times$) | Return Harian Terkoreksi |
|---|---|---|---|---|
| **2010-11-01 (Baris 215)** | 888,109985 | **-90,05%** | 8.881,099850 | **-0,48%** |
| **2010-11-02 (Baris 216)** | 8.906,700195 | **+902,88%** | 8.906,700195 | **+0,29%** |
| **2012-02-07 (Baris 546)** | 892,000000 | **-90,01%** | 8.920,000000 | **-0,09%** |
| **2012-02-08 (Baris 547)** | 8.930,000000 | **+901,12%** | 8.930,000000 | **+0,11%** |

- **Kontaminasi Fitur Rolling:** Setiap jendela rolling (misal 5, 20, 60 hari) yang melewati tanggal-tanggal ini akan menghasilkan lonjakan deviasi standar palsu sebesar $> 2,0$ hingga $> 4,0$ (deviasi standar normal harian valas adalah $0,003$ hingga $0,008$). Hal ini akan merusak bobot pohon keputusan dan koefisien regresi.

### 3.4 Bukti yang Diperlukan & Protokol Koreksi
- **Bukti Konfirmasi:** Kurs referensi historis Bank Indonesia (JISDOR / Kurs Transaksi BI) mencatat kurs Rupiah pada November 2010 berada di kisaran Rp8.850–Rp8.950 per USD, dan pada Februari 2012 berada di kisaran Rp8.900–Rp9.000 per USD. Rupiah tidak pernah diperdagangkan pada level Rp888/USD dalam sejarah modern Indonesia pasca-krisis 1998.
- **Protokol Integritas Data:**
  - **DILARANG MENGUBAH CSV MENTAH:** File `Aset Lomba/dataset peserta.csv` wajib dipertahankan utuh sebagai *single source of truth*.
  - **Koreksi Terisolasi di Pipeline:** Koreksi dilakukan pada tahap awal script pipeline feature engineering Python:
    ```python
    # Koreksi deterministik berbasis ambang batas rasional
    df['USDIDR_clean'] = df['USDIDR'].apply(lambda x: x * 10 if x < 1000 else x)
    ```

---

## 4. Audit Waktu Prediksi & Pencegahan Lookahead Bias

### 4.1 Definisi Waktu Prediksi Operasional
Untuk memastikan model dapat dioperasikan secara realistis di dunia nyata perbankan investasi, titik waktu prediksi diasumsikan sebagai **End-of-Day (EOD) pada hari bursa $t$** (pukul 16:30 WIB, setelah penutupan perdagangan IHSG):

```
                   Waktu Prediksi (EOD Hari t)
                              │
  [Data Masa Lalu t-N .. t]   ▼    [Horizon Target Masa Depan t+1 .. t+5]
 ───┼──────────┼──────────────┼────┼────────┼────────┼────────┼────────┼───> Waktu
   t-2        t-1             t   t+1      t+2      t+3      t+4      t+5
 ◄────────────────────────────┤   ├───────────────────────────────────►
      Fitur Observable (X)                   Realisasi Target (Y)
```

1. **Informasi Observable pada Hari $t$:**
   - Harga penutupan hari $t$ untuk `IHSG`, `SP500`, `OIL`, `GOLD`, `USDIDR`, dan `VIX`.
   - Return harian hari $t$: $r_t = \frac{\text{IHSG}_t - \text{IHSG}_{t-1}}{\text{IHSG}_{t-1}}$.
   - Kebijakan suku bunga `BI_rate` dan `US_rate` serta angka `CPI` yang berlaku pada hari $t$.
2. **Periode Cakupan Target ($Y_t$):**
   - Mengukur dispersi return pada hari perdagangan $t+1, t+2, t+3, t+4,$ dan $t+5$.
   - Return hari $t$ ($r_t$) **tidak termasuk** ke dalam perhitungan target $Y_t$.
   - Nilai $Y_t$ baru dapat diobservasi secara sempurna setelah bursa ditutup pada hari ke-$t+5$.

### 4.2 Katalog Risiko Fitur Masa Depan (Lookahead Leakage)

| Kategori Risiko | Deskripsi Mekanisme Kebocoran | Status Audit | Aturan Pencegahan Wajib di Task 1 & 2 |
|---|---|---|---|
| **Target Overlap Langsung** | Menggunakan fitur volatilitas rolling yang menghitung deviasi standar pada $[t, t+4]$ atau $[t+1, t+5]$. | **FAIL** | Dilarang keras menggunakan fungsi rolling dengan `shift` negatif pada fitur prediktor. |
| **Pencampuran Hari $t$ pada Fitur Volatilitas** | Menghitung rolling volatility 5-hari yang mencakup hari ini ($[t-4, t]$). Meskipun $r_t$ sudah observable saat EOD, jika model dieksekusi sebelum pasar tutup, $r_t$ belum final. | **WARNING** | Disarankan menggunakan fitur volatilitas yang digeser satu hari (`.shift(1)`), merefleksikan volatilitas yang tuntas hingga $t-1$. |
| **Centered Moving Averages** | Menggunakan `df.rolling(W, center=True)` yang menarik informasi masa depan sebanyak $\frac{W}{2}$ hari ke depan. | **FAIL** | Seluruh rolling filter wajib menggunakan parameter default `center=False`. |
| **Global Scaling / Normalization** | Menjalankan `StandardScaler.fit()` atau `MinMaxScaler.fit()` pada seluruh 4.266 baris dataset sebelum partisi split. | **WARNING** | Parameter $\mu$ dan $\sigma$ wajib diestimasi secara eksklusif hanya dari data Training ($t \le 2021$). |
| **Global Imputation** | Mengisi nilai kosong (misalnya akibat pembentukan lag) dengan rata-rata global deret waktu. | **WARNING** | Lakukan pemangkasan baris awal (*trimming*) atau forward-fill berbasis historis lokal saja. |
| **Macro Reporting Lags** | Di dunia nyata, angka `CPI` bulanan dirilis BPS pada hari kerja pertama bulan berikutnya. Penggunaan CPI tanggal 1 mengasumsikan angka tersebut langsung diketahui. | **UNVERIFIED** | Dataset peserta menyajikan `CPI` secara harian konstan. Asumsikan data ini observable sesuai baris tanggal yang disediakan. |

---

## 5. Rekomendasi Time-Series Split, Purging, dan Embargo

### 5.1 Kegagalan Skema Validasi Tradisional
Dalam data time-series finansial, penerapan K-Fold Cross Validation acak (`shuffle=True`) adalah kesalahan fatal yang menghasilkan metrik performa palsu (*overly optimistic backtest*). Penyebabnya:
1. **Autokorelasi Temporal:** Observasi hari $t+1$ sangat berkorelasi dengan hari $t$. Jika hari $t$ masuk set latih dan $t+1$ masuk set uji, model hanya menghafal korelasi lokal.
2. **Label Overlap:** Karena target berdurasi 5 hari ke depan, label pada hari $t$ dan $t+1$ berbagi 4 hari return yang persis sama ($r_{t+2}, r_{t+3}, r_{t+4}, r_{t+5}$).

### 5.2 Mengapa Embargo 5 Hari Tidak Otomatis Menyelesaikan Semua Risiko?
Secara teori sederhana, karena target mencakup horizon $[t+1, t+5]$, memberikan jeda (embargo) sebesar 5 hari tampak cukup untuk memisahkan label. Namun secara kuantitatif, anggapan ini **keliru dan berbahaya** karena dua faktor:
1. **Memori Volatilitas Jangka Panjang (ARCH Persistence):**
   - Sebagaimana dibuktikan pada Section 5 laporan EDA, autokorelasi nilai absolut return ($|r_t|$) terbukti signifikan melampaui batas selang kepercayaan 95% **hingga lag 30 hari perdagangan**.
   - Guncangan volatilitas di akhir set latih masih mentransmisikan energi varians ke awal set validasi melampaui jeda 5 hari.
2. **Jendela Rekayasa Fitur Rolling yang Panjang:**
   - Pada Task 1, kita akan merekayasa fitur dengan jendela rolling 10, 20, hingga 60 hari (misalnya moving average kurs atau volatilitas 1 bulan).
   - Jika observasi validasi dimulai pada hari $T_{\text{split}} + 6$ (setelah embargo 5 hari), fitur rolling 20-hari pada observasi tersebut masih menarik data harga dari $T_{\text{split}} - 14$ yang berada di dalam set latih.

### 5.3 Desain Purged Walk-Forward Time-Series Split yang Direkomendasikan
Berdasarkan metodologi *Advances in Financial Machine Learning* (López de Prado), skema partisi yang direkomendasikan adalah **Purged Walk-Forward Split dengan Embargo Diperpanjang**:

```
[────────────── SET LATIH (TRAIN) ──────────────] [PURGE] [EMBARGO] [────── SET VALIDASI (VAL) ──────] [PURGE] [─── TEST ───]
2010-01-04 ─────────────────────────> 2021-12-17  5 hari   10 hari   2022-01-10 ─────────> 2024-12-17   5 hari   2025-01-02 ..
                                      (3.120 baris) (Buffer Gabungan: 15 hari)     (767 baris)          (Buffer)   (359 baris)
```

#### Spesifikasi Parameter Partisi:
1. **Partisi Set Latih (Training Set):**
   - Rentang: **4 Januari 2010 s/d 17 Desember 2021** (~3.120 baris observasi).
   - Mencakup rezim normal, Taper Tantrum 2013, krisis komoditas 2015, dan krisis pandemi COVID-19 2020.
2. **Buffer Purge & Embargo 1 (Batas Train-Validation):**
   - Rentang: **20 Desember 2021 s/d 7 Januari 2022** (15 hari bursa).
   - 5 hari untuk mem-purge target overlap baris akhir Train, dan 10 hari untuk meredam autokorelasi residual volatilitas.
3. **Partisi Set Validasi (Validation Set / Out-of-Sample Backtest):**
   - Rentang: **10 Januari 2022 s/d 17 Desember 2024** (~767 baris observasi).
   - Mewakili rezim kenaikan suku bunga global agresif (*Fed quantitative tightening*), inflasi pasca-pandemi, dan normalisasi pasar.
4. **Buffer Purge 2 (Batas Validation-Test):**
   - Rentang: **18 Desember 2024 s/d 24 Desember 2024** (5 baris observasi batas).
   - Menghilangkan anomali pemotongan kalender akhir 2024 yang teridentifikasi pada audit Section 2.
5. **Partisi Uji Akhir (Competition Test Set):**
   - Rentang: **2 Januari 2025 s/d 22 Mei 2026** (359 baris observasi tanpa label target).

---

## 6. Evaluasi Fitur Kandidat: Rasionalitas vs Bukti Empiris

Tabel berikut membedah secara ketat empat kandidat fitur awal untuk memisahkan narasi finansial dari validasi statistik:

| Fitur Kandidat | Formulasi Matematika | Rasionalitas Finansial | Korelasi Linier ($r$) | Bukti Empiris / Keterbatasan | Status Kelayakan |
|---|---|---|---|---|---|
| **`rv_past5`** | $\text{std}(r_{t-4..t}, \text{ddof}=1)$ | **Sangat Kuat:** Teori *volatility clustering* (ARCH effect) menyatakan bahwa volatilitas saat ini adalah prediktor terbaik volatilitas esok hari. | **+0,4460** | **Terbukti Kuat:** Korelasi positif tinggi, konsisten di seluruh periode. Keterbatasan: Rentan lag saat volatilitas berbalik arah (*mean-reverting*). | **PASS** (Pilar utama; tambahkan variasi jendela 10 & 20 hari). |
| **$X_1$ (`Fear_Liquidity`)** | $VIX_t \times \ln\left(\frac{USDIDR_t}{MA_{20}(USDIDR)_t}\right)$ | **Kuat:** Interaksi non-linier antara ketakutan global ($VIX$) dan tekanan pelarian modal valas domestik (*capital flight*). | **+0,1258** | **Cukup Prospektif:** Scatter plot menunjukkan sinyal tajam saat krisis. Keterbatasan: Sangat sensitif terhadap anomali kurs USDIDR; sinyal nol pada pasar tenang. | **PASS** (Layak diuji di Task 2 setelah koreksi typo USDIDR). |
| **$X_2$ (`Rate_Diff_Pressure`)** | $(BI_t - US_t) \times \Delta\%_5(USDIDR)_t$ | **Moderat:** Mengukur insentif *carry trade* dan transmisi paritas suku bunga (*uncovered interest parity*). | **+0,0124** | **Lemah:** Korelasi linier mendekati nol. Suku bunga bersifat tangga bulanan, sehingga dinamika harian didominasi fluktuasi acak kurs. | **WARNING** (Perlu reformulasi: gunakan nilai absolut atau selisih laju perubahan suku bunga). |
| **$X_3$ (`Commodity_Macro_Shock`)** | $\Delta\%_5 OIL \times \Delta\%_5 GOLD \times \Delta\%_5 SP500$ | **Lemah secara Matematis:** Hipotesis guncangan simultan 3 pilar makro (energi, safe haven, ekuitas AS). | **-0,1016** | **Gagal Metodologis:** Perkalian tiga return menghasilkan magnitudo mikroskopis ($10^{-6}$) dan pembatalan tanda guncangan (negatif $\times$ negatif = positif). | **FAIL** (Ditolak dalam bentuk perkalian; ganti dengan norma L2 vektor return makro). |

---

## 7. Rekomendasi Tindakan Menuju Task 1 & Task 2

Sesuai pembatasan Checkpoint 1A, tidak ada pemodelan, tuning hyperparameter, SHAP, atau pembuatan prediksi yang dilakukan. Rekomendasi teknis yang wajib diimplementasikan saat melangkah ke fase berikutnya:

1. **Pipeline Preprocessing Deterministik:**
   - Buat fungsi penanganan kurs `USDIDR` yang mengoreksi nilai di bawah 1.000 dengan perkalian $10\times$ tanpa menyentuh file CSV mentah.
   - Pertahankan nilai `OIL = -37.63` secara utuh.
2. **Rekayasa Fitur Lanjutan (Task 1):**
   - Kembangkan fitur volatilitas bergulir multi-skala: `rv_past5`, `rv_past10`, `rv_past20`, dan `rv_past60` dengan proteksi lookahead bias.
   - Reformulasi fitur $X_2$ menjadi magnitudo tekanan suku bunga mutlak $|BI - US| \times |\Delta\% USDIDR|$.
   - Gantikan fitur $X_3$ dengan *Macro Stress Index* berbasis agregasi magnitudo atau Principal Component Analysis (PCA) dari return komoditas.
3. **Penyusunan Pipeline Modeling Anti-Leakage (Task 2):**
   - Terapkan modul *Purged TimeSeriesSplit* dengan buffer embargo 15 hari di batas train-val.
   - Pastikan seluruh proses standardisasi data dibungkus di dalam `sklearn.pipeline.Pipeline` agar scaler tidak pernah melihat data validasi sebelum evaluasi.
