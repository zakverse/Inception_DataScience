# Laporan Audit Slide Presentasi Penyisihan (Presentation Audit) — Checkpoint 7

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 7 (Final Submission Preparation — Slide Deck Assembly & Audit)  
**Nama Tim:** GajahHitam  
**Peran Peserta:** Senior Quantitative Risk & Machine Learning Analyst (PT Investion Asset Management Division)  
**Berkas Presentasi Utama:** [`outputs/final/DSC_GajahHitam_PPT.pptx`](file:///z:/Projects/Inception/outputs/final/DSC_GajahHitam_PPT.pptx)  
**Dimensi Layar:** 16:9 Widescreen ($13,333 \times 7,5\text{ inci}$)  
**Jumlah Slide:** Tepat **15 Slide** (Sesuai target 12–15 slide)  
**Ukuran Berkas PPTX:** $1.351,7\text{ KB}$ ($1,35\text{ MB}$)  
**Status Render Visual:** Terverifikasi 100% menggunakan PowerPoint Native COM Export (15 slide diekspor ke PNG di [`outputs/final/slides_preview/`](file:///z:/Projects/Inception/outputs/final/slides_preview/) dan diaudit bebas clipping/distorsi).

---

## 1. Daftar Slide, Sumber Data, & Status Verifikasi Visual

Tabel berikut merangkum setiap slide, topik bahasan, sumber artefak data proyek, visualisasi yang disematkan, dan status audit tampilannya:

| No | Judul / Topik Slide | Sumber Data / Dokumen Acuan | Aset Visual yang Disematkan | Status Render |
|:---:|---|---|---|:---:|
| **1** | **Sampul & Identitas Kompetisi:** Sistem Peringatan Dini Realized Volatility IHSG — Tim GajahHitam | `Aset Lomba/Studi Kasus.docx`, [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) | Desain flat corporate navy, badge kompetisi & 4 kartu metadata | **VERIFIED (PASS)** |
| **2** | **Konteks Bisnis & Manajemen Risiko:** Mengawal Dana Triliunan PT Investion | `Aset Lomba/Studi Kasus.docx`, [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) Bab 1 | 3 kartu terstruktur: Profil risiko, kelemahan naif, mandat anti-black box | **VERIFIED (PASS)** |
| **3** | **Dataset & Target Volatilitas:** Struktur Data Multivariat & Target 5-Hari Forward | `Aset Lomba/DATA DICTIONARY...docx`, [`notebook/EDA.ipynb`](file:///z:/Projects/Inception/notebook/EDA.ipynb) | [`outputs/eda/fig_03_timeseries_macro.png`](file:///z:/Projects/Inception/outputs/eda/fig_03_timeseries_macro.png) (Pergerakan multi-aset) | **VERIFIED (PASS)** |
| **4** | **Exploratory Data Analysis (EDA):** Distribusi Leptokurtik, Volatility Clustering, & Rezim | [`docs/EDA_analysis_report.md`](file:///z:/Projects/Inception/docs/EDA_analysis_report.md), [`notebook/EDA.ipynb`](file:///z:/Projects/Inception/notebook/EDA.ipynb) | [`outputs/eda/fig_08_volatility_clustering.png`](file:///z:/Projects/Inception/outputs/eda/fig_08_volatility_clustering.png) (ACF return absolut & clustering) | **VERIFIED (PASS)** |
| **5** | **Task 1: Feature Engineering:** Formulasi $X_1, X_2, X_3$ & Rasionalitas Finansial | [`docs/checkpoint_1b_feature_design.md`](file:///z:/Projects/Inception/docs/checkpoint_1b_feature_design.md), [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) | 3 kolom terstruktur dengan kotak rumus matematis & rasionalitas | **VERIFIED (PASS)** |
| **6** | **Task 1: Hipotesis Ekonomi & Validasi:** Transmisi Makro & Non-Kausalitas | [`docs/checkpoint_1b_feature_design.md`](file:///z:/Projects/Inception/docs/checkpoint_1b_feature_design.md), [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb) | [`outputs/models/fig_mod_03_feature_importance.png`](file:///z:/Projects/Inception/outputs/models/fig_mod_03_feature_importance.png) (MDI Importance Checkpoint 3A) | **VERIFIED (PASS)** |
| **7** | **Task 2: Protokol Validasi Time-Series:** Expanding Walk-Forward & Anti-Leakage | [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb), [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) | [`outputs/validation/fig_val_01_timeline_split.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_01_timeline_split.png) (Partisi waktu & Purging $H=5$) | **VERIFIED (PASS)** |
| **8** | **Task 3: Baseline & Kandidat Model:** Hierarki Pembanding & Algoritma ML | [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb), [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb) | 2 kartu komparatif: 3 model baseline vs 4 kandidat algoritma ML | **VERIFIED (PASS)** |
| **9** | **Task 3: Tuning & Seleksi Model:** Grid Search & Alasan Pemilihan Arsitektur | [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb), [`docs/checkpoint_3b_tuning.md`](file:///z:/Projects/Inception/docs/checkpoint_3b_tuning.md) | [`outputs/tuning/fig_tune_01_grid_search_curves.png`](file:///z:/Projects/Inception/outputs/tuning/fig_tune_01_grid_search_curves.png) (Kurva validasi GBR & Ridge) | **VERIFIED (PASS)** |
| **10**| **Task 3: Benchmark Evaluasi Akurasi:** Keunggulan $+19,5\%$ vs Baseline Naif | [`docs/checkpoint_63_documentation_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_63_documentation_reconciliation.md), [`notebook/06_Reconciliation_Audit.ipynb`](file:///z:/Projects/Inception/notebook/06_Reconciliation_Audit.ipynb) | Tabel metrik evaluasi 772 hari OOF & kartu ketahanan rezim ekstrem 5% | **VERIFIED (PASS)** |
| **11**| **Task 3: Explainable AI — Global:** Dekomposisi SHAP Summary Beeswarm | [`notebook/07_Model_Interpretation_XAI.ipynb`](file:///z:/Projects/Inception/notebook/07_Model_Interpretation_XAI.ipynb), [`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md) | [`outputs/xai/fig_xai_02_shap_summary_beeswarm.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_02_shap_summary_beeswarm.png) (Ranking mean \|SHAP\|) | **VERIFIED (PASS)** |
| **12**| **Task 3: Explainable AI — Lokal:** Deteksi Puncak Krisis 11 Mei 2022 | [`notebook/07_Model_Interpretation_XAI.ipynb`](file:///z:/Projects/Inception/notebook/07_Model_Interpretation_XAI.ipynb), [`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md) | [`outputs/xai/fig_xai_03_local_explanations.png`](file:///z:/Projects/Inception/outputs/xai/fig_xai_03_local_explanations.png) (Waterfall plot lokal 11 Mei 2022) | **VERIFIED (PASS)** |
| **13**| **Task 3: Error Analysis XAI:** Audit Forensik Krisis Black Monday 2024 | [`docs/checkpoint_61_xai_error_analysis.md`](file:///z:/Projects/Inception/docs/checkpoint_61_xai_error_analysis.md), [`scripts/generate_xai_error_plots.py`](file:///z:/Projects/Inception/scripts/generate_xai_error_plots.py) | [`outputs/xai/error_analysis/fig_err_01_timeline_context.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_01_timeline_context.png) (Timeline context) | **VERIFIED (PASS)** |
| **14**| **Tata Kelola & Rekomendasi Portofolio:** Batasan Model & Mitigasi Risiko | [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) Bab 7, [`docs/checkpoint_61_xai_error_analysis.md`](file:///z:/Projects/Inception/docs/checkpoint_61_xai_error_analysis.md) | Kerangka 3 lapis, batasan no prescience, dan 3 kebijakan komite risiko | **VERIFIED (PASS)** |
| **15**| **Kesimpulan Akhir & Keterlacakan:** 100% Kepatuhan & Traceability Matrix | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md), [`docs/final_report.md`](file:///z:/Projects/Inception/docs/final_report.md) Bab 8 | 3 kartu kesimpulan eksekutif & tabel keterlacakan komputasi sumber | **VERIFIED (PASS)** |

---

## 2. Verifikasi Ketat Kaidah Akurasi & Integritas Data

Audit terhadap teks dan tabel di dalam presentasi membuktikan kepatuhan $100\%$ terhadap aturan kompetisi:
1. **Penerapan Angka Hasil Rekonsiliasi Checkpoint 6.3:**
   - Baseline naif resmi (`rv_past5`): Tertera tepat **MAE $0,002981$** dan **RMSE $0,004088$** (Slide 8, 10, 15).
   - Baseline persistensi (`rv_past20`): Tertera tepat **MAE $0,002675$** dan **RMSE $0,003540$** (Slide 8, 10, 15).
   - Model tunggal (`GBR Tuned`): Tertera tepat **MAE $0,002462$** dan **RMSE $0,003178$** (Slide 8, 10).
   - Model ensemble champion (`Blend 60:40`): Tertera tepat **MAE $0,002401$** dan **RMSE $0,003152$** (Slide 8, 10, 15).
   - Klaim keunggulan relatif: Dinyatakan secara akurat sebesar **$+19,5\%$ terhadap `rv_past5`** dan **$+10,2\%$ terhadap `rv_past20`** (Slide 10, 15).
2. **Keterbukaan Metodologis (Methodological Honesty):**
   - Periode validasi 2022–2024 dinyatakan sebagai evaluasi out-of-fold (*expanding walk-forward*), namun Fold 2024 dideklarasikan secara transparan sebagai **Pseudo-Holdout** karena sempat memengaruhi proses tuning hyperparameter (Slide 7, 10).
   - Periode 2025–2026 (359 baris) dinyatakan secara tegas sebagai **data inferensi murni tanpa label ($Y=\text{NaN}$)**, BUKAN data validasi berlabel yang telah terkonfirmasi akurasinya (Slide 3, 7, 14).
3. **Integritas Batasan Explainable AI (Anti-Causal Claim):**
   - Nilai SHAP secara eksplisit didefinisikan sebagai ukuran atribusi marjinal terhadap fungsi prediksi model (*statistical predictive association*), BUKAN bukti kausalitas hukum alam atau dalil intervensi ekonomi langsung (Slide 6, 14).
   - Pada studi kasus 31 Juli 2024, diakui secara jujur bahwa model deret waktu bebas-bocor tidak memiliki bola kristal (*no prescience*) untuk meramalkan kejutan likuidasi *Yen carry trade* yang baru meledak pada $t+3$ (Slide 13, 14).

---

## 3. Hasil Pemeriksaan Visual & Rendering

Seluruh 15 slide telah diekspor ke format gambar beresolusi tinggi (PNG) menggunakan Microsoft PowerPoint COM Automation engine dan diperiksa secara visual:
1. **Rasio Layar & Margin:** Rasio $16:9$ terpasang presisi dengan batas margin kiri/kanan $0,8\text{ inci}$ dan margin bawah $0,45\text{ inci}$ yang konsisten.
2. **Keterbacaan Teks (Typography & Hierarchy):**
   - Judul slide berukuran $20\text{ pt bold}$, sub-judul $11\text{ pt}$, judul kartu $10–12\text{ pt bold}$, dan teks tubuh $8,5–10,5\text{ pt}$.
   - Seluruh kotak teks memiliki properti `word_wrap = True` dan margin yang teratur, diaudit bebas dari fenomena pemotongan teks (*text clipping*) atau teks yang meluap ke luar kartu (*overflow*).
3. **Ketajaman Visualisasi Grafik:**
   - 8 slide yang menyematkan grafik proyek asli (`fig_03`, `fig_08`, `fig_mod_03`, `fig_val_01`, `fig_tune_01`, `fig_xai_02`, `fig_xai_03`, dan `fig_err_01`) menampilkan plot beresolusi tinggi ($300\text{ DPI}$) dengan bingkai kartu putih yang serasi, label sumbu yang jelas, dan teks keterangan (*caption*) berhuruf miring.
4. **Tabel Kinerja & Keterlacakan:**
   - Tabel perbandingan metrik pada Slide 10 dan tabel keterlacakan pada Slide 15 menggunakan skema baris selang-seling (*zebra striping*) dengan header berwarna *Navy Dark* dan teks kontras tinggi yang sangat mudah dipindai oleh dewan juri.

---

## 4. Checklist Pra-Submisi untuk Peserta (Pre-Submission Checklist)

Sebelum mengunggah berkas ke portal resmi kompetisi INCEPTION 2026, peserta disarankan memastikan langkah-langkah verifikasi berikut:
- [x] **File Presentasi Siap:** Berkas `outputs/final/DSC_GajahHitam_PPT.pptx` tersedia dan dapat dibuka sempurna di aplikasi Microsoft PowerPoint.
- [x] **File Laporan Final Siap:** Berkas `docs/final_report.md` dan `outputs/final/INCEPTION_2026_Final_Report.pdf` tersedia dan tersinkronisasi 100%.
- [x] **File Prediksi Submission Siap:** 
  - `outputs/submission/submission_blend60_40.csv` (Format 2-kolom, tepat 359 baris, bebas missing/inf).
  - `outputs/submission/dataset_peserta_filled_blend60_40.csv` (Format dataset lengkap, 4.266 baris, target historis identik, 359 baris terisi).
- [ ] **Konfirmasi Dashboard Portal Lomba:** Periksa dashboard portal INCEPTION 2026 untuk melihat apakah form pengunggahan meminta format 2-kolom (`submission_blend60_40.csv`) atau format dataset penuh (`dataset_peserta_filled_blend60_40.csv`).
- [ ] **Penamaan File Akhir Sesuai Aturan Panitia:** Pastikan panitia tidak mensyaratkan format penamaan khusus (misal: `[INCEPTION2026]_[GajahHitam]_[PPT].pptx`). Jika diperlukan, ubah nama berkas sesuai template panitia sebelum klik submit.

---

### Kesimpulan Audit
Slide presentasi `outputs/final/DSC_GajahHitam_PPT.pptx` telah memenuhi seluruh standar visual, kelengkapan narasi, disiplin time-series, dan akurasi rekonsiliasi data proyek. Seluruh materi siap dipresentasikan di hadapan Dewan Juri Kompetisi INCEPTION 2026.
