# PAKET PENGUMPULAN FINAL INCEPTION 2026 — TIM GAJAHHITAM
**Nama Proyek:** Sistem Peringatan Dini Realized Volatility IHSG: Arsitektur Regresi Prediktif 5-Hari Forward dan Dekomposisi Explainable AI (SHAP)  
**Institusi / Tim:** Tim GajahHitam (PT Investion Quantitative Risk Division)  
**Trek Kompetisi:** Financial Time Series & Machine Learning Track  
**Tanggal Kompilasi:** 26 Oktober 2026  
**Status Audit Integritas:** **100% VERIFIED & IDENTICAL (SHA-256 MATCHED)**  

---

## 1. Panduan Struktur Berkas Pengumpulan

Paket ini dirancang secara terstruktur dan modular untuk memudahkan dewan juri dan panitia kompetisi dalam mereview seluruh deliverables:

```text
submission_package/
│
├── 01_Presentation/
│   ├── INCEPTION_2026_GajahHitam_PPT_Final_Audit.pdf  <-- [UTAMA/WAJIB] Slide Presentasi Final (Format PDF Resmi Juri)
│   └── INCEPTION_2026_GajahHitam_PPT_Final_Audit.pptx <-- [UTAMA/WAJIB] Slide Presentasi Final (Format PPTX 16:9)
│
├── 02_Final_Report/
│   ├── INCEPTION_2026_Final_Report.pdf               <-- [UTAMA/WAJIB] Laporan Riset Kuantitatif Final (PDF Resmi A4)
│   └── INCEPTION_2026_Final_Report.html              <-- [INTERAKTIF] Laporan Interaktif Mandiri (Bisa Dibuka Offline)
│
├── 03_Predictions/
│   ├── submission_blend60_40.csv                     <-- [SUBMISSION UTAMA] Format Standar 2-Kolom (Date, Target_Volatilitas_Y)
│   └── Optional_Backup/
│       └── dataset_peserta_filled_blend60_40.csv      <-- [CADANGAN] Format Dataset Peserta Lengkap Terisi 4.266 Baris
│
├── 04_Notebooks_and_Code/
│   ├── EDA.ipynb                                     <-- [TASK 1] Notebook 01: EDA & Formulasi Fitur Orisinal X1, X2, X3
│   ├── 02_Validation_Baseline.ipynb                  <-- [TASK 2 & 3] Notebook 02: Validasi Walk-Forward & Baseline Naif
│   ├── 03_Model_Comparison.ipynb                    <-- [TASK 3] Notebook 03: Eksplorasi 4 Model Regresi Awal
│   ├── 04_Model_Tuning.ipynb                        <-- [TASK 3] Notebook 04: Hiperparameter Tuning GBR & Ridge
│   ├── 05_Robustness_Model_Selection.ipynb          <-- [TASK 3] Notebook 05: Uji Ketahanan Krisis & Ensemble Blend 60:40
│   ├── 06_Reconciliation_Audit.ipynb                <-- [TASK 3] Notebook 06: Audit Rekonsiliasi Metrik Silang OOF 772 Hari
│   ├── 07_Model_Interpretation_XAI.ipynb            <-- [TASK 3] Notebook 07: SHAP Beeswarm Global & Waterfall Krisis
│   ├── 08_Final_Training_Submission.ipynb           <-- [TASK 3] Notebook 08: Full Retrain 3.887 Hari & Inferensi Uji 359 Hari
│   ├── feature_engineering.py                       <-- Modul Perhitungan Fitur & Uji Invariansi Anti-Leakage
│   └── scripts/
│       └── feature_engineering.py                   <-- Salinan Path Subfolder untuk Kompatibilitas Impor
│
├── 05_Documentation/
│   ├── Studi Kasus.docx                             <-- Petunjuk Teknis & Soal Studi Kasus Asli Panitia
│   ├── DATA DICTIONARY dari DATASET...docx          <-- Kamus Data Resmi dari Panitia
│   ├── final_report.md                              <-- Naskah Laporan Riset Lengkap (Format Markdown)
│   ├── checkpoint_71_final_presentation_accuracy_audit.md <-- Laporan Audit Akurasi Forensik Slide Presentasi
│   └── checkpoint_80_final_submission_inventory.md  <-- Laporan Inventarisasi Berkas Final
│
├── requirements.txt                                 <-- Daftar Dependensi Pustaka Python
└── README.md                                        <-- Panduan Navigasi & Reproduksibilitas Ini
```

---

## 2. Catatan Kritis Terkait Format Submission Resmi (`NEEDS_VERIFICATION`)

