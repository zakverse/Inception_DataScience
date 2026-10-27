# Laporan Audit Kepatuhan Studi Kasus (Compliance Audit) — Checkpoint 6

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 6 (Studi Kasus Compliance & Artifact Verification Audit)  
**Dokumen Acuan Utama:** `Aset Lomba/Studi Kasus.docx`, `Aset Lomba/DATA DICTIONARY dari DATASET Indonesia Financial Time Series Dataset 2010-2026.docx`  
**Ruang Lingkup Audit:** Verifikasi keterpenuhan butir-butir Task 1, Task 2, dan Task 3 pada artefak riil proyek (Notebooks 01–08, Skrip, Outputs, dan Dokumen Checkpoint).  
**Kaidah Evaluasi:** Keterpenuhan dinilai berdasarkan **bukti nyata kode dan artefak**, bukan sekadar klaim naratif dalam laporan.  

---

## 1. Matriks Kepatuhan Menyeluruh (*Overall Compliance Matrix*)

Status klasifikasi kepatuhan:
- **`COMPLETE`**: Persyaratan telah dipenuhi secara penuh dengan bukti kode, grafik, tabel, dan dokumen pendukung yang terverifikasi.
- **`PARTIAL`**: Persyaratan telah dikerjakan secara substansi, namun belum disajikan dalam struktur atau bab khusus yang diminta secara eksplisit oleh Studi Kasus.
- **`MISSING`**: Persyaratan belum dikerjakan sama sekali pada artefak proyek.
- **`NEEDS_VERIFICATION`**: Persyaratan bergantung pada informasi eksternal yang belum tersedia di repositori (misalnya portal lomba).

### Tabel Kepatuhan Task 1, Task 2, & Task 3

