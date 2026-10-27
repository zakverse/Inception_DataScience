# Laporan Rancangan Feature Engineering & Audit Metodologis — Checkpoint 1B

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 1B (Finalisasi Feature Engineering & Verifikasi Pra-Modeling)  
**Modul Kode:** [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py)  
**Dokumen Rujukan:** [`docs/checkpoint_1a_verification.md`](file:///z:/Projects/Inception/docs/checkpoint_1a_verification.md), [`docs/EDA_analysis_report.md`](file:///z:/Projects/Inception/docs/EDA_analysis_report.md), `Aset Lomba/dataset peserta.csv`, `Aset Lomba/Studi Kasus.docx`

---

## 1. Executive Summary

Checkpoint 1B mengonsolidasikan arsitektur rekayasa fitur (*feature engineering*) untuk Task 1 kompetisi INCEPTION 2026. Fokus utama pekerjaan ini adalah:
1. Membangun modul Python terisolasi ([`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py)) yang memproses data mentah secara deterministik tanpa pernah menimpa file CSV asli maupun notebook EDA yang sudah rampung.
2. Mengimplementasikan fungsi pembersihan anomali skala kurs `USDIDR` yang memiliki mekanisme validasi ketat (*strict assertions*) dan pencatatan audit (*audit logging*).
3. Merekayasa 14 fitur prediktor historis yang mencakup persistensi volatilitas multi-skala, momentum pasar saham, transmisi nilai tukar, guncangan sentimen global (VIX), serta implementasi 3 fitur wajib ($X_1, X_2, X_3$) bersama formula alternatif yang lebih robust secara matematis.
4. Memvalidasi seluruh fitur melalui suite pengujian otomatis 5 tahap, termasuk uji invariansi masa depan (*empirical future perturbation test*) untuk membuktikan ketiadaan *lookahead bias*.

### Ringkasan Status Kesiapan Fitur

| Kategori Fitur | Jumlah Fitur | Status Pengujian | Kesiapan Pemodelan |
|---|---|---|---|
| **Preprocessing Kurs USD/IDR** | 1 kolom (`USDIDR_clean`) | **PASS** (100% tervalidasi) | Siap digunakan di seluruh fitur turunan valas |
| **Volatilitas Multi-Scale IHSG** | 3 fitur (`rv_past5`, `rv_past10`, `rv_past20`) | **PASS** (Korelasi vs Y: +0,45 s/d +0,49) | Pilar utama prediktor awal |
| **Momentum Asimetris IHSG** | 2 fitur (`mom_ihsg_5`, `mom_ihsg_10`) | **PASS** (Korelasi vs Y: -0,23 s/d -0,28) | Menangkap efek leverage finansial |
| **Tekanan Nilai Tukar Valas** | 1 fitur (`usdidr_ret5`) | **PASS** (Korelasi vs Y: +0,14) | Sinyal terpulihkan pasca-koreksi kurs |
| **Kejutan Kepanikan Global (VIX)** | 2 fitur (`vix_ratio_ma20`, `vix_diff_ma20`) | **PASS** (Korelasi vs Y: +0,22 s/d +0,24) | Menangkap rezim kepanikan pasar global |
| **Fitur Wajib $X_1$ (Fear Liquidity)** | 2 varian (Original & Robust Taylor) | **PASS** (Korelasi vs Y: +0,34 s/d +0,35) | Siap diuji di Task 2 & Task 3 |
| **Fitur Wajib $X_2$ (Rate Differential)** | 2 varian (Original & Absolute Stress) | **PASS** (Korelasi vs Y: +0,11 s/d +0,20) | Alternatif absolut lebih kuat menangkap stres |
| **Fitur Wajib $X_3$ (Macro Shock)** | 2 varian (Original & L2 Euclidean Norm) | **PASS** (Korelasi vs Y: -0,10 s/d +0,16) | Alternatif norma L2 menyelesaikan anomali skala |

---

## 2. Kebijakan Preprocessing & Audit Anomali Kurs USD/IDR

### 2.1 Aturan Koreksi Eksplisit
Fungsi `preprocess_usdidr()` pada modul [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) dirancang dengan aturan pengamanan ketat:
1. **Preservasi Data Mentah:** Kolom asli `USDIDR` disalin menjadi `USDIDR_raw` sebelum proses apa pun. Data hasil koreksi disimpan pada kolom baru `USDIDR_clean`. File `Aset Lomba/dataset peserta.csv` **tidak dimodifikasi sama sekali**.
2. **Validasi Kondisi Eksak Sebelum Koreksi:**
   - Tanggal target 1: `2010-11-01` wajib bernilai dalam rentang $[800.0, 950.0]$ (nilai aktual: `888.109985`).
   - Tanggal target 2: `2012-02-07` wajib bernilai dalam rentang $[800.0, 950.0]$ (nilai aktual: `892.000000`).
   - Jika salah satu baris tidak ditemukan atau nilainya di luar ambang batas yang diharapkan, sistem langsung berhenti dengan `ValueError` eksplisit.
3. **Penerapan Transformasi Skala:**
   - Baris 2010-11-01 dikalikan dengan faktor $10,0 \rightarrow 8.881,099850$.
   - Baris 2012-02-07 dikalikan dengan faktor $10,0 \rightarrow 8.920,000000$.
4. **Pencatatan Audit (*Audit Logging*):**
   Setiap eksekusi fungsi menghasilkan dictionary log terstruktur berisi tanggal perubahan, nilai sebelum, nilai sesudah, faktor pengali, dan rujukan bukti.

### 2.2 Dampak Kuantitatif Pembersihan Kurs terhadap Return Valas

| Indeks Baris | Tanggal Observasi | Kurs Mentah (`USDIDR_raw`) | Return Harian Mentah | Kurs Bersih (`USDIDR_clean`) | Return Harian Bersih |
|---|---|---|---|---|---|
| **214** | 2010-10-29 | 8.923,799805 | 0,00% | 8.923,799805 | 0,00% |
| **215** | **2010-11-01** | **888,109985** | **-90,05%** | **8.881,099850** | **-0,48%** |
| **216** | 2010-11-02 | 8.906,700195 | **+902,88%** | 8.906,700195 | **+0,29%** |
| **545** | 2012-02-06 | 8.928,099609 | -0,34% | 8.928,099609 | -0,34% |
| **546** | **2012-02-07** | **892,000000** | **-90,01%** | **8.920,000000** | **-0,09%** |
| **547** | 2012-02-08 | 8.930,000000 | **+901,12%** | 8.930,000000 | **+0,11%** |

### 2.3 Status Bukti & Keterbatasan
- **Bukti Konfirmasi Kuat:**
  1. *Signifikansi Digit Identik:* Angka signifikan $8881$ dan $8920$ persis menyatu dengan deret waktu tetangganya ($8923 \rightarrow 8881 \rightarrow 8906$ dan $8928 \rightarrow 8920 \rightarrow 8930$). Bahkan nilai $8920,0$ persis muncul kembali pada penutupan tanggal 2012-02-10 ($8.920,00$).
  2. *Konsistensi Makroekonomi:* Kurs referensi historis Bank Indonesia (JISDOR/Kurs Transaksi) mencatat kurs Rupiah pada November 2010 berkisar Rp8.850–Rp8.950/USD dan Februari 2012 berkisar Rp8.900–Rp9.000/USD. Nilai Rp888/USD tidak pernah terjadi dalam sejarah moneter Indonesia pasca-krisis 1998.
- **Keterbatasan:** Koreksi ini merupakan inferensi deduktif berdasarkan bukti data historis eksternal dan kontinuitas numerik, bukan berasal dari konfirmasi langsung panitia penyelenggara. Oleh karena itu, aturan koreksi diisolasi ke dalam fungsi independen yang dapat dinonaktifkan (`use_cleaned_usdidr=False`) jika diperlukan untuk komparasi uji sensitivitas.

---

## 3. Matriks Rancangan Fitur Historis & Wajib

Tabel berikut mendokumentasikan secara lengkap seluruh 14 fitur prediktor yang diimplementasikan pada modul [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py):

| Nama Kolom Fitur | Formulasi Matematika | Jendela Observasi | Waktu Ketersediaan | Hipotesis Finansial | Risiko Leakage | Rencana Evaluasi di Task 2 & 3 | Status Kelayakan |
|---|---|---|---|---|---|---|---|
| `rv_past5` | $\text{std}(r_{t-4..t}, \text{ddof}=1)$ | 5 hari $[t-4, t]$ | EOD $t$ | *Volatility clustering* jangka pendek (ARCH effect). | Rendah jika EOD $t$; overlap jika SOD $t$. | Baseline regresi & SHAP importance global. | **PASS** |
| `rv_past10` | $\text{std}(r_{t-9..t}, \text{ddof}=1)$ | 10 hari $[t-9, t]$ | EOD $t$ | Estimasi volatilitas 2 pekan yang lebih mulus dari noise harian. | Rendah (EOD $t$). | Feature ablation study vs `rv_past5`. | **PASS** |
| `rv_past20` | $\text{std}(r_{t-19..t}, \text{ddof}=1)$ | 20 hari $[t-19, t]$ | EOD $t$ | Volatilitas bulanan; menangkap pergeseran rezim stres pasar. | Rendah (EOD $t$). | Korelasi silang & VIF collinearity check. | **PASS** |
| `mom_ihsg_5` | $\frac{\text{IHSG}_t - \text{IHSG}_{t-5}}{\text{IHSG}_{t-5}}$ | 5 hari $[t-5, t]$ | EOD $t$ | *Asymmetric leverage effect*: penurunan pasar memicu lonjakan volatilitas. | Bebas leakage (EOD $t$). | Analisis korelasi parsial terhadap target. | **PASS** |
| `mom_ihsg_10` | $\frac{\text{IHSG}_t - \text{IHSG}_{t-10}}{\text{IHSG}_{t-10}}$ | 10 hari $[t-10, t]$ | EOD $t$ | Tren menengah pasar saham; konfirmasi pelemahan struktural. | Bebas leakage (EOD $t$). | Analisis interaksi pohon keputusan (LightGBM). | **PASS** |
| `usdidr_ret5` | $\frac{\text{USDIDR}_t - \text{USDIDR}_{t-5}}{\text{USDIDR}_{t-5}}$ | 5 hari $[t-5, t]$ | EOD $t$ | Depresiasi tajam Rupiah memicu pelarian modal asing dari ekuitas. | Sangat sensitif typo USDIDR jika uncleaned. | Uji sensitivitas model dengan vs tanpa koreksi kurs. | **PASS** |
| `vix_ratio_ma20` | $\frac{\text{VIX}_t}{\text{MA}_{20}(\text{VIX})_t}$ | 20 hari $[t-19, t]$ | EOD $t$ | Guncangan kepanikan mendadak global relatif terhadap baseline 1 bulan. | Proteksi pembagian nol wajib aktif. | SHAP dependence plot terhadap nilai ekstrem VIX. | **PASS** |
| `vix_diff_ma20` | $\text{VIX}_t - \text{MA}_{20}(\text{VIX})_t$ | 20 hari $[t-19, t]$ | EOD $t$ | Selisih poin absolut kepanikan global; menangkap magnitudo stres. | Bebas leakage (EOD $t$). | Pemilihan fitur linear vs ratio di regresi. | **PASS** |
| `X1_Fear_Liquidity_Original` | $\text{VIX}_t \times \ln\left(\frac{\text{USDIDR}_t}{\text{MA}_{20}(\text{USDIDR})_t}\right)$ | 20 hari $[t-19, t]$ | EOD $t$ | Interaksi non-linier kepanikan global $\times$ pelarian likuiditas valas. | Risiko singularity jika ratio $\le 0$ (terlindungi). | Benchmarking terhadap formula alternatif $X_{1,\text{robust}}$. | **PASS** |
| `X1_Fear_Liquidity_Robust` | $\text{VIX}_t \times \left(\frac{\text{USDIDR}_t - \text{MA}_{20}}{\text{MA}_{20}}\right)$ | 20 hari $[t-19, t]$ | EOD $t$ | Linierisasi Taylor dari $X_1$; menghindari distorsi logaritmik. | Bebas leakage (EOD $t$). | Perbandingan R-squared dan MAE model. | **PASS** |
| `X2_Rate_Diff_Pressure_Original` | $(\text{BI}_t - \text{US}_t) \times \text{usdidr\_ret5}_t$ | 5 hari $[t-5, t]$ | EOD $t$ | Insentif *carry trade* $\times$ realisasi risiko volatilitas kurs. | Suku bunga berupa tangga; korelasi linier lemah. | Uji feature importance Tree vs Linear. | **WARNING** |
| `X2_Rate_Diff_Pressure_Abs` | $|\text{BI}_t - \text{US}_t| \times |\text{usdidr\_ret5}_t|$ | 5 hari $[t-5, t]$ | EOD $t$ | Magnitudo mutlak tekanan makro-moneter tanpa pembatalan tanda. | Bebas leakage (EOD $t$). | Uji signifikansi out-of-sample di Task 2. | **PASS** |
| `X3_Commodity_Shock_Original` | $\Delta\%_5 \text{OIL} \times \Delta\%_5 \text{GOLD} \times \Delta\%_5 \text{SP500}$ | 5 hari $[t-5, t]$ | EOD $t$ | Guncangan simultan energi, safe-haven, dan pasar ekuitas AS. | Skala mikroskopis ($10^{-6}$); tanda arah ambigu. | Dokumentasikan kelemahan di Task 3. | **FAIL / OBSOLETE** |
| `X3_Commodity_Shock_L2Norm` | $\sqrt{(\Delta\%_5 \text{OIL})^2 + (\Delta\%_5 \text{GOLD})^2 + (\Delta\%_5 \text{SP500})^2}$ | 5 hari $[t-5, t]$ | EOD $t$ | Norma Euclidean guncangan makro global; selalu positif dan berskala wajar. | Bebas leakage (EOD $t$). | Evaluasi kontribusi prediksi saat shock komoditas 2020. | **PASS** |

---

## 4. Analisis Mendalam Karakteristik Statistik Fitur

Tabel berikut menyajikan statistik deskriptif dan korelasi empiris terhadap `Target_Volatilitas_Y` pada seluruh 3.907 baris data berlabel:

| Nama Kolom Fitur | Mean | Std Dev | Min | Max | Korelasi Pearson vs Target ($Y$) | Jumlah Awal NaN |
|---|---|---|---|---|---|---|
| `rv_past5` | 0,0083 | 0,0056 | 0,0000 | 0,0585 | **+0,4460** | 5 |
| `rv_past10` | 0,0087 | 0,0050 | 0,0022 | 0,0508 | **+0,4935** | 10 |
| `rv_past20` | 0,0089 | 0,0046 | 0,0030 | 0,0412 | **+0,4731** | 20 |
| `mom_ihsg_5` | 0,0015 | 0,0221 | -0,1614 | 0,1527 | **-0,2295** | 5 |
| `mom_ihsg_10` | 0,0031 | 0,0305 | -0,2718 | 0,2136 | **-0,2840** | 10 |
| `usdidr_ret5` (Clean) | 0,0008 | 0,0140 | -0,1798 | 0,2483 | **+0,1444** | 5 |
| `vix_ratio_ma20` | 1,0035 | 0,1608 | 0,6910 | 2,8306 | **+0,2238** | 19 |
| `vix_diff_ma20` | -0,0115 | 3,4334 | -17,6910 | 43,8400 | **+0,2390** | 19 |
| `X1_Fear_Liquidity_Original` | 0,0391 | 0,4059 | -2,1618 | 7,2062 | **+0,3446** | 19 |
| `X1_Fear_Liquidity_Robust` | 0,0416 | 0,4143 | -2,0981 | 7,6441 | **+0,3504** | 19 |
| `X2_Rate_Diff_Pressure_Original` | 0,0041 | 0,0874 | -1,3320 | 1,8397 | **+0,1103** | 5 |
| `X2_Rate_Diff_Pressure_Abs` | 0,0372 | 0,0791 | 0,0000 | 1,8397 | **+0,1968** | 5 |
| `X3_Commodity_Shock_Original` | -0,000002 | 0,000127 | -0,0048 | 0,0019 | **-0,1016** | 5 |
| `X3_Commodity_Shock_L2Norm` | 0,0495 | 0,0626 | 0,0018 | 2,6794 | **+0,1642** | 5 |

### Temuan Kuantitatif Penting:
1. **Keunggulan Jendela Menengah (`rv_past10`):** Korelasi univariat `rv_past10` ($+0,4935$) melampaui `rv_past5` ($+0,4460$). Jendela 10 hari memberikan estimasi varians yang lebih stabil dan tahan terhadap *one-day outlier spike*.
2. **Asimetri Pasar Terbukti Kuat:** Korelasi negatif momentum (`mom_ihsg_10` = $-0,2840$) mengonfirmasi teori ekonometrika keuangan: penurunan tajam harga saham memicu kepanikan dan meningkatkan volatilitas jauh lebih besar dibanding kenaikan harga yang stabil.
3. **Pemulihan Sinyal Valas Pasca-Koreksi:** Sebelum kurs `USDIDR` dibersihkan, korelasi return valas terhadap target tertutup noise ($r = +0,0138$). Setelah koreksi desimal, korelasi naik menjadi **$+0,1444$**, membuktikan bahwa hubungan ekonomi riil berhasil diselamatkan.
4. **Validasi Varian Alternatif $X_1, X_2, X_3$:**
   - $X_1$ versi robust menghasilkan korelasi **$+0,3504$** (tertinggi di antara fitur interaksi).
   - $X_2$ versi absolut melipatgandakan korelasi dari $+0,1103$ menjadi **$+0,1968$**.
   - $X_3$ versi norma L2 membalik korelasi bermasalah $-0,1016$ menjadi korelasi positif rasional **$+0,1642$** dengan skala angka yang stabil (mean $0,0495$).

---

## 5. Landasan Alignment Temporal & Pembuktian Non-Leakage

### 5.1 Justifikasi Teoretis Waktu Prediksi End-of-Day (EOD $t$)
SOP kompetisi menuntut pembuktian bahwa fitur pada hari $t$ tidak menyenggol informasi masa depan ($t+1$). Alignment waktu prediksi ditetapkan secara eksplisit:

```
            Selesai Perdagangan Hari t (EOD t)
                           │
 ──[Data Historis <= t]────┼─────[Horizon Realisasi Target t+1 .. t+5]────> Waktu
   r_{t-4}, ..., r_t       │      r_{t+1}, r_{t+2}, r_{t+3}, r_{t+4}, r_{t+5}
 ◄─────────────────────────┤      ├─────────────────────────────────────────►
    Fitur Prediktor X_t                         Target Y_t
```

1. **Harga Penutupan Hari $t$ Sudah Final:** Pada pukul 16:30 WIB hari $t$, bursa saham domestik telah ditutup. Harga penutupan `IHSG_t` dan return harian $r_t = \frac{\text{IHSG}_t - \text{IHSG}_{t-1}}{\text{IHSG}_{t-1}}$ sudah menjadi fakta historis yang observable.
2. **Target Berada Sepenuhnya di Masa Depan:** Target $\text{Target\_Volatilitas\_Y}_t$ mengukur deviasi standar return pada hari kerja $t+1$ hingga $t+5$.
3. **Ketiadaan Irisan (Zero Overlap):**
   $$\text{Window}(X_t) = (-\infty, t] \quad \cap \quad \text{Window}(Y_t) = [t+1, t+5] \quad = \quad \emptyset$$
   Karena irisan keduanya adalah himpunan kosong, penggunaan data hingga penutupan hari $t$ **secara matematis bebas dari kebocoran informasi target**.

### 5.2 Mengapa `shift(1)` Tidak Boleh Diterapkan Secara Membabi Buta?
Penerapan `shift(1)` pada seluruh fitur tanpa memahami waktu eksekusi justru menciptakan inefisiensi metodologis:
- Jika model dieksekusi saat EOD $t$, membuang informasi return hari $t$ dengan memaksakan `shift(1)` akan menghilangkan informasi terbaru (*stale information bias*).
- Namun, **JIKA skenario operasional digeser ke Start-of-Day (SOD $t$, sebelum bursa buka)**, maka harga penutupan hari $t$ belum ada. Dalam skenario SOD tersebut, `shift(1)` wajib diterapkan.
- Dalam modul ini, seluruh formula dirancang konsisten untuk skenario EOD $t$, dan dokumentasi batasan ini dicatat secara transparan.

---

## 6. Hasil Eksekusi Suite Pengujian Otomatis

Eksekusi script [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) memicu suite pengujian otomatis independen yang memverifikasi integritas data:

```
=================================================================
HASIL EKSEKUSI PENGUJIAN FITUR (SUITE OTOMATIS)
=================================================================
[PASS] test_1_date_monotonic          : Tanggal terurut monotonik naik (2010-01-04 -> 2026-05-22, N=4266)
[PASS] test_2_usdidr_correction       : Baris 215 (888.11 -> 8881.10) & Baris 546 (892.00 -> 8920.00) tervalidasi
[PASS] test_3_numerical_sanity        : 0 nilai np.inf atau -np.inf pada seluruh 19 kolom numerik
[PASS] test_4_window_alignment        : Jumlah awal NaN persis sesuai panjang jendela (rv5=5, rv20=20)
[PASS] test_5_anti_leakage_invariance : Uji perturbasi masa depan t+1..t+K menghasilkan selisih fitur baris t = 0.000000
=================================================================
STATUS KESELURUHAN: ALL 5 FEATURE ENGINEERING TESTS PASSED! [OK]
=================================================================
```

### Rincian Uji Anti-Leakage (Test 5: Future Data Invariance Test)
Uji ini dilakukan secara deterministik:
1. Memilih baris acak $t = 1000$ (tanggal 2013-11-20).
2. Mencatat nilai fitur pada baris 1000 (`rv_past20`, `X1_robust`, `X3_l2norm`).
3. Memutilasi seluruh data masa depan dari baris 1001 hingga 4266 dengan mengalikan harga IHSG, VIX, OIL, GOLD, SP500, dan USDIDR sebesar **$1.000\times$** (lonjakan artifisial ekstrem).
4. Menghitung ulang seluruh pipeline fitur dari data yang telah dimutilasi.
5. Membandingkan nilai fitur baris 1000 sebelum vs sesudah mutilasi:
   - Deviasi `rv_past20`: **0,000000000000**
   - Deviasi `X1_Fear_Liquidity_Robust`: **0,000000000000**
   - Deviasi `X3_Commodity_Shock_L2Norm`: **0,000000000000**
6. **Kesimpulan Uji:** Terbukti secara komputasi bahwa fitur pada baris $t$ **sama sekali tidak memiliki akses read maupun backward dependency ke data masa depan ($> t$)**.

### Keterbatasan Pengujian Secara Eksplisit
Meskipun 5 unit test di atas berstatus **PASS**, analis wajib mengakui keterbatasan berikut:
1. Uji invariansi hanya membuktikan bahwa *fungsi pembuatan fitur* bersifat kausal. Uji ini **tidak otomatis mencegah leakage pada tahap pemisahan data (split)** jika train-val split dilakukan tanpa embargo 15 hari.
2. Koreksi kurs USDIDR didasarkan pada inferensi tetangga dan referensi BI historis; data asli dari penyedia data pihak ketiga kompetisi belum dapat diaudit secara independen.
3. Korelasi in-sample yang tinggi pada $X_1$ ($+0,35$) dan `rv_past10` ($+0,49$) **belum menjamin performa prediksi out-of-sample**; evaluasi sesungguhnya baru akan terbukti pada Task 2 dan Task 3.

---

## 7. Rekomendasi Persiapan Menuju Task 2

Dengan tuntasnya Checkpoint 1B, seluruh fondasi data dan rekayasa fitur telah siap untuk melangkah ke Task 2. Prosedur yang direkomendasikan:
1. **Import Modul:** Di Task 2 dan Task 3, gunakan `from scripts.feature_engineering import preprocess_usdidr, engineer_features` sebagai pipeline standar.
2. **Gunakan Fitur Alternatif yang Lebih Robust:** Utamakan pengujian model menggunakan `X1_Fear_Liquidity_Robust`, `X2_Rate_Diff_Pressure_Abs`, dan `X3_Commodity_Shock_L2Norm` di samping formula original untuk membuktikan keunggulan stabilitasnya pada SHAP analysis (Task 3).
3. **Terapkan Purged Walk-Forward Split:** Partisi dataset sesuai rekomendasi Checkpoint 1A dengan embargo 15 hari di batas 2021/2022.
4. **Pencegahan Global Scaling Leakage:** Pastikan `StandardScaler` hanya di-fit pada partisi Train di dalam pipeline `scikit-learn`.