> [!IMPORTANT]
> **Pemberitahuan Format Submisi untuk Analis / Peserta:**  
> Berdasarkan dokumen `Aset Lomba/Studi Kasus.docx` dan `DATA DICTIONARY...docx`, panitia lomba tidak melampirkan file contoh format submisi (seperti `sample_submission.csv`) maupun panduan teknis pengunggahan portal.
> 
> Oleh karena itu:
> 1. **Submission Rekomendasi Utama:** `03_Predictions/submission_blend60_40.csv`  
>    Menggunakan format standar 2-kolom (`Date`, `Target_Volatilitas_Y`) berisi tepat 359 baris data uji out-of-sample (2 Januari 2025 s/d 22 Mei 2026). Format ini merupakan standar paling umum pada sistem evaluasi otomatis kompetisi data science (Kaggle/CodaLab).
> 2. **Submission Cadangan (Optional Backup):** `03_Predictions/Optional_Backup/dataset_peserta_filled_blend60_40.csv`  
>    Disediakan apabila sistem portal panitia mengharuskan pengunggahan kembali file dataset peserta utuh (4.266 baris) dengan nilai kolom target yang telah dilengkapi.
> 
> **Status Ketentuan Format Portal:** Tetap ditandai sebagai **`NEEDS_VERIFICATION`** sampai formulir portal pengumpulan lomba resmi dibuka dan dikonfirmasi.

---

## 3. Urutan Eksekusi Notebook Reproduksi (01 s/d 08)

Seluruh notebook telah dieksekusi secara berurutan pada clean kernel tanpa galat:

1. **`EDA.ipynb` (Task 1):**  
   Menganalisis karakteristik leptokurtik target historis, memverifikasi autokorelasi return absolut (volatility clustering), dan merumuskan tiga sinyal finansial baru: $X_1$ (Fear-Liquidity Composite), $X_2$ (Rate Differential Pressure), dan $X_3$ (Commodity Macro Shock).
2. **`02_Validation_Baseline.ipynb` (Task 2 & 3):**  
   Membangun skema 3-fold expanding walk-forward validation dengan gap purging $H=5$ hari. Mengukur batas acuan dasar model naif (`rv_past5`, MAE 0,002981) dan model persistensi (`rv_past20`, MAE 0,002675).
3. **`03_Model_Comparison.ipynb` (Task 3):**  
   Melakukan benchmarking awal terhadap empat kandidat model regresi: Ridge, Random Forest, Gradient Boosting, dan Linear Regression.
4. **`04_Model_Tuning.ipynb` (Task 3):**  
   Melakukan optimasi hiperparameter berbasis fungsi loss L1 (MAE) dan regularisasi L2 (Ridge $lpha=1000$) untuk menangani ekor tebal distribusi finansial.
5. **`05_Robustness_Model_Selection.ipynb` (Task 3):**  
   Melakukan uji stres rezim krisis dan merumuskan arsitektur ensemble terbobot Blend 60:40 (GBR 60% + Ridge 40%).
6. **`06_Reconciliation_Audit.ipynb` (Audit Mutu):**  
   Mengaudit konsistensi metrik evaluasi pooled OOF 772 hari, memastikan kesetaraan cakupan evaluasi antar seluruh model dan baseline.
7. **`07_Model_Interpretation_XAI.ipynb` (Task 3):**  
   Membongkar *black box* model menggunakan SHAP (SHAP Beeswarm global dan Waterfall lokal pada puncak krisis 11 Mei 2022).
8. **`08_Final_Training_Submission.ipynb` (Task 3):**  
   Melatih model final pada seluruh 3.887 hari berlabel aktif dan menghasilkan 359 prediksi out-of-sample murni untuk periode uji 2025–2026.

---

## 4. Lingkungan Komputasi & Dependensi Pustaka

Proyek ini dibangun menggunakan Python 3.10–3.12 dengan dependensi pustaka standar yang tercantum dalam `requirements.txt`:

```bash
# Instalasi pustaka yang dibutuhkan
pip install -r requirements.txt
```

Pustaka utama yang digunakan:
- `numpy >= 1.24.0`
- `pandas >= 2.0.0`
- `scipy >= 1.10.0`
- `scikit-learn >= 1.3.0`
- `matplotlib >= 3.7.0`
- `seaborn >= 0.12.0`
- `shap >= 0.42.0`
- `jupyter >= 1.0.0`
- `python-docx >= 1.1.0` (opsional untuk membaca kamus data)
- `python-pptx >= 0.6.20` (opsional untuk otomasi slide)

---

## 5. Ringkasan Kinerja Model Champion (Blend 60:40)

- **Pooled MAE (772 Hari Bursa OOF 2022–2024):** **`0,002401`**
- **Keunggulan vs Baseline Naif Resmi (`rv_past5`, MAE 0,002981):** **`+19,5%`**
- **Keunggulan vs Baseline Persistensi Kuat (`rv_past20`, MAE 0,002675):** **`+10,2%`**
- **Pooled RMSE (772 Hari Bursa OOF):** **`0,003152`** (Unggul dari Naif RMSE 0,004088)
- **MAE Rezim Krisis Ekstrem ($Y > 0,01265$, $N=39$ hari):** **`0,007778`** (Unggul 12,7% dari Naif MAE 0,008914)
- **Uji Invariansi Anti-Leakage Masa Depan:** **`0,000000000000`** deviasi (Terbukti 100% Bebas Bocor)

---
*Tim GajahHitam — PT Investion Quantitative Risk Division | INCEPTION 2026 Data Science Competition*