| ID Butir | Rincian Persyaratan Studi Kasus | Status Kepatuhan | Artefak Pembuktian Utama | Bagian / Sel Rujukan |
|---|---|---|---|---|
| **TASK 1.1** | Minimal tiga fitur turunan baru ($X_1, X_2, X_3$) | **`COMPLETE`** | `notebook/EDA.ipynb`, `scripts/feature_engineering.py` | EDA Cell 14; FE lines 135–175 |
| **TASK 1.2** | Rumus dan rasionalitas bisnis/finansial setiap fitur | **`COMPLETE`** | `docs/checkpoint_1b_feature_design.md`, `notebook/EDA.ipynb` | CP 1B Section 2; EDA Cell 14 |
| **TASK 1.3** | Hipotesis ekonomi dampak fitur terhadap volatilitas $Y$ | **`COMPLETE`** | `docs/checkpoint_1b_feature_design.md`, `docs/EDA_analysis_report.md` | CP 1B Section 2.1–2.3; EDA Report Sec 5 |
| **TASK 1.4** | Visualisasi kuantitatif korelasi/kontribusi fitur ke $Y$ | **`COMPLETE`** | `outputs/eda/`, `outputs/models/`, `outputs/xai/` | `fig_07`, `fig_10`, `fig_11`, `fig_mod_03`, `fig_xai_01` |
| **TASK 1.5** | Interpretasi hasil tanpa klaim kausalitas palsu | **`COMPLETE`** | `notebook/EDA.ipynb`, `docs/checkpoint_4_xai.md` | EDA Cell 14; CP 4 Section 1.3 |
|---|---|---|---|---|
| **TASK 2.1** | Pemisahan time-series urut waktu (Dilarang random split) | **`COMPLETE`** | `notebook/02_Validation_Baseline.ipynb`, `outputs/validation/` | NB 02 Section 4; `fig_val_01_timeline_split.png` |
| **TASK 2.2** | Penjelasan periode training, validasi, dan testing | **`COMPLETE`** | `docs/checkpoint_2_validation_baseline.md`, `docs/checkpoint_5_final_submission.md` | CP 2 Section 3; CP 5 Section 3 |
| **TASK 2.3** | Bukti scaler/preprocessing di-fit HANYA pada data training | **`COMPLETE`** | `notebook/03`, `04`, `05`, `07`, `08` (Pipeline StandardScaler) | NB 08 Section 4, Cell 4; NB 04 Cell 5 |
| **TASK 2.4** | Bukti fitur tidak menggunakan informasi masa depan ($t+1$) | **`COMPLETE`** | `scripts/feature_engineering.py` (`test_5_anti_leakage_invariance`) | FE lines 240–285; NB 08 Section 2 |
| **TASK 2.5** | Penanganan overlap target 5-hari & warm-up fitur | **`COMPLETE`** | `notebook/02_Validation_Baseline.ipynb`, `docs/checkpoint_1a_verification.md` | NB 02 Section 4 (Purging $H=5$); Dropna warm-up |
| **TASK 2.6** | Pengakuan periode tuning bukan holdout independen | **`COMPLETE`** | `docs/checkpoint_3c1_reconciliation.md`, `docs/checkpoint_5_final_submission.md` | CP 3C.1 Audit 2 (Pseudo-Holdout 2024); CP 5 Sec 1 & 8 |
| **TASK 2.7** | Pemisahan test 2025–2026 dari proses seleksi model | **`COMPLETE`** | `notebook/02` s/d `07` (Isolasi 359 baris test berstatus NaN) | Seluruh notebook validasi; NB 08 Section 4 |
|---|---|---|---|---|
| **TASK 3.1** | Pemilihan 1 jenis model utama beserta alasan teknis | **`COMPLETE`** | `notebook/04_Model_Tuning.ipynb`, `docs/checkpoint_3b_tuning.md` | NB 04 Section 7; CP 3B Section 1 & 5 |
| **TASK 3.2** | Hyperparameter tuning menggunakan data train & validasi | **`COMPLETE`** | `notebook/04_Model_Tuning.ipynb`, `outputs/tuning/` | NB 04 Section 5 & 6; `fig_tune_01_grid_search_curves.png` |
| **TASK 3.3** | Benchmark: Bukti error ML lebih kecil dari model baseline | **`COMPLETE`** | `notebook/02`, `03`, `04`, `05`, `outputs/validation/`, `outputs/models/` | NB 02 Sec 5; NB 04 Sec 6; `fig_mod_01_baseline_vs_models.png` |
| **TASK 3.4** | Global explanation menggunakan SHAP Summary Plot | **`COMPLETE`** | `notebook/07_Model_Interpretation_XAI.ipynb`, `outputs/xai/` | NB 07 Section 5; `fig_xai_02_shap_summary_beeswarm.png` |
| **TASK 3.5** | Local explanation tanggal volatilitas tinggi & bahasa bisnis | **`COMPLETE`** | `notebook/07_Model_Interpretation_XAI.ipynb`, `outputs/xai/` | NB 07 Section 6 & 7; `fig_xai_03_local_explanations.png` |
| **TASK 3.6** | Identifikasi kondisi pasar di mana model meleset jauh | **`PARTIAL`** | `docs/checkpoint_3c_robustness_audit.md`, `scratch/inspect_error_cases.py` | CP 3C Sec 3.1; Teridentifikasi pada rezim ekstrem 5% |
| **TASK 3.7** | Analisis kesalahan berbasis XAI (Bukan dugaan semata) | **`PARTIAL`** | `docs/checkpoint_4_xai.md` (Rezim 11 Mei 2022) | CP 4 Section 5; Belum ada bab terdedikasi "Error Analysis XAI" |
|---|---|---|---|---|
| **SUBMISSION** | Format berkas submission terverifikasi terhadap portal | **`NEEDS_VERIFICATION`** | `outputs/submission/`, `docs/checkpoint_51_submission_integrity.md` | 2 format tersedia (359 baris & 4.266 baris); portal belum dicek |

---

## 2. Bukti Artefak Riil untuk Setiap Persyaratan

### 2.1 TASK 1: Rekayasa Fitur & Analisis Eksplorasi Data (EDA)

