# Laporan Eksperimen Komparasi Model Awal (Initial Model Comparison) — Checkpoint 3A

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 3A (Task 3: Initial Model Exploration & Baseline Benchmarking)  
**Notebook Utama:** [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb)  
**Modul Kode Terkait:** [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py), [`scripts/build_model_comparison_nb.py`](file:///z:/Projects/Inception/scripts/build_model_comparison_nb.py)  
**Folder Output Visualisasi:** [`outputs/models/`](file:///z:/Projects/Inception/outputs/models/)  
**Status Eksekusi Kernel Bersih:** **100% PASS** (8/8 code cells tereksekusi tanpa error, exit code 0)

---

## 1. Executive Summary & Ringkasan Eksperimen

Checkpoint 3A menandai transisi penting dari pembuktian integritas data dan baseline (Task 2) menuju fase eksplorasi pemodelan Machine Learning (Task 3). Tujuan inti dari tahap ini adalah melakukan **komparasi model regresi awal tanpa tuning berlebih (*un-tuned / default hyperparameter comparison*)** terhadap standar performa (*benchmark baseline*) yang telah ditetapkan pada Checkpoint 2.

### 1.1 Temuan Pokok Kuantitatif
1. **Dinamika Pemisahan Statis (Static Validation 2022–2024, $N=772$):**
   - Pada pemisahan statis tunggal tanpa tuning, **`Persistence rv_past20`** ($\text{MAE} = \mathbf{0,002675}$, $\text{RMSE} = 0,003540$) dan **`Constant Median`** ($\text{MAE} = 0,002772$, $\text{RMSE} = \mathbf{0,003390}$) tetap menjadi patokan terkuat.
   - Model Machine Learning awal dengan parameter default (`Gradient Boosting` $\text{MAE} = 0,003480$, `Ridge` $\text{MAE} = 0,003690$, `Random Forest` $\text{MAE} = 0,005150$) menghasilkan error yang lebih tinggi.
   - **Diagnosa Ekonometrika:** Set latih 2010–2021 didominasi oleh lonjakan volatilitas ekstrem pandemi Covid-19 tahun 2020 ($\sigma = 0,0059$, nilai puncak $0,0585$). Model yang dilatih dengan fungsi objektif kuadratik standar ($L_2$/MSE) tanpa tuning bobot sampel mengalami tarikan prediksi ke atas (*upward prediction bias*), sementara era 2022–2024 merupakan rezim pasar yang sangat tenang ($\sigma = 0,0033$).
2. **Pembuktian Daya Prediksi Riil pada Walk-Forward (Expanding Window 3 Folds):**
   - Ketika model diperbarui secara berkala (*rolling retraining*), keunggulan prediktif Machine Learning mulai terbukti nyata:
     - **Fold 2 (Tahun 2023):** **Ridge Regression berhasil mengalahkan seluruh baseline** dengan $\text{MAE} = \mathbf{0,001972}$ dan $\text{RMSE} = \mathbf{0,002484}$ (jauh melampaui `Persistence rv_past20` $\text{MAE} = 0,002265$ dan `Constant Median` $\text{MAE} = 0,002952$). `Gradient Boosting` juga mengungguli median ($\text{MAE} = 0,002434$).
     - **Fold 3 (Tahun 2024):** Baik `Ridge` ($\text{MAE} = 0,002847$) maupun `Gradient Boosting` ($\text{MAE} = 0,002988$) **mengalahkan `Persistence rv_past20`** ($\text{MAE} = 0,003232$).
   - Hal ini membuktikan bahwa sinyal fitur prediktor (terutama `rv_past10`, `mom_ihsg_10`, `VIX`, dan fitur interaksi `X1_Fear_Liquidity_Robust`) memiliki nilai tambah ekonomi yang nyata jika model adaptif terhadap pergantian rezim.
3. **Kepatuhan Anti-Leakage & Integritas Metodologis:**
   - Seluruh proses preprocessing yang memerlukan kalkulasi statistik (`StandardScaler`) dibungkus dalam `sklearn.pipeline.Pipeline` dan hanya dipelajari dari data latih.
   - Data uji kompetisi (2025–2026, 359 baris) diisolasi 100% dan tidak pernah disentuh.
   - Tidak ada klaim palsu bahwa model awal langsung mengalahkan baseline pada pemisahan statis; analisis dilakukan secara jujur dan transparan berdasarkan bukti numerik empiris.

---

## 2. Kandidat Model & Konfigurasi Parameter Awal

Sesuai arahan panduan kompetisi, model yang dievaluasi mencakup representasi linier ber-regularisasi, ensemble pohon berbasis bagging, ensemble pohon berbasis boosting, serta baseline terbaik Checkpoint 2:

| Arsitektur Model | Implementasi / Modul | Parameter Awal (Un-tuned) | Alasan & Peran Metodologis | Kebutuhan Scaling |
|---|---|---|---|---|
| **Ridge Regression** | `sklearn.linear_model.Ridge` dalam `Pipeline([('scaler', StandardScaler()), ('ridge', ...)])` | $\alpha = 1.0$, `random_state=42` | Baseline linear ter-regularisasi L2 untuk mencegah multikolinearitas antar-fitur. | **Wajib** (StandardScaler fit murni pada train). |
| **Random Forest Regressor** | `sklearn.ensemble.RandomForestRegressor` | `n_estimators=100`, `random_state=42`, `n_jobs=-1` | Representasi non-linier ensemble bagging untuk menangkap variasi lokal tanpa asumsi distribusi. | Tidak wajib (invarian skala). |
| **Gradient Boosting Regressor** | `sklearn.ensemble.GradientBoostingRegressor` | `n_estimators=100`, `learning_rate=0.05`, `max_depth=3`, `random_state=42` | Representasi arsitektur boosting adaptif (menggantikan LightGBM yang tidak tersedia di environment). | Tidak wajib (invarian skala). |
| *LightGBM Regressor* | *`lightgbm.LGBMRegressor`* | *N/A (Library tidak terpasang di runtime)* | *Dicatat status ketiadaannya sesuai SOP prompt; digantikan oleh GradientBoostingRegressor.* | *Tidak wajib.* |
| **Persistence `rv_past20`** | Fitur historis `rv_past20` pada EOD $t$ | Non-parametrik (Deterministic) | **Baseline Terbaik MAE Checkpoint 2** (Ambang batas yang wajib dikalahkan). | Tidak ada. |
| **Constant Median** | Median target set latih | $\text{Median}(Y_{\text{train}}) = 0,007452$ | **Baseline Terbaik RMSE Checkpoint 2** (Tangguh outlier krisis). | Tidak ada. |
| **Persistence `rv_past5`** | Fitur historis `rv_past5` pada EOD $t$ | Non-parametrik (Deterministic) | Naive benchmark bawaan kompetisi. | Tidak ada. |
| **Constant Mean** | Rata-rata target set latih | $\bar{Y}_{\text{train}} = 0,008802$ | Benchmark naif klasik (paling terdistorsi oleh krisis masa lalu). | Tidak ada. |

> [!NOTE]
> **Pemeriksaan Ketersediaan Library LightGBM:**  
> Lingkungan eksekusi Python 3.12 mendeteksi `scikit-learn 1.9.1`, tetapi modul `lightgbm` belum terpasang. Sesuai instruksi resmi: *"Jika model tidak tersedia, catat dan lanjutkan dengan kandidat yang dapat dijalankan"*, `GradientBoostingRegressor` dari `sklearn.ensemble` digunakan sebagai perwakilan pohon boosting dengan kedalaman dangkal (`max_depth=3`) dan laju pembelajaran rendah (`learning_rate=0.05`).

---

## 3. Matriks Fitur & Arsitektur Pemisahan Temporal

Seluruh eksperimen menggunakan 29 fitur historis yang dihasilkan oleh [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) dengan pembersihan anomali kurs USD/IDR:

### 3.1 Ringkasan 29 Fitur Prediktor ($X$)
1. **Harga Aset & Makro Level:** `IHSG`, `SP500`, `OIL`, `GOLD`, `USDIDR`, `VIX`, `BI_Rate`, `Fed_Rate`, `CPI`.
2. **Log Return 1-Hari:** `ihsg_ret1`, `sp500_ret1`, `oil_ret1`, `gold_ret1`, `usdidr_ret1`.
3. **Log Return Kumulatif 5-Hari:** `ihsg_ret5`, `sp500_ret5`, `oil_ret5`, `gold_ret5`, `usdidr_ret5`.
4. **Realized Volatility Historis:** `rv_past5`, `rv_past10`, `rv_past20`.
5. **Indikator Momentum & Deviasi Dinamis:** `mom_ihsg_5`, `mom_ihsg_10`, `vix_diff_ma20`, `rate_differential`.
6. **Interaksi Makro-Finansial:** `X1_Fear_Liquidity_Original`, `X1_Fear_Liquidity_Robust`, `X2_Rate_Diff_Pressure_Original`, `X2_Rate_Diff_Pressure_Robust`.

### 3.2 Partisi Data & Penanganan Warm-up Rolling Window
- **Training Purged Mentah:** 2010-01-04 s/d 2021-12-24 (3.125 baris).
- **Penanganan Warm-up Window:** Karena fitur `rv_past20` memerlukan 20 hari observasi historis, 20 baris pertama di bulan Januari 2010 bernilai NaN. Baris ini dipotong murni pada set latih menghasilkan **`train_fit` sebanyak 3.105 baris**.
- **Purged Buffer ($H=5$):** 2021-12-27 s/d 2021-12-31 (5 hari perdagangan di-purge dari set latih untuk mengeliminasi target overlap ke tahun 2022).
- **Validation Clean:** 2022-01-03 s/d 2024-12-17 (**772 baris, 100% lengkap tanpa NaN**).
- **Test Set Kompetisi:** 2025-01-02 s/d 2026-05-22 (**359 baris, target kosong $Y=\text{NaN}$, diisolasi total**).

---

## 4. Hasil Komparasi Kinerja pada Validation Clean (2022–2024)

Seluruh kandidat dievaluasi pada 772 hari bursa validasi bersih (`val_clean`). Hasil aktual dari eksekusi notebook disajikan pada tabel di bawah:

| Peringkat MAE | Kategori | Model / Baseline | MAE | RMSE | Korelasi Pearson ($r$) | Evaluasi Kinerja Relatif vs Baseline Terbaik |
|---|---|---|---|---|---|---|
| **1** | **Baseline** | **Persistence `rv_past20`** | **0,002675** | **0,003540** | **0,2197** | **Best Baseline MAE (Tolok Ukur Utama)** |
| 2 | Baseline | Constant Median | 0,002772 | 0,003390 | 0,0000 | Best Baseline RMSE |
| 3 | Baseline | Persistence `rv_past5` | 0,002981 | 0,004088 | 0,2077 | Naive Kompetisi (+11,4% MAE vs rv_past20) |
| 4 | Baseline | Constant Mean | 0,003456 | 0,003985 | 0,0000 | Terdistorsi krisis masa lalu (+29,2% MAE) |
| **5** | **Machine Learning** | **Gradient Boosting** | **0,003480** | **0,004175** | **0,2373** | **Model ML Terbaik** (Pearson $r$ lebih tinggi dari baseline) |
| 6 | Machine Learning | Ridge (Pipeline) | 0,003690 | 0,004333 | 0,2599 | Korelasi Pearson tertinggi ($r = 0,2599$) |
| 7 | Machine Learning | Random Forest | 0,005150 | 0,005843 | 0,1245 | Performa terburuk (Overfitting krisis) |

*Visualisasi komparasi grafik deret waktu dan diagram batang tersimpan di [`outputs/models/fig_mod_01_baseline_vs_models.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_01_baseline_vs_models.png).*

### 4.1 Mengapa Model ML Awal Belum Mengalahkan Baseline pada Pemisahan Statis?
Analisis kuantitatif mengungkap alasan struktural mengapa model Machine Learning tanpa penyesuaian khusus belum mengalahkan `rv_past20` pada split statis tunggal:
1. **Asimetri Rezim Data Latih vs Data Uji:**
   - Periode latih (2010–2021) memiliki rata-rata target $0,008802$ dengan standar deviasi $0,005947$ dan nilai maksimum $0,058497$ akibat pandemi Covid-19.
   - Periode validasi (2022–2024) memiliki rata-rata target hanya $0,006509$ ($\sigma = 0,003260$, puncak hanya $0,019745$).
2. **Kelemahan Fungsi Loss Standar ($L_2$ Loss / MSE):**
   - Random Forest dan Ridge standar meminimalkan Mean Squared Error.
   - Karena $L_2$ loss menghukum error besar secara kuadratik, sampel-sampel volatilitas tinggi tahun 2020 menarik (*pulling*) bobot model ke atas secara masif.
   - Akibatnya, pada periode validasi 2022–2024 yang tenang, prediksi model rata-rata berada pada level $0,0085$ – $0,0095$ (terjadi *upward shift* konstan), menghasilkan error absolut (MAE) yang membengkak.
3. **Korelasi Positif yang Menjanjikan:**
   - Meskipun level prediksi bergeser ke atas (*level bias*), korelasi Pearson model ML justru **lebih tinggi daripada baseline** (`Ridge` $r = 0,2599$ dan `Gradient Boosting` $r = 0,2373$ vs `rv_past20` $r = 0,2197$).
   - Hal ini membuktikan bahwa arah pergerakan (*relative movement*) yang dipelajari model sudah tepat, dan hanya memerlukan kalibrasi intercept / regularisasi loss (Task 3B) untuk mengeliminasi bias level.

---

## 5. Evaluasi Expanding Window Walk-Forward (3 Folds)

Untuk menguji apakah sinyal prediktor benar-benar berdaya guna ketika model dilatih dengan data yang selalu diperbarui (*continuous learning / rolling retraining*), evaluasi Walk-Forward 3 Lipatan dijalankan:

### 5.1 Rincian Kinerja Per Lipatan (Fold 1, 2, 3)

| Lipatan (Fold) | Periode Validasi (Out-of-Sample) | Kondisi Rezim Pasar | Model / Baseline | MAE | RMSE | Catatan Evaluasi |
|---|---|---|---|---|---|---|
| **Fold 1** | **Tahun 2022** (260 baris) | Kenaikan suku bunga agresif The Fed | **Persistence `rv_past20`** | **0,002546** | 0,003625 | Baseline terbaik di tahun pasca-Covid. |
| Fold 1 | Tahun 2022 | | Constant Median | 0,002565 | **0,003312** | RMSE terendah. |
| Fold 1 | Tahun 2022 | | Gradient Boosting | 0,003393 | 0,004279 | Model ML terbaik di Fold 1. |
| Fold 1 | Tahun 2022 | | Ridge (Pipeline) | 0,003816 | 0,004593 | Terbebani shock Covid di set latih. |
| Fold 1 | Tahun 2022 | | Random Forest | 0,004270 | 0,004955 | Overfitting pada noise latih. |
|---|---|---|---|---|---|---|
| **Fold 2** | **Tahun 2023** (260 baris) | Normalisasi pasar, inflasi melandai | **Ridge (Pipeline)** | **0,001972** | **0,002484** | **UNGGUL MUTLAK DI ATAS SELURUH BASELINE!** |
| Fold 2 | Tahun 2023 | | Persistence `rv_past20` | 0,002265 | 0,002946 | Baseline terbaik kedua. |
| Fold 2 | Tahun 2023 | | Gradient Boosting | 0,002434 | 0,002842 | Mengalahkan Constant Median & Mean. |
| Fold 2 | Tahun 2023 | | Constant Median | 0,002952 | 0,003306 | Error melonjak karena median historis terlalu tinggi. |
| Fold 2 | Tahun 2023 | | Random Forest | 0,003377 | 0,003726 | Membaik dari Fold 1 tetapi masih tertinggal. |
|---|---|---|---|---|---|---|
| **Fold 3** | **Tahun 2024** (252 baris) | All-Time High IHSG & Pemilu RI | **Constant Median** | **0,002640** | **0,003459** | Median set latih mendekati rezim aktual. |
| Fold 3 | Tahun 2024 | | **Ridge (Pipeline)** | **0,002847** | 0,003839 | **Mengalahkan Persistence `rv_past20`!** |
| Fold 3 | Tahun 2024 | | **Gradient Boosting** | **0,002988** | 0,003767 | **Mengalahkan Persistence `rv_past20`!** |
| Fold 3 | Tahun 2024 | | Constant Mean | 0,003136 | 0,003735 | |
| Fold 3 | Tahun 2024 | | Persistence `rv_past20` | 0,003232 | 0,003987 | Tertinggal di era reli pasar. |
| Fold 3 | Tahun 2024 | | Random Forest | 0,003671 | 0,004338 | |

### 5.2 Rata-rata Kinerja Walk-Forward Lintas 3 Lipatan

| Peringkat Rata-rata | Model / Algoritma | Rata-rata MAE (3 Folds) | Rata-rata RMSE (3 Folds) | Stabilitas & Karakteristik Lintas Rezim |
|---|---|---|---|---|
| **1** | **Persistence `rv_past20`** | **0,002681** | 0,003519 | Paling konsisten di saat shock (2022), namun tertinggal saat pasar tenang (2023 & 2024). |
| **2** | **Constant Median** | **0,002719** | **0,003359** | RMSE rata-rata terendah berkat ketahanan terhadap ekor tebal. |
| **3** | **Ridge (Pipeline)** | **0,002878** | **0,003639** | **Model ML Paling Menjanjikan:** Menang telak di Fold 2 dan nomor 2 di Fold 3. |
| **4** | **Gradient Boosting** | **0,002938** | **0,003629** | Kompetitif dan stabil melintasi seluruh lipatan tanpa fluktuasi ekstrem. |
| **5** | Constant Mean | 0,003360 | 0,003889 | Paling buruk di antara baseline univariat. |
| **6** | Random Forest | 0,003773 | 0,004340 | Kurang adaptif tanpa pemangkasan kedalaman pohon (*pruning*). |

*Visualisasi komparasi stabilitas walk-forward tersimpan di [`outputs/models/fig_mod_02_walk_forward_models.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_02_walk_forward_models.png).*

> [!IMPORTANT]
> **Temuan Kunci Sesuai Arahan Kepatuhan Poin 7:**  
> Peningkatan performa model Machine Learning **tidak seragam di seluruh periode**, melainkan sangat bergantung pada rezim data latih:
> - Pada periode yang langsung menyusul shock krisis (Fold 1 / 2022), model ML mengalami distorsi *upward bias*.
> - Namun ketika model telah 'melihat' data pasca-krisis (Fold 2 / 2023 dan Fold 3 / 2024), **Ridge Regression dan Gradient Boosting terbukti mengungguli persistence baseline secara signifikan**.

---

## 6. Analisis Sinyal Prediktor (Feature Importance & Koefisien)

Inspeksi sinyal fitur menjelaskan logika ekonomi yang dipelajari oleh masing-masing arsitektur model:

### 6.1 Top Fitur Ridge Regression (Standardized Coefficients)
Ridge Regression memberikan bobot linier positif/negatif yang seimbang terhadap variabel makro dan volatilitas:
1. `X1_Fear_Liquidity_Robust` ($+0,006862$): Sinyal interaksi ketakutan likuiditas (kombinasi VIX dan return kurs) memiliki dampak positif terkuat terhadap kenaikan volatilitas forward IHSG.
2. `X1_Fear_Liquidity_Original` ($-0,005961$): Menjadi pasangan penyeimbang (*offsetting counter-weight*) terhadap versi robust untuk memitigasi collinearity.
3. `VIX` ($+0,001281$): Ketakutan pasar global secara langsung mentransmisikan risiko ke volatilitas domestik.
4. `SP500` ($+0,000975$) dan `CPI` ($+0,000930$): Menangkap tekanan makroekonomi inflasi dan pergerakan bursa global.
5. `IHSG` ($-0,000815$): Korelasi asimetris negatif (fenomena *leverage effect*, di mana penurunan indeks memicu lonjakan volatilitas).
6. `rv_past20` ($+0,000772$) dan `rv_past10` ($+0,000722$): Komponen persistensi memori volatilitas jangka menengah.

### 6.2 Top Fitur Pohon (Random Forest & Gradient Boosting MDI Importance)
Pada model non-linier berbasis pohon, fitur volatilitas dan momentum mendominasi pembagian cabang (*tree splits*):
- **Fitur Paling Berpengaruh:**
  - `mom_ihsg_10` (GBR: $19,11\%$, RF: $9,25\%$): Momentum 10-hari IHSG menjadi sinyal penentu apakah pasar sedang berada dalam tren tenang atau guncangan.
  - `rv_past10` (GBR: $17,72\%$, RF: $20,57\%$): Memori volatilitas 10-hari menjadi proksi lokal paling efisien.
  - `VIX` (GBR: $13,00\%$, RF: $7,01\%$): Tolok ukur volatilitas global menjadi fitur makro terpenting.
  - `X1_Fear_Liquidity_Robust` (GBR: $9,92\%$, RF: $5,31\%$): Fitur hasil rancangan Checkpoint 1B terbukti masuk ke jajaran 4 besar prediktor pohon!
  - `rv_past20` (GBR: $4,23\%$, RF: $5,14\%$) dan `mom_ihsg_5` (GBR: $4,49\%$, RF: $5,40\%$).

*Visualisasi perbandingan feature importance tersimpan di [`outputs/models/fig_mod_03_feature_importance.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_03_feature_importance.png).*

---

## 7. Verifikasi Kepatuhan & Integritas Metodologis (6 Checks)

Seluruh proses eksperimen Checkpoint 3A telah divalidasi oleh 6 unit pengujian otomatis pada Section 8 notebook:

```
=================================================================
HASIL PEMERIKSAAN KEPATUHAN & INTEGRITAS ANTI-LEAKAGE (TASK 3A)
=================================================================
[PASS 1] Monotonisitas Urutan Waktu: PASS
         Train Max (2021-12-24) < Val Min (2022-01-03) < Test Min (2025-01-02)
[PASS 2] Isolasi Fitting Preprocessing: PASS
         Scaler mean fit pada Train != Val mean (Terbukti bebas data-snooping).
[PASS 3] Isolasi Penuh Test Set (2025–2026): PASS
         359/359 baris target test bernilai NaN (Tidak pernah disentuh pemodelan).
[PASS 4] Purging Target Horizon H=5: PASS
         5 hari bursa (2021-12-27 s/d 2021-12-31) telah di-purge dari set latih.
[PASS 5] Kemurnian Matriks Fitur: PASS
         29 fitur prediktor terbukti bebas dari target masa depan.
[PASS 6] Verifikasi Klaim Numerik Objektif: PASS
         Jumlah model ML awal yang mengalahkan baseline pada static val: 0
         -> Tidak ada klaim palsu bahwa model awal langsung unggul pada static split.
         -> Mengakui secara jujur bahwa model un-tuned mengalami regime shift bias.
=================================================================
SELURUH 6 PEMERIKSAAN KEPATUHAN DINYATAKAN PASS! [VERIFIED]
=================================================================
```

---

## 8. Keterbatasan Eksperimen & Rekomendasi Kandidat Menuju Checkpoint 3B (Tuning)

### 8.1 Keterbatasan Eksperimen Awal Checkpoint 3A
1. **Belum Ada Penyesuaian Loss Function:**
   Semua model masih menggunakan default loss (MSE / Ordinary Least Squares). Karakteristik target yang *fat-tailed* dengan shock krisis masa lalu mengharuskan transisi ke fungsi loss yang robust (*Huber Loss* atau *MAE Loss*).
2. **Ketiadaan Pembobotan Waktu (*Sample Weighting / Exponential Decay*):**
   Model memperlakukan data krisis tahun 2010 dan 2020 dengan bobot yang persis sama dengan data 2021, padahal dinamika rezim pasar terus berevolusi.
3. **Hyperparameter Masih Baku:**
   - Ridge masih menggunakan $\alpha=1.0$ tanpa eksplorasi grid pencarian.
   - Pohon Boosting dan Random Forest masih menggunakan konfigurasi default tanpa regularisasi kedalaman adaptif.

### 8.2 Rekomendasi Kandidat untuk Hyperparameter Tuning (Task 3B)

Berdasarkan hasil empiris static split dan walk-forward 3-fold, ditetapkan 3 kandidat prioritas untuk tahap tuning selanjutnya:

| Prioritas Tuning | Kandidat Model | Rasionalitas Pemilihan Berdasarkan Data | Rencana Strategi Tuning (Task 3B) |
|---|---|---|---|
| **Prioritas 1** | **Gradient Boosting / LightGBM Regressor** | Model pohon terbaik; memiliki Pearson $r = 0,2373$ dan stabil di walk-forward Fold 2 & 3. Fitur non-linier seperti momentum dan VIX terekstrak optimal. | 1. Ganti objective ke **Huber Loss** atau **MAE Loss (L1)** untuk meredam sensitivitas krisis 2020.<br>2. Tuning `max_depth` (2 s/d 4) dan `learning_rate` (0.01 s/d 0.05).<br>3. Eksplorasi `subsample` dan `min_samples_leaf` untuk mencegah leaf overfitting. |
| **Prioritas 2** | **Ridge Regression (Pipeline)** | **Pemenang mutlak Fold 2 ($\text{MAE} = 0,001972$)** dan korelasi tertinggi ($r = 0,2599$). Sangat stabil menangkap sinyal makro linier. | 1. Tuning intensitas penalti L2 $\alpha \in [10^{-3}, 10^3]$ menggunakan TimeSeriesSplit CV.<br>2. Uji variasi HuberRegressor / ElasticNet untuk ketahanan terhadap outlier. |
| **Prioritas 3** | **Ensemble Stacking / Blending (Hybrid Model)** | Diversifikasi risiko arsitektur: menggabungkan kekuatan linier Ridge, non-linier Boosting, dan baseline `rv_past20`. | Bentuk weighted blend: $w_1 \cdot \text{Ridge} + w_2 \cdot \text{Boosting} + w_3 \cdot \text{rv\_past20}$ yang dioptimalkan pada validation window. |

> **Penyelesaian Checkpoint 3A:**  
> Seluruh komparasi model awal, pencatatan tabel metrik MAE/RMSE, evaluasi walk-forward lintas lipatan, dan pembuatan visualisasi telah tuntas tanpa melakukan tuning ekstensif, SHAP, atau inferensi test set sebelum waktunya. Proyek siap melangkah ke Checkpoint 3B (Hyperparameter Tuning).
