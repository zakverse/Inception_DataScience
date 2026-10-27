# Laporan Audit Remake Slide Presentasi Eksekutif — Checkpoint 7.1

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Nama Tim:** Tim GajahHitam  
**Peran Peserta:** Senior Quantitative Risk & Machine Learning Analyst (PT Investion Asset Management Division)  
**Berkas Presentasi Baru:** [`outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pptx`](file:///z:/Projects/Inception/outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pptx)  
**Berkas Ekspor PDF:** [`outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pdf`](file:///z:/Projects/Inception/outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pdf)  
**Folder Pratinjau Visual (PNG):** [`outputs/final/slides_preview_remake/`](file:///z:/Projects/Inception/outputs/final/slides_preview_remake/)  
**Berkas Referensi Awal (Tidak Ditimpa):** [`outputs/final/Sistem Peringatan Dini Realized Volatility IHSG — Tim GajahHitam.pptx`](file:///z:/Projects/Inception/outputs/final/Sistem%20Peringatan%20Dini%20Realized%20Volatility%20IHSG%20%E2%80%94%20Tim%20GajahHitam.pptx)  

---

## 1. Latar Belakang & Filosofi Remake Desain

Sesuai arahan evaluasi final, presentasi telah dirombak secara menyeluruh dari gaya *card-heavy template* standar menjadi gaya **Editorial Quantitative Finance Research Report** yang lazim digunakan oleh divisi manajemen risiko institusional papan atas (seperti *Goldman Sachs Global Investment Research*, *J.P. Morgan Quantitative Strategies*, dan *AQR Capital Management*).

### Karakteristik Desain Baru:
1. **Palet Warna Institusional yang Konsisten:**
   - **Deep Midnight Navy (`#0B192C`):** Memberikan wibawa analitis pada cover, hero bar, dan tabel.
   - **Crisp Editorial White & Off-White Canvas (`#FFFFFF` / `#F8FAFC`):** Menjamin ruang kosong (*whitespace*) memadai dan keterbacaan tinggi.
   - **Institutional Teal (`#0D9488`):** Aksen utama untuk penanda status terverifikasi, keunggulan akurasi (+19,5%), dan metrik kunci.
   - **Ochre Amber (`#D97706`):** Sinyal waspada moderat dan peringatan risiko.
   - **Crimson Red (`#B91C1C`):** Sinyal krisis ekstrem dan audit kasus underprediction.
2. **Penghapusan Pola Layout Berulang:**
   - Tidak ada layout kartu generik yang diulang-ulang. Setiap slide memiliki tata letak fungsional yang berbeda: *editorial split-screen, data comparison matrix, sequential progressive flow, hero stat callouts, full-width time series spotlight, dan governance policy bands*.
3. **Penyematan Grafik Asli Beresolusi Tinggi:**
   - Seluruh visualisasi menggunakan grafik empiris asli dari artefak proyek (DPI tinggi, label terbaca, dilengkapi keterangan bernomor gambar dan tafsiran ekonomi).

---

## 2. Pemetaan 15 Slide, Sumber Data, & Perubahan Konten

| Slide | Topik / Judul Bahasan | Artefak Acuan & Visualisasi | Inovasi Desain & Perubahan Konten | Status Verifikasi |
|:---:|---|---|---|:---:|
| **1** | **Sampul & Identitas:** Sistem Peringatan Dini Realized Volatility IHSG — Tim GajahHitam | `Aset Lomba/Studi Kasus.docx`, [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) | Desain dark navy dengan badge metadata teal, 4 kartu parameter bawah, dan tipografi judul tegas. | **VERIFIED (PASS)** |
| **2** | **Executive Summary:** Tesis Eksekutif: Mengawal Portofolio Triliunan di Tengah Turbulensi Pasar | [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) Bab 1 | 3 panel analitis: Masalah bisnis (crimson), Solusi kuantitatif (teal), dan 3 Stat Callouts hasil empiris (+19,5%, 0,00000, 100% XAI). | **VERIFIED (PASS)** |
| **3** | **Dataset & Target:** Struktur Data Multivariat & Horizon Target 5-Hari Forward | `DATA DICTIONARY.docx`, [`outputs/eda/fig_03_timeseries_macro.png`](file:///z:/Projects/Inception/outputs/eda/fig_03_timeseries_macro.png) | Panel kiri memuat spesifikasi 4.266 baris, pemisahan 3.887 latih vs 359 uji, rumus matematis; panel kanan menyematkan grafik deret waktu makro. | **VERIFIED (PASS)** |
| **4** | **EDA:** Distribusi Leptokurtik, Ekor Tebal, & Fenomena Volatility Clustering | [`docs/EDA_analysis_report.md`](file:///z:/Projects/Inception/docs/EDA_analysis_report.md), [`outputs/eda/fig_08_volatility_clustering.png`](file:///z:/Projects/Inception/outputs/eda/fig_08_volatility_clustering.png) | Pita 4 metrik atas (Mean, Median, Skewness, Kurtosis); panel kiri memuat temuan fat tails dan ambang batas Y=0,012650; kanan memuat plot clustering. | **VERIFIED (PASS)** |
| **5** | **Task 1: Feature Engineering:** Tiga Sinyal Finansial Orisinal: Formulasi & Rasionalitas Pasar | [`docs/checkpoint_1b_feature_design.md`](file:///z:/Projects/Inception/docs/checkpoint_1b_feature_design.md), [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) | Tabel kuantitatif 4 kolom yang membedah formulasi matematis EOD $t$, transmisi finansial, dan peran model untuk X1, X2, dan X3; callout bawah tentang non-multikolinearitas. | **VERIFIED (PASS)** |
| **6** | **Task 1: Bukti Empiris & Batasan:** Validasi Empiris Fitur Baru & Batasan Disiplin Non-Kausal | [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb), [`outputs/models/fig_mod_03_feature_importance.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_03_feature_importance.png) | 3 bukti empiris (Ridge, MDI GBR 9,92%, heteroskedastisitas) dipadukan dengan peringatan etika institusional: asosiasi prediktif bukan kausalitas mekanistik. | **VERIFIED (PASS)** |
| **7** | **Task 2: Protokol Anti-Leakage:** Arsitektur Validasi Temporal Bebas Bocor & Uji Invariansi | [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb), [`outputs/validation/fig_val_01_timeline_split.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_01_timeline_split.png) | 4 blok horizontal berurutan (Walk-Forward, Purging H=5, StandardScaler, Uji Invariansi 0,000000000000); bawah menampilkan plot split timeline penuh. | **VERIFIED (PASS)** |
| **8** | **Task 3: Arsitektur Pemodelan:** Hierarki Pemodelan: Tolok Ukur Historis vs Kandidat Machine Learning | [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb), [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb) | Dua panel komparatif: Kelompok A (Constant Median, Naif rv_past5, Persistensi rv_past20) vs Kelompok B (Ridge, GBR Tuned, Blend 60:40, Blend 50:30:20). | **VERIFIED (PASS)** |
| **9** | **Task 3: Seleksi Arsitektur:** Optimasi Hiperparameter: Fungsi Loss L1 & Kontrol Overfitting | [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb), [`outputs/tuning/fig_tune_01_grid_search_curves.png`](file:///z:/Projects/Inception/outputs/tuning/fig_tune_01_grid_search_curves.png) | Penjelasan teknis pemilihan Loss L1 (median bersyarat), pohon dangkal depth 2, shrinkage 0,03, dan penalti Ridge 1000; kanan memuat kurva validasi tuning. | **VERIFIED (PASS)** |
| **10** | **Task 3: Evaluasi Kuantitatif:** Rekonsiliasi Evaluasi OOF 772 Hari: Keunggulan +19,5% vs Naif | [`docs/checkpoint_63_documentation_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_63_documentation_reconciliation.md), [`notebook/06_Reconciliation_Audit.ipynb`](file:///z:/Projects/Inception/notebook/06_Reconciliation_Audit.ipynb) | Callout banner keunggulan +19,5% (0,002401 vs 0,002981); tabel performa 6 baris lengkap; catatan kejujuran metodologi Fold 2024 pseudo-holdout. | **VERIFIED (PASS)** |
| **11** | **Task 3: Explainable AI Global:** Dekomposisi SHAP Global: Hierarki Pengaruh & Transmisi Risiko | [`notebook/07_Model_Interpretation_XAI.ipynb`](file:///z:/Projects/Inception/notebook/07_Model_Interpretation_XAI.ipynb), [`outputs/xai/fig_xai_02_shap_summary_beeswarm.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_02_shap_summary_beeswarm.png) | Peringkat 5 fitur teratas mean \|SHAP\| (rv_past20, mom_ihsg_10, US_rate, VIX, X1); kanan menampilkan beeswarm plot resmi OOF. | **VERIFIED (PASS)** |
| **12** | **Task 3: Explainable AI Lokal:** Audit Forensik Krisis 11 Mei 2022: Deteksi Dini Puncak Volatilitas | [`notebook/07_Model_Interpretation_XAI.ipynb`](file:///z:/Projects/Inception/notebook/07_Model_Interpretation_XAI.ipynb), [`outputs/xai/fig_xai_03_local_explanations.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_03_local_explanations.png) | Rekonstruksi kasus Red Alert pembukaan bursa pasca-Lebaran (aktual 0,01974, pred 0,01274); dekomposisi kontribusi SHAP VIX, return 5d, tren 10d, dan valuasi indeks. | **VERIFIED (PASS)** |
| **13** | **Task 3: Audit Kesalahan Prediksi:** Analisis Galat Ekstrem: Forensik Black Monday Agustus 2024 | [`docs/checkpoint_61_xai_error_analysis.md`](file:///z:/Projects/Inception/docs/checkpoint_61_xai_error_analysis.md), [`outputs/xai/error_analysis/fig_err_01_timeline_context.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_01_timeline_context.png) | Dua panel komparatif atas: Underprediction 31 Juli (kejutan eksogen BoJ pada t+3, no prescience) vs Overprediction 5 Agustus (reversi BoJ, reduksi galat 38,7% vs naif); bawah memuat timeline context. | **VERIFIED (PASS)** |
| **14** | **Task 3: Rekomendasi Komite Risiko:** Tata Kelola Risiko Portofolio: Kerangka Kebijakan Dinamis Tiga Rezim | [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) Bab 7 | Matriks alokasi aset dinamis 3 pita: Tenang (Hijau, Ekuitas 90-95%), Waspada (Kuning, Ekuitas 75-80%), dan Krisis (Merah, Ekuitas 50-60%); 3 mandat tata kelola institusional. | **VERIFIED (PASS)** |
| **15** | **Kesimpulan & Keterlacakan:** Kesimpulan Akhir & Matriks Keterlacakan Komputasi Sumber | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md), [`outputs/submission/submission_blend60_40.csv`](file:///z:/Projects/Inception/outputs/submission/submission_blend60_40.csv) | Kiri merangkum 3 pilar kesiapan sistem; kanan memuat tabel keterlacakan komputasi sumber; status kesiapan submisi 359 baris out-of-sample murni. | **VERIFIED (PASS)** |

---

## 3. Verifikasi Akurasi & Rekonsiliasi Angka (Checkpoint 6.3)

Semua angka yang tercantum di dalam slide baru telah dicocokkan langsung dengan artefak kode komputasi:
1. **Hierarki Baseline vs Model:**
   - `Constant Median`: MAE **0,003299**; RMSE **0,004454** *(tidak disamakan dengan rv_past5)*.
   - `Baseline Naif Resmi (rv_past5)`: MAE **0,002981**; RMSE **0,004088**.
   - `Baseline Persistensi Kuat (rv_past20)`: MAE **0,002675**; RMSE **0,003540**.
   - `Ridge Tuned (Alpha 1000)`: MAE **0,002476**; RMSE **0,003289**.
   - `GBR Tuned (Champion Tunggal)`: MAE **0,002462**; RMSE **0,003178**.
   - `Blend 60:40 (Ensemble Champion)`: MAE **0,002401**; RMSE **0,003152**.
2. **Kalkulasi Keunggulan Relatif MAE:**
   $$\text{Keunggulan vs Naif} = \frac{0,002981 - 0,002401}{0,002981} = \frac{0,000580}{0,002981} = 19,4566\% \approx \mathbf{+19,5\%}$$
   $$\text{Keunggulan vs Persistensi} = \frac{0,002675 - 0,002401}{0,002675} = \frac{0,000274}{0,002675} = 10,2430\% \approx \mathbf{+10,2\%}$$
3. **Rezim Ekstrem ($Y > 0,012650$, Top 5% OOF, $N=39$ hari):**
   - Naif `rv_past5`: MAE **0,008914**
   - Persistensi `rv_past20`: MAE **0,008310**
   - GBR Tuned: MAE **0,007882**
   - Blend 60:40: MAE **0,007778** (meredam lonjakan galat krisis secara konsisten)
   - Ridge Tuned: MAE **0,007683**
4. **Studi Kasus 11 Mei 2022 & Black Monday 2024:**
   - 11 Mei 2022: Aktual $Y = 0,01974$ (Red Alert terpicu pada proyeksi $0,01274$).
   - 31 Juli 2024: Aktual $Y = 0,01258$, Prediksi $0,00583$, Residual $-0,00675$.
   - 5 Agustus 2024: Aktual $Y = 0,00473$, Prediksi $0,01231$, Residual $+0,00758$ (galat model $38,7\%$ lebih rendah dari naif $0,01662$).

---

## 4. Batasan Model & Bagian yang Ditegaskan Bebas Klaim Berlebih

Untuk menjaga integritas ilmiah dan reputasi kuantitatif di hadapan dewan juri:
1. **Tidak Ada Klaim Bola Kristal (*No Prescience*):**
   Model diakui secara jujur tidak mampu meramalkan keputusan kenaikan suku bunga BoJ pada 31 Juli 2024 yang bersifat eksogen mendadak.
2. **Status Pseudo-Holdout Fold 2024:**
   Diakui secara terbuka bahwa Fold 2024 adalah pseudo-holdout karena penyetelan parameter model pernah melibatkan evaluasi pada fold tersebut.
3. **Data Uji 2025–2026 (359 Baris):**
   Ditegaskan bahwa data kompetisi 2025–2026 adalah data inferensi murni tanpa label ($Y=\text{NaN}$), sehingga **tidak diklaim memiliki skor akurasi tertentu** sebelum evaluasi panitia.
4. **Batas Non-Kausalitas SHAP:**
   SHAP beeswarm dan waterfall ditegaskan sebagai ukuran kontribusi marjinal prediktif, bukan bukti hubungan kausalitas mekanistik.

---

## 5. Ringkasan Status Berkas Keluaran

| Tipe Berkas | Lokasi Berkas | Status Render & Verifikasi |
|---|---|:---:|
| **PowerPoint (.pptx)** | [`outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pptx`](file:///z:/Projects/Inception/outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pptx) | **PASS (1,38 MB, 15 Slide)** |
| **PDF Dokumen (.pdf)** | [`outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pdf`](file:///z:/Projects/Inception/outputs/final/INCEPTION_2026_GajahHitam_PPT_Remake.pdf) | **PASS (1,23 MB, 15 Halaman)** |
| **Pratinjau Slide (PNG)** | [`outputs/final/slides_preview_remake/`](file:///z:/Projects/Inception/outputs/final/slides_preview_remake/) (Slide1.PNG – Slide15.PNG) | **PASS (100% Diaudit Visual)** |
| **Laporan Audit** | [`docs/checkpoint_7_presentation_remake_audit.md`](file:///z:/Projects/Inception/docs/checkpoint_7_presentation_remake_audit.md) | **DOKUMEN INI** |