#### 1. Inovasi & Formulasi Fitur Turunan ($X_1, X_2, X_3$) — `COMPLETE`
- **Persyaratan:** Buat minimal 3 fitur turunan baru berbasis analisis keuangan, statistik, atau makroekonomi untuk memprediksi realized volatility 5-hari forward ($Y$).
- **Bukti Kode:**
  1. `$X_1$ (Fear Liquidity Composite):`
     - Formulasi Awal: `df_feat['X1_Fear_Liquidity'] = df_feat['VIX'] * np.log(df_feat['USDIDR'] / usdidr_ma20)` ([`notebook/EDA.ipynb:L1310`](file:///z:/Projects/Inception/notebook/EDA.ipynb#L1310)).
     - Formulasi Robust: `df_feat['X1_Fear_Liquidity_Robust'] = df_feat['VIX'] * ((df_feat['USDIDR'] - usdidr_ma20) / usdidr_ma20)` ([`scripts/feature_engineering.py:L145`](file:///z:/Projects/Inception/scripts/feature_engineering.py#L145)).
  2. `$X_2$ (Rate Differential Pressure):`
     - Formulasi Awal: `(BI_rate - US_rate) * pct_change(USDIDR, 5)` ([`notebook/EDA.ipynb:L1314`](file:///z:/Projects/Inception/notebook/EDA.ipynb#L1314)).
     - Formulasi Absolut Robust: `df_feat['X2_Rate_Diff_Pressure_Abs'] = np.abs(df_feat['rate_differential']) * np.abs(df_feat['usdidr_ret5'])` ([`scripts/feature_engineering.py:L157`](file:///z:/Projects/Inception/scripts/feature_engineering.py#L157)).
  3. `$X_3$ (Commodity Macro Shock):`
     - Formulasi Awal: `oil_ret5 * gold_ret5 * sp500_ret5` ([`notebook/EDA.ipynb:L1318-1322`](file:///z:/Projects/Inception/notebook/EDA.ipynb#L1318-L1322)).
     - Formulasi L2-Norm Robust: `df_feat['X3_Commodity_Shock_L2Norm'] = np.sqrt(oil_ret5**2 + gold_ret5**2 + sp500_ret5**2)` ([`scripts/feature_engineering.py:L172`](file:///z:/Projects/Inception/scripts/feature_engineering.py#L172)).
- **Dokumentasi Lengkap:** [`docs/checkpoint_1b_feature_design.md`](file:///z:/Projects/Inception/docs/checkpoint_1b_feature_design.md) (Bagian 2).

#### 2. Rasionalitas Bisnis & Hipotesis Ekonomi — `COMPLETE`
- **Persyaratan:** Jelaskan ide penggabungan variabel dan hipotesis transmisi ekonominya ke volatilitas IHSG.
- **Bukti Rujukan:** [`docs/checkpoint_1b_feature_design.md`](file:///z:/Projects/Inception/docs/checkpoint_1b_feature_design.md) (Tabel Bagian 2.1 & 2.2).
  - **$X_1$:** Mengawinkan indeks kepanikan ekuitas global (VIX) dengan sinyal pelarian modal valas domestik (depresiasi kurs rupiah terhadap tren 20 hari). Hipotesis: Guncangan ganda kepanikan global dan depresiasi rupiah memicu *capital flight* investor asing yang melipatgandakan volatilitas IHSG.
  - **$X_2$:** Mengawinkan selisih suku bunga kebijakan moneter (BI Policy Rate minus Fed Funds Rate) dengan momentum kurs 5-hari. Hipotesis: Penyempitan *interest rate differential* memicu penutupan posisi *carry trade*, menekan likuiditas rupiah dan mengguncang bursa saham.
  - **$X_3$:** Mengintegrasikan guncangan komoditas strategis (minyak WTI dan emas dunia) bersama ekuitas AS (S&P 500). Hipotesis: Guncangan serentak pada pasar energi, komoditas lindung nilai (*safe haven*), dan pasar modal Wall Street mencerminkan pergeseran rezim makro global yang merambat cepat ke pasar berkembang.

#### 3. Uji Validitas Kuantitatif (EDA) — `COMPLETE`
- **Persyaratan:** Tampilkan grafik (heatmap korelasi, plot tren, scatter plot, atau feature importance) yang membuktikan signifikansi kontribusi fitur terhadap $Y$.
- **Bukti Artefak Grafis:**
  - `outputs/eda/fig_06_correlation_heatmap.png`: Heatmap korelasi matriks multivariat.
  - `outputs/eda/fig_07_feature_target_correlation.png`: Bar plot ranking korelasi prediktor terhadap `Target_Volatilitas_Y`.
  - `outputs/eda/fig_10_candidate_features_scatter.png`: Scatter plot sebaran $X_1, X_2, X_3$ terhadap target $Y$.
  - `outputs/eda/fig_11_candidate_features_timeseries.png`: Plot deret waktu ko-pergerakan kandidat fitur terhadap lonjakan volatilitas pasar.
  - `outputs/models/fig_mod_03_feature_importance.png`: Pembuktian bahwa $X_{1,\text{robust}}$ menduduki posisi top-4 prediktor pohon di Checkpoint 3A (bobot MDI $9,92\%$).
  - `outputs/xai/fig_xai_01_global_importance.png`: Pembuktian atribusi $X_1$ dan $X_2$ pada model ter-tuning di Checkpoint 4.

#### 4. Integritas Interpretasi Tanpa Klaim Kausalitas Palsu — `COMPLETE`
- **Persyaratan:** Membedakan kontribusi statistik terhadap fungsi estimasi dari klaim sebab-akibat ekonomis langsung.
- **Bukti Rujukan:**
  - [`notebook/EDA.ipynb:L1293-1294`](file:///z:/Projects/Inception/notebook/EDA.ipynb#L1293-L1294): *"Korelasi ini bersifat linear dan belum mengontrol collinearity atau overfitting. Klaim paling berpengaruh belum dibuat sampai ada bukti dari model akhir."*
  - [`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md) (Bagian 1.3): Peringatan tegas anti-causal claim bahwa nilai SHAP dan koefisien regresi adalah ukuran atribusi marjinal model terhadap variansi target, bukan hubungan mekanis kausal di dunia riil.

---

### 2.2 TASK 2: Pemisahan Data Time-Series & Anti-Leakage Pipeline

#### 1. Pemisahan Waktu Kronologis (Bebas Random Split) — `COMPLETE`
- **Persyaratan:** Dilarang keras mengacak data (`train_test_split(shuffle=True)`). Data harus dipotong urut waktu.
- **Bukti Kode:**
  - Skema expanding walk-forward temporal cross-validation 3-lipatan diterapkan konsisten:
    - Fold 1: Train 2010–2021 | Validasi 2022 ($N=247$ hari)
    - Fold 2: Train 2010–2022 | Validasi 2023 ($N=246$ hari)
    - Fold 3: Train 2010–2023 | Validasi 2024 ($N=279$ hari)
  - Visualisasi timeline: [`outputs/validation/fig_val_01_timeline_split.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_01_timeline_split.png).
  - Notebook implementasi: [`notebook/02_Validation_Baseline.ipynb:L196-208`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb#L196-L208).

#### 2. Disiplin Kebersihan Data (Anti-Leakage Preprocessing) — `COMPLETE`
- **Persyaratan:** Seluruh proses normalisasi/standarisasi/imputasi hanya boleh di-fit pada Data Training, lalu diterapkan (transform) ke Data Validasi dan Data Uji.
- **Bukti Kode:**
  - Pada seluruh permodelan linier (`Ridge` dan `Huber`), proses penskalaan dibungkus dalam scikit-learn Pipeline:  
    `Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(...))])`
  - Pemanggilan `.fit(X_train, y_train)` selalu dilakukan secara eksklusif pada partisi training tiap fold. Partisi validasi dan testing hanya menerima panggilan `.predict(X_val)` yang secara otomatis mengeksekusi `.transform()`.
  - Rujukan: [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb), [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb), [`notebook/08_Final_Training_Submission.ipynb`](file:///z:/Projects/Inception/notebook/08_Final_Training_Submission.ipynb).

#### 3. Bukti Kuantitatif Anti-Leakage (Zero Future Information at EOD $t$) — `COMPLETE`
- **Persyaratan:** Tunjukkan bukti pada kode bahwa fitur $X$ pada hari $t$ tidak menyenggol informasi dari hari $t+1$.
- **Bukti Kode:**
  - Unit test terotomasi `test_5_anti_leakage_invariance` pada [`scripts/feature_engineering.py:L240-285`](file:///z:/Projects/Inception/scripts/feature_engineering.py#L240-L285).
  - Metodologi: Baris $t=1.000$ direkam nilainya, kemudian data baris masa depan $t+1$ s/d $t+5$ dimutasi secara agresif (diberi lonjakan nilai $+1.000\%$). Fitur baris $t$ dihitung ulang pada data termutasi.
  - Hasil Pembuktian: Deviasi fitur $X_t$ termutasi vs asli adalah tepat **$0,000000000000$ (Zero Difference)**. Lolos uji pada seluruh eksekusi pipeline.

#### 4. Penanganan Overlap Target 5-Hari & Warm-Up Historis — `COMPLETE`
- **Persyaratan:** Mencegah label training tumpang-tindih (*lookahead label overlap*) dengan periode evaluasi, serta menangani baris awal deret waktu.
- **Bukti Kode:**
  - **Mekanisme Purging $H=5$:** Pada setiap lipatan training yang berakhir di tanggal $T$, tepat 5 hari perdagangan terakhir di-purge (`train_purged = train_unpurged.iloc[:-5]`) ([`notebook/02_Validation_Baseline.ipynb:L199-202`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb#L199-L202)).
  - **Warm-Up Window Handling:** 20 hari perdagangan pertama (Januari 2010) dieliminasi menggunakan `dropna(subset=feature_cols)` untuk memastikan seluruh model ML menerima input matriks yang lengkap dan seragam ($N=3.887$ hari berlabel).

#### 5. Audit Bias Seleksi & Isolasi Data Uji 2025–2026 — `COMPLETE`
- **Persyaratan:** Menjelaskan bahwa data evaluasi bukan holdout independen mutlak jika telah dipakai dalam tuning, serta mengisolasi data uji 2025–2026.
- **Bukti Rujukan:**
  - Status tahun 2024 formally dideklarasikan sebagai **Pseudo-Holdout / Re-purposed Evaluation Window** pada [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (Bagian 2) karena data 2024 memengaruhi pemilihan parameter `learning_rate=0.03`.
  - Data uji 359 baris (2025–2026) diisolasi 100% dengan target `NaN` dan baru disentuh pada Checkpoint 5.

---

### 2.3 TASK 3: Pemodelan Regresi, Evaluasi, & Explainable AI (XAI)

#### 1. Pemilihan 1 Model Terbaik Versi Tim & Rasionalitasnya — `COMPLETE`
- **Persyaratan:** Pilih 1 jenis algoritma regresi utama (contoh: XGBoost, LightGBM, CatBoost, Random Forest, GARCH, GBR) dan jelaskan alasan pemilihannya.
- **Bukti Keputusan:**
  - **Model Tunggal Utama:** `GBR Tuned (Gradient Boosting Regressor dengan loss='absolute_error', lr=0.03, max_depth=2, n_estimators=100)`.
  - **Alasan Pemilihan:**
    1. Fungsi kerugian $L_1$ absolute error secara langsung mengoptimalkan metrik MAE kompetisi dan kebal (*robust*) terhadap outlier lonjakan varians krisis 2020.
    2. Struktur pohon dangkal (`max_depth=2`) bertindak sebagai regularisasi struktural yang membatasi kapasitas memori dan meredam overfitting pada rezim volatilitas tinggi.
    3. Konsisten mengalahkan baseline naif kompetisi di seluruh lipatan waktu.
  - **Model Ensemble Pendamping:** `Blend 60:40 (GBR Tuned : Ridge Tuned)` sebagai penggabungan komplementer non-linier dan linier makro.
  - Rujukan: [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb), [`docs/checkpoint_3b_tuning.md`](file:///z:/Projects/Inception/docs/checkpoint_3b_tuning.md), [`docs/checkpoint_5_final_submission.md`](file:///z:/Projects/Inception/docs/checkpoint_5_final_submission.md).

#### 2. Hyperparameter Tuning pada Data Latih & Validasi — `COMPLETE`
- **Persyaratan:** Cari kombinasi parameter terbaik hanya menggunakan data latih dan validasi Task 2.
- **Bukti Kode & Grafis:**
  - Grid search terstruktur pada `notebook/04_Model_Tuning.ipynb`:
    - GBR: grid search `learning_rate` [0.01, 0.02, 0.03, 0.05, 0.10], `max_depth` [2, 3, 4], `loss` ['absolute_error', 'squared_error', 'huber'].
    - Ridge: log-grid `alpha` [$10^{-3}, 10^{-2}, 10^{-1}, 1, 10, 100, 1000$].
  - Kurva validasi grafis: [`outputs/tuning/fig_tune_01_grid_search_curves.png`](file:///z:/Projects/Inception/outputs/tuning/fig_tune_01_grid_search_curves.png).

#### 3. Benchmark Evaluasi Akurasi (RMSE / MAE) vs Baseline — `COMPLETE`
- **Persyaratan:** Tampilkan skor RMSE/MAE pada data validasi dan buktikan model ML memiliki error lebih kecil dari baseline naif (rata-rata volatilitas 5 hari lalu).
- **Bukti Numerik:**
  - **Baseline Naif Resmi (`rv_past5`):** Pooled MAE = **$0,002981$** | Pooled RMSE = **$0,004088$** (terverifikasi pada 772 hari validasi di `notebook/02_Validation_Baseline.ipynb` Cell 10).
  - **Baseline Persistensi Kuat (`rv_past20`):** Pooled MAE = **$0,002675$** | Pooled RMSE = **$0,003540$**.
  - **GBR Tuned:** Pooled MAE = **$0,002462$** (Unggul $+17,4\%$ vs `rv_past5`; $+8,0\%$ vs `rv_past20`).
  - **Blend 60:40:** Pooled MAE = **$0,002401$** (Unggul $+19,5\%$ vs `rv_past5`; $+10,2\%$ vs `rv_past20`).
  - Grafis pembuktian: [`outputs/models/fig_mod_01_baseline_vs_models.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_01_baseline_vs_models.png), [`outputs/tuning/fig_tune_02_fold_and_pooled_comparison.png`](file:///z:/Projects/Inception/outputs/tuning/fig_tune_02_fold_and_pooled_comparison.png).

#### 4. Transparansi Model: Penjelasan Global (Global Explanation) — `COMPLETE`
- **Persyaratan:** Wajib menggunakan library XAI (seperti SHAP atau LIME) dan tampilkan SHAP Summary Plot yang menunjukkan fitur berbobot paling besar.
- **Bukti Artefak:**
  - Library yang digunakan: `shap==0.54.1` (`shap.TreeExplainer`).
  - Summary Beeswarm Plot: [`outputs/xai/fig_xai_02_shap_summary_beeswarm.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_02_shap_summary_beeswarm.png).
  - Global Feature Importance Bar Chart: [`outputs/xai/fig_xai_01_global_importance.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_01_global_importance.png).
  - Temuan Utama: Fitur volatilitas lokal (`rv_past20`) menduduki peringkat teratas (mean |SHAP| $0,000466$), diikuti momentum penjualan IHSG (`mom_ihsg_10`, $0,000294$), suku bunga The Fed (`US_rate`, $0,000231$), dan indeks ketakutan global (`VIX`, $0,000188$).

#### 5. Transparansi Model: Penjelasan Lokal (Local Explanation) — `COMPLETE`
- **Persyaratan:** Pilih tanggal spesifik di mana model memprediksi volatilitas sangat tinggi/berbahaya, tampilkan visualisasi lokal (waterfall/force/bar plot), dan terjemahkan ke dalam bahasa bisnis.
- **Bukti Rujukan:**
  - Kasus Puncak Volatilitas: **11 Mei 2022** (Pasca libur panjang Idul Fitri & kenaikan agresif suku bunga The Fed 50 bps). Target aktual melonjak ekstrem ke $Y=0,019739$.
  - Prediksi Model: Baseline $0,007949 \to$ Prediksi melonjak ke $0,012739$ (Blend 60:40) dan $0,012095$ (GBR).
  - Pendorong Naik (Bahasa Bisnis):
    1. `VIX` (+0,001599): Kepanikan Wall Street melonjak ke $32,56$, mentransmisikan premi risiko global.
    2. `mom_ihsg_5` (+0,001228): Kejatuhan tajam IHSG $-8,7\%$ dalam 1 pekan memicu efek *leverage* asimetris.
    3. `mom_ihsg_10` (+0,001071): Pelemahan tren 2 pekan mempertegas kepanikan likuiditas.
  - Visualisasi Grafis: [`outputs/xai/fig_xai_03_local_explanations.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_03_local_explanations.png).
  - Dokumen: [`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md) (Bagian 5, Rezim 1).

#### 6. Identifikasi Kondisi Pasar di Mana Model Meleset Jauh — `PARTIAL`
- **Persyaratan:** Identifikasi kondisi pasar di mana model sempat meleset jauh dari kenyataan pada data berlabel.
- **Kondisi Aktual Artefak:**
  - Pada [`docs/checkpoint_3c_robustness_audit.md`](file:///z:/Projects/Inception/docs/checkpoint_3c_robustness_audit.md) (Bagian 3.1 & 3.2), analisis kuantitatif residual $e_t = y_t - \hat{y}_t$ telah dilakukan melintasi 772 hari validasi, termasuk pembagian 95% rezim normal vs 5% rezim ekstrem.
  - Skrip audit [`scratch/inspect_error_cases.py`](file:///C:/Users/dzaki/.gemini/antigravity-ide/brain/f516e878-5249-4f41-8527-a0a51a75f83d/scratch/inspect_error_cases.py) mengidentifikasi bahwa error terbesar terjadi pada:
    1. *Underprediction Ekstrem (Pasar Jauh Lebih Bergejolak dari Prediksi):* Periode **31 Juli – 2 Agustus 2024** (tepat sebelum guncangan global *Black Monday* 5 Agustus 2024), di mana target aktual melonjak ke $0,01925$ sementara prediksi model berada di $0,00583$ (residual $+0,01343$).
    2. *Overprediction Ekstrem (Model Menduga Sangat Bergejolak, tetapi Pasar Cepat Tenang):* Tanggal **5 Agustus 2024**, di mana VIX melonjak ke $38,57$ dan model memprediksi volatilitas tinggi $0,01231$, namun 5 hari ke depan pasar pulih cepat (*swift mean-reversion*) sehingga volatilitas riil hanya $0,00550$ (residual $-0,00681$).
  - **Alasan Status `PARTIAL`:** Identifikasi tanggal-tanggal spesifik ini telah dieksekusi secara empiris, namun belum dituangkan ke dalam bab formal bertajuk *"Analisis Kesalahan (Error Analysis)"* di dalam laporan atau notebook presentasi akhir.

#### 7. Analisis Kesalahan Berbasis XAI (Bukan Dugaan Semata) — `PARTIAL`
- **Persyaratan:** Bedah alasan mengapa model meleset menggunakan dekomposisi fitur XAI, bukan sekadar tebakan naratif.
- **Kondisi Aktual Artefak:**
  - Pada kasus 11 Mei 2022 ([`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md)), dekomposisi SHAP membuktikan bahwa fitur penahan (pushing down) adalah level absolut `IHSG` ($-0,000283$) dan selisih suku bunga yang belum melebar ekstrem.
  - Namun, analisis dekomposisi XAI formal untuk kasus *Black Monday* Agustus 2024 (mengapa model terlambat mengantisipasi guncangan 31 Juli 2024 karena VIX sebelum kejadian masih rendah $16,36$, dan mengapa model meng-overestimate pada 5 Agustus 2024 karena VIX $38,57$ mendominasi fitur) baru tersimpan dalam skrip dan belum dijadikan satu sub-bab utuh di `notebook/07` atau laporan XAI.
  - **Alasan Status `PARTIAL`:** Bukti teknis XAI tersedia, namun integrasi penyajiannya ke dalam dokumen laporan masih perlu diformalkan.

---

### 2.4 Berkas Submission & Verifikasi Format Portal

#### Format Berkas Submission — `NEEDS_VERIFICATION`
- **Persyaratan:** Berkas submission sesuai aturan dan format resmi kompetisi.
- **Kondisi Aktual Artefak:**
  - Tiga berkas submission 2-kolom (`outputs/submission/submission_*.csv`) telah tervalidasi 100% (tepat 359 baris, rentang `2025-01-02` s/d `2026-05-22`, zero NaN, zero inf, non-negatif).
  - Dua berkas dataset lengkap terisi (`outputs/submission/dataset_peserta_filled_*.csv`) telah tervalidasi 100% (4.266 baris, seluruh target historis identik, 359 target NaN terisi).
  - Laporan audit integritas telah selesai: [`docs/checkpoint_51_submission_integrity.md`](file:///z:/Projects/Inception/docs/checkpoint_51_submission_integrity.md).
  - **Alasan Status `NEEDS_VERIFICATION`:** Pihak panitia tidak menyediakan `sample_submission.csv` di dalam folder aset lomba. Oleh karena itu, kesesuaian format terhadap form unggah portal resmi **belum dapat diverifikasi tanpa konfirmasi dari pengguna mengenai dashboard portal lomba**.

---

## 3. Daftar Kekurangan yang Masih Harus Diselesaikan

Berdasarkan audit ketat di atas, proyek ini berada pada tingkat keterpenuhan **$95\%$**. Dua kekurangan yang masih berstatus `PARTIAL` dan satu yang berstatus `NEEDS_VERIFICATION` adalah:

1. **Kekurangan 1 (Task 3.6 & 3.7 — Prioritas Tinggi):**  
   *Ketiadaan Sub-Bab Eksplisit "Analisis Kesalahan Berbasis XAI (XAI-Based Error Analysis)" di Notebook 07 dan Laporan XAI.*  
   Studi kasus meminta secara spesifik pembedahan kondisi pasar di mana model meleset jauh menggunakan XAI. Dua kasus historis terbaik yang telah terbukti pada data validasi adalah:
   - **Kasus Underprediction (31 Juli 2024):** Model meleset karena volatilitas historis (`rv_past20`) dan `VIX` ($16,36$) saat penutupan bursa masih tenang, sementara guncangan geopolitik/carry trade global baru meledak pada hari forward $t+3$ (*Black Monday* 5 Agustus 2024). XAI membuktikan model tertipu oleh fitur backward-looking yang belum merefleksikan stres likuiditas mendadak.
   - **Kasus Overprediction (5 Agustus 2024):** Model memprediksi volatilitas sangat tinggi ($0,0123$) akibat lonjakan VIX ke $38,57$ dan kejatuhan momentum IHSG, namun bursa mengalami normalisasi cepat (*mean-reverting volatility*) ke level $0,0055$. XAI membuktikan lonjakan prediksi murni dipicu oleh sensitivitas tinggi model terhadap VIX sesaat.

2. **Kekurangan 2 (Kesiapan Submission — Prioritas Sedang):**  
   *Konfirmasi Format Unggah Portal Lomba.*  
   Perlu memeriksa dashboard portal kompetisi INCEPTION 2026 untuk memastikan apakah panitia meminta berkas 2-kolom (`submission_blend60_40.csv`) atau dataset lengkap (`dataset_peserta_filled_blend60_40.csv`).

---

## 4. Prioritas Pengerjaan Berdasarkan Dampak Terhadap Penilaian

| Peringkat Prioritas | Item Tindakan | Justifikasi Dampak Penilaian | Rekomendasi Waktu Eksekusi |
|---|---|---|---|
| **PRIORITAS 1 (KRUSIAL)** | **Menambahkan Bab "Analisis Kesalahan Berbasis XAI" ke Laporan XAI & Slide Presentasi** | Poin ini tertulis secara eksplisit dalam panduan Task 3 Studi Kasus. Dewan juri PT Investion sangat menghargai kejujuran intelektual analis saat membedah kelemahan model menggunakan SHAP (bukan membual bahwa model sempurna). | Segera (Sebelum Final Packaging) |
| **PRIORITAS 2 (PENTING)** | **Verifikasi Template Portal Lomba & Pemilihan Champion Final** | Mencegah diskualifikasi teknis akibat kesalahan format kolom atau format berkas saat submisi resmi. | Saat konfirmasi portal dibuka |
| **PRIORITAS 3 (PENYEMPURNAAN)** | **Penyusunan Executive Summary / Deck Presentasi Komite Risiko** | Studi Kasus menetapkan peran analis kuantitatif mengawal dana triliunan rupiah PT Investion. Komite direksi membutuhkan slide/ringkasan bisnis berbasis XAI. | Tahap Akhir |

---

## 5. Rekomendasi Langkah Penutupan Proyek

1. **Langkah 1 (Opsional/Sangat Direkomendasikan):** Buat suplemen dokumentasi teknis atau perbarui laporan XAI dengan menambahkan bagian **"Analisis Kesalahan Berbasis XAI (Studi Kasus Black Monday Agustus 2024 & Pasca-Lebaran Mei 2022)"** sehingga status Task 3.6 dan 3.7 naik menjadi **`COMPLETE 100%`**.
2. **Langkah 2:** Verifikasi dashboard portal lomba untuk menetapkan berkas mana di folder `outputs/submission/` yang akan diunggah.
3. **Langkah 3:** Finalisasi repositori dan persiapan dokumen presentasi / laporan akhir untuk komite juri INCEPTION 2026.

---

### Kesimpulan Audit
Proyek **INCEPTION 2026** memiliki fondasi metodologis yang sangat kuat, disiplin anti-leakage yang terbukti dengan unit test, rekayasa fitur yang berakar pada teori keuangan makro, serta pemodelan dan dekomposisi XAI yang transparan. Seluruh butir Task 1 dan Task 2 telah **100% COMPLETE**. Pada Task 3, analisis kesalahan berbasis XAI telah teridentifikasi secara empiris dan tinggal disempurnakan penyajiannya agar memenuhi rubrik penilaian kompetisi secara sempurna.
