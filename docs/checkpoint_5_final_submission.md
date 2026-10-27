# Laporan Pelatihan Model Final, Inferensi Kompetisi, & Validasi Submission — Checkpoint 5

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 5 (Tahap Akhir: Model Retraining, Competition Test Inference, & Submission Verification)  
**Notebook Utama:** [`notebook/08_Final_Training_Submission.ipynb`](file:///z:/Projects/Inception/notebook/08_Final_Training_Submission.ipynb)  
**Skrip Generator Terkait:** [`scripts/build_final_submission_nb.py`](file:///z:/Projects/Inception/scripts/build_final_submission_nb.py), [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py)  
**Folder Output Visualisasi & Submission:** [`outputs/submission/`](file:///z:/Projects/Inception/outputs/submission/)  
**Dataset Mentah Rujukan:** `Aset Lomba/dataset peserta.csv` (Dipertahankan 100% utuh tanpa modifikasi)  

---

## 1. Champion dan Alasan Pemilihannya

### 1.1 Matriks Keputusan Kandidat Model
Sebelum menjalankan pelatihan ulang model pada seluruh data historis, kami menyusun matriks keputusan komparatif yang membandingkan secara transparan ketiga kandidat model terkuat yang telah melalui audit rekonsiliasi Checkpoint 3C.1 dan audit interpretabilitas Checkpoint 4:

| Kriteria Komparasi | Blend 50:30:20 (Hibrida ML + Naif) | Blend 60:40 (Ensemble Murni ML) | GBR Tuned Standalone (Single Model) |
|---|---|---|---|
| **Komposisi Bobot** | $0,50 \cdot \text{GBR} + 0,30 \cdot \text{Ridge} + 0,20 \cdot \text{rv20}$ | $0,60 \cdot \text{GBR} + 0,40 \cdot \text{Ridge}$ | $1,00 \cdot \text{GBR Tuned}$ |
| **Pooled MAE (2022–2024)** | **0,002377 (Peringkat 1 Absolut)** | 0,002401 (Peringkat 2, $\Delta = 0,000024$) | 0,002462 (Peringkat 3) |
| **Pooled RMSE (2022–2024)** | **0,003144 (Peringkat 1 Absolut)** | 0,003152 (Peringkat 2) | 0,003178 (Peringkat 3) |
| **Pearson Correlation ($r$)** | **0,3055 (Peringkat 1 Absolut)** | 0,2992 (Peringkat 2) | 0,2721 (Peringkat 3) |
| **Fold 3 (2024) MAE** | 0,002692 | **0,002654 (Lebih Unggul di Fold 3)** | **0,002646 (Model Tunggal Terbaik)** |
| **MAE Rezim Ekstrem (Top 5%)**| 0,007858 | **0,007778 (Lebih Tahan Guncangan)** | 0,007882 |
| **Arsitektur Model** | Hibrida: Menggabungkan model ML dengan fitur naif `rv_past20` secara linier langsung. | Ensemble Murni: Memadukan pohon keputusan non-linier L1 dengan regresi linier teratur L2. | Model Tunggal: Gradient boosting murni pohon kedalaman dangkal (`max_depth=2`). |
| **Transparansi XAI** | Memerlukan bobot heuristik tambahan di luar dekomposisi model ML. | **Superposisi Aditif Eksak 100%:** Memadukan SHAP pohon dengan koefisien linier secara presisi. | **TreeSHAP Murni:** Sifat aditif lokal eksak ($100\%$). |
| **Kepatuhan Rubrik Task 3** | Kombinasi hibrida multi-model. | Kombinasi ensemble multi-model. | **Patuh Harfiah:** Memenuhi teks "Pilih 1 jenis algoritma regresi utama". |

### 1.2 Rasionalitas Pemilihan Rekomendasi Champion:
1. **Penyataan Transparan Mengenai Kinerja MAE:**  
   Sesuai mandat pengujian, kami **TIDAK MENGKLAIM Blend 60:40 sebagai pemenang MAE validasi**. Data membuktikan secara objektif bahwa `Blend 50:30:20` mencatat Pooled MAE terendah ($0,002377$).
2. **Mengapa Blend 60:40 Direkomendasikan Sebagai Champion Utama Machine Learning?**  
   - **Kelemahan Struktural Blend 50:30:20 pada Pergeseran Rezim:** Fitur `rv_past20` telah menjadi fitur nomor 1 di dalam `GBR Tuned` (mean |SHAP| $0,000466$) dan fitur nomor 1 di dalam `Ridge Tuned` ($\beta^* = +0,000755$). Menyuntikkan bobot langsung sebesar $20\%$ di luar model melipatgandakan eksposur terhadap varians 20-hari. Ketika pasar memasuki level All-Time High pada tahun 2024 (Fold 3), kinerja `rv_past20` anjlok (MAE $0,003232$), yang menyebabkan `Blend 50:30:20` tertinggal dari `Blend 60:40` ($0,002692$ vs $0,002654$).
   - **Ketahanan Terhadap Guncangan Ekstrem:** Pada $5\%$ volatilitas pasar tertinggi ($Y > 0,012650$, $N=39$ hari), `Blend 60:40` memiliki MAE lebih rendah ($0,007778$ dibanding Blend 50:30:20 $0,007858$ dan GBR Tuned $0,007882$) karena pilar Ridge bertindak sebagai peredam overreaksi non-linier.
   - **Keselarasan Integritas XAI:** Atribusi global dan lokal pada `Blend 60:40` terbukti merupakan superposisi linier aditif yang sempurna ($\text{error} = 0,00 \times 10^{-17}$), memberikan akuntabilitas risiko yang sangat seimbang bagi Komite Risiko PT Investion.
3. **Mitigasi Risiko Total (Multi-Candidate Generation):**  
   Untuk mengantisipasi preferensi dewan juri (apakah mengutamakan skor MAE murni, integritas arsitektur ensemble ML, atau kepatuhan harfiah terhadap model tunggal), **kami mengekspor dan memvalidasi file prediksi untuk KETIGA kandidat** secara lengkap di folder `outputs/submission/`.

---

## 2. Konfigurasi Final Seluruh Komponen Model

Seluruh komponen model dilatih ulang secara penuh menggunakan data historis berlabel 2010–2024 dengan hyperparameter yang telah terkunci sejak Checkpoint 3B dan 3C:

```python
# 1. Komponen Pohon Non-Linier (GBR Tuned)
final_gbr = GradientBoostingRegressor(
    loss='absolute_error',      # Mengoptimalkan metrik evaluasi kompetisi (MAE)
    learning_rate=0.03,         # Learning rate konservatif peredam overfitting
    max_depth=2,                # Pohon dangkal (stump) penangkap interaksi orde-2
    n_estimators=100,           # Jumlah pohon optimal pada loss L1
    min_samples_leaf=1,         # Daun minimum
    random_state=42             # Reproducibility seed
)

# 2. Komponen Linier Teredam (Ridge Tuned Pipeline)
final_ridge = Pipeline([
    ('scaler', StandardScaler()),                    # Standardisasi fitur z-score (fit on train only)
    ('ridge', Ridge(alpha=1000.0, random_state=42))  # Regularisasi penalti L2 intensif peredam multikolinearitas
])

# 3. Komponen Persistensi Volatilitas Historis (rv_past20)
# Dihitung secara strictly backward-looking dari akar jumlah kuadrat return logaritmik 20 hari penutupan bursa.

# 4. Formulasi Kombinasi Prediksi:
# Prediksi Blend 60:40    = 0.60 * y_pred_gbr + 0.40 * y_pred_ridge
# Prediksi Blend 50:30:20 = 0.50 * y_pred_gbr + 0.30 * y_pred_ridge + 0.20 * rv_past20
```

---

## 3. Jumlah Baris Training dan Test yang Digunakan

### 3.1 Rincian Partisi Data Aktual
Audit komputasi pada notebook [`notebook/08_Final_Training_Submission.ipynb`](file:///z:/Projects/Inception/notebook/08_Final_Training_Submission.ipynb) mencatat penggunaan data yang diverifikasi secara eksak:

- **Total Observasi Dataset Mentah:** $4.266$ baris (`Date` 2010-01-04 hingga 2026-05-22).
- **Data Historis Berlabel Tersedia:** $3.907$ baris (`Target_Volatilitas_Y` tidak kosong).
- **Warm-Up Window Dropna (20 Hari Pertama):** $20$ baris (2010-01-04 hingga 2010-01-29) dieliminasi karena fitur rolling 20-hari (`rv_past20`, `mom_ihsg_20`) memerlukan 20 hari observasi historis pembentukan awal.
- **Data Training Final yang Digunakan ($N_{\text{train}}$):** **$3.887$ baris** (Rentang `2010-02-01` hingga `2024-12-24`).
- **Data Uji Kompetisi ($N_{\text{test}}$):** **Tepat $359$ baris** (Rentang `2025-01-02` hingga `2026-05-22`, di mana seluruh target awal berstatus `NaN`).

### 3.2 Audit Partisi Purged ($N=3.882$) vs Full ($N=3.887$)
Untuk menguji sensitivitas terhadap 5 baris batas akhir Desember 2024 (yang diidentifikasi memiliki artefak pemotongan kalender pada Checkpoint 1A), kami melatih model pembanding pada data *purged* ($N=3.882$, cut-off `2024-12-17`):
- Korelasi prediksi antara model yang dilatih pada Full ($3.887$) versus Purged ($3.882$) pada 359 hari data uji mencapai **$r = 0,997831$** dengan deviasi absolut rata-rata hanya **$0,000099$**.
- Hal ini membuktikan bahwa pelatihan model pada data penuh 2010–2024 sangat stabil dan tidak terdistorsi oleh anomali kalender batas.

---

## 4. Pemeriksaan Anti-Leakage & Integritas Pipeline

Seluruh 5 pengujian otomatis dalam suite `run_anti_leakage_and_quality_tests` lolos $100\%$ tanpa catatan:

1. **Strictly Backward-Looking Feature Windows:**  
   Seluruh 29 prediktor historis (seperti `rv_past5`, `rv_past20`, `mom_ihsg_10`, `vix_ratio_ma20`) dihitung menggunakan harga penutupan historis $[t-W+1, t]$. Tidak ada fitur yang mengakses hari besok ($t+1$).
2. **Ketersediaan Informasi EOD $t$:**  
   Seluruh variabel makro (IHSG, kurs USD/IDR, BI rate, Fed Funds Rate, yield obligasi, harga minyak, emas, dan VIX) telah dipublikasikan secara resmi pada penutupan perdagangan pukul 16:30 WIB pada hari prediksi $t$.
3. **Isolasi Target & Label Masa Depan:**  
   Kolom `Target_Volatilitas_Y` dikeluarkan secara eksplisit dari matriks prediktor (`feature_cols`). Tidak ada kolom target yang masuk sebagai input model.
4. **Isolasi Preprocessing:**  
   `StandardScaler` hanya mempelajari rata-rata ($\mu$) dan varians ($\sigma$) dari partisi training ($N=3.887$), kemudian mentransformasikannya ke data uji kompetisi tanpa memperbarui parameter skala.
5. **Koreksi Skala USD/IDR Terisolasi:**  
   Perbaikan pengali desimal $10\times$ pada dua tanggal anomali historis (2010-11-01 dan 2012-02-07) didasarkan pada audit rule eksplisit tanpa menyentuh data 2025–2026.

---

## 5. Statistik Prediksi dan Hasil Sanity Check

### 5.1 Tabel Statistik Deskriptif Prediksi Data Uji (359 Hari Bursa 2025–2026)

| Model Prediksi | Mean | Std Dev | Min | Kuartil 1 (25%) | Median (50%) | Kuartil 3 (75%) | Max | Ketiadaan NaN / Inf | Nilai Negatif |
|---|---|---|---|---|---|---|---|---|---|
| **Target Historis (2010–2024)** | 0,008345 | 0,005589 | 0,000000 | 0,004857 | 0,007054 | 0,010042 | 0,058497 | 0 NaN / 0 Inf | 0 |
|---|---|---|---|---|---|---|---|---|---|
| **Blend 60:40 (Rekomendasi)** | **0,008133** | **0,002423** | **0,005561** | **0,006376** | **0,007269** | **0,009037** | **0,020201** | **0 NaN / 0 Inf** | **0 (Strictly > 0)** |
| **Blend 50:30:20 (Kandidat MAE)**| **0,008890** | **0,002820** | **0,005592** | **0,006640** | **0,007802** | **0,010611** | **0,020721** | **0 NaN / 0 Inf** | **0 (Strictly > 0)** |
| **GBR Tuned Standalone** | **0,007654** | **0,002088** | **0,005877** | **0,006299** | **0,006737** | **0,008231** | **0,016389** | **0 NaN / 0 Inf** | **0 (Strictly > 0)** |
| Ridge Tuned Standalone | 0,008850 | 0,003139 | 0,004409 | 0,006417 | 0,008015 | 0,010564 | 0,025918 | 0 NaN / 0 Inf | 0 (Strictly > 0) |
| Persistence `rv_past20` | 0,012040 | 0,005447 | 0,005303 | 0,007560 | 0,009610 | 0,016282 | 0,026046 | 0 NaN / 0 Inf | 0 (Strictly > 0) |

### 5.2 Hasil 6 Pemeriksaan Kepatuhan & Sanity Checks
Seluruh 6 uji verifikasi otomatis pada Section 6 notebook lolos $100\%$:
- **[CHECK 1] Jumlah Baris Prediksi Tepat 359:** **PASS** (Tepat 359 observasi harian).
- **[CHECK 2] Urutan Tanggal Monotonik & Kontigu:** **PASS** (Mulai `2025-01-02` hingga `2026-05-22` tanpa duplikasi atau pergeseran indeks).
- **[CHECK 3] Ketiadaan NaN, Null, & Infinity:** **PASS** (Vektor prediksi 100% bersih).
- **[CHECK 4] Nilai Prediksi Strictly Positif:** **PASS** ($\min(\hat{Y}) = 0,005561 > 0$).
- **[CHECK 5] Rentang Volatilitas Finansial Realistis:** **PASS** (Seluruh prediksi berada pada koridor realistis $[0,00556, 0,02020]$, jauh di bawah batas atas teoritis guncangan pasar $0,0350$).
- **[CHECK 6] Konsistensi Terhadap Distribusi Historis:** **PASS** (Median prediksi `Blend 60:40` sebesar $0,007269$ selaras sempurna dengan median historis 15 tahun $0,007054$, rasio $1,031$ berada pada koridor aman $[0,80, 1,25]$).

---

## 6. Status Validasi Format Submission

### 6.1 Audit Format Resmi Kompetisi
Pemeriksaan mendalam terhadap dokumen `Aset Lomba/Studi Kasus.docx` dan `Aset Lomba/DATA DICTIONARY...docx` menunjukkan bahwa panitia kompetisi:
1. Menetapkan nama kolom target resmi sebagai: **`Target_Volatilitas_Y`**.
2. **Tidak menyertakan file template terpisah** (seperti `sample_submission.csv`) di dalam aset lomba.

### 6.2 Strategi Ekspor File Submission Multi-Varian
Untuk menjamin kesiapan pengumpulan tim PT Investion dalam menghadapi berbagai kemungkinan spesifikasi portal web lomba, kami telah membuat dua format standar di folder `outputs/submission/`:

1. **Format Standar 2-Kolom (`Date`, `Target_Volatilitas_Y`):**
   - Format paling umum pada evaluasi otomatis platform kompetisi (Kaggle/data contest custom).
   - `outputs/submission/submission_blend60_40.csv` (Rekomendasi Utama)
   - `outputs/submission/submission_blend50_30_20.csv` (Kandidat MAE Terendah)
   - `outputs/submission/submission_gbr_tuned.csv` (Kandidat Model Tunggal)
2. **Format Dataset Lengkap Terisi (`Date`, `OIL`, ..., `Target_Volatilitas_Y`):**
   - Berisi seluruh $4.266$ baris dataset peserta, di mana $359$ baris data uji yang semula kosong telah terisi prediksi model.
   - `outputs/submission/dataset_peserta_filled_blend60_40.csv`
   - `outputs/submission/dataset_peserta_filled_blend50_30_20.csv`

> [!CAUTION]
> **Peringatan Penting Sebelum Pengunggahan:**  
> Analis wajib memverifikasi petunjuk teknis di dashboard portal pengumpulan INCEPTION 2026: apakah formulir meminta file 2-kolom atau file CSV peserta lengkap. Kedua file telah siap dan dapat digunakan secara instan.

---

## 7. Lokasi Seluruh Artefak yang Dihasilkan

Seluruh artefak telah dibuat, dieksekusi dari clean kernel, dan tersimpan secara permanen pada struktur proyek:

### 7.1 Notebook & Generator
- **Notebook Final:** [`notebook/08_Final_Training_Submission.ipynb`](file:///z:/Projects/Inception/notebook/08_Final_Training_Submission.ipynb)  
  *(Telah dieksekusi dari clean kernel menggunakan nbconvert: 21 cells, 10 code cells executed cleanly, 0 errors, exit code 0).*
- **Skrip Generator Notebook:** [`scripts/build_final_submission_nb.py`](file:///z:/Projects/Inception/scripts/build_final_submission_nb.py)

### 7.2 File Submission (`outputs/submission/`)
- [`outputs/submission/submission_blend60_40.csv`](file:///z:/Projects/Inception/outputs/submission/submission_blend60_40.csv) ($359$ baris, 2 kolom, 11,9 KB) — **Rekomendasi Utama**
- [`outputs/submission/submission_blend50_30_20.csv`](file:///z:/Projects/Inception/outputs/submission/submission_blend50_30_20.csv) ($359$ baris, 2 kolom, 11,8 KB) — **Kandidat MAE Validasi**
- [`outputs/submission/submission_gbr_tuned.csv`](file:///z:/Projects/Inception/outputs/submission/submission_gbr_tuned.csv) ($359$ baris, 2 kolom, 11,8 KB) — **Kandidat Single Model**
- [`outputs/submission/dataset_peserta_filled_blend60_40.csv`](file:///z:/Projects/Inception/outputs/submission/dataset_peserta_filled_blend60_40.csv) ($4.266$ baris, 11 kolom, 646,7 KB)
- [`outputs/submission/dataset_peserta_filled_blend50_30_20.csv`](file:///z:/Projects/Inception/outputs/submission/dataset_peserta_filled_blend50_30_20.csv) ($4.266$ baris, 11 kolom, 646,7 KB)

### 7.3 Visualisasi Diagnostik (`outputs/submission/`)
- [`outputs/submission/fig_sub_01_test_trajectories.png`](file:///z:/Projects/Inception/outputs/submission/fig_sub_01_test_trajectories.png)  
  *Trajektori deret waktu prediksi forward volatility 2025–2026 melintasi seluruh model.*
- [`outputs/submission/fig_sub_02_distribution_comparison.png`](file:///z:/Projects/Inception/outputs/submission/fig_sub_02_distribution_comparison.png)  
  *KDE dan Boxplot perbandingan distribusi target historis 2010–2024 vs prediksi data uji.*
- [`outputs/submission/fig_sub_03_candidate_correlations.png`](file:///z:/Projects/Inception/outputs/submission/fig_sub_03_candidate_correlations.png)  
  *Scatter plot dan matriks korelasi antar-kandidat prediksi data uji.*

---

## 8. Keterbatasan Validasi yang Masih Berlaku

Sesuai komitmen transparansi metodologis:
1. **Validation Selection Bias:** Hyperparameter model (`learning_rate=0.03`, `max_depth=2`, `alpha=1000.0`) dan bobot blending ($60:40$ dan $50:30:20$) dioptimalkan menggunakan data validasi out-of-fold 2022–2024. Oleh karena itu, metrik validasi ($0,00237$–$0,00240$) mengandung potensi bias optimisme marjinal dan bukan estimasi independen mutlak atas performa masa depan.
2. **Status Pseudo-Holdout 2024:** Tahun 2024 telah memengaruhi pemilihan parameter (pada data 2022–2023 saja, `lr=0.05` menghasilkan MAE lebih rendah dibanding `0.03`). Oleh karena itu, data 2024 tidak dapat diklaim sebagai data yang benar-benar 'tidak terlihat' dalam siklus eksperimen.
3. **Ketidakpastian Rezim Makroekonomi 2025–2026:** Model dilatih pada data hingga akhir 2024. Meskipun fitur dan arsitektur model memiliki bantalan proteksi terhadap guncangan pasar ekstrem, pergeseran struktural moneter global atau krisis geopolitik baru di periode 2025–2026 yang belum pernah tercatat pada data latih tetap menjadi faktor risiko laten.

---

## 9. Rekomendasi Tahap Selanjutnya

Pipeline teknis, pemodelan, interpretasi XAI, inferensi, dan validasi submission telah **100% selesai dan terverifikasi secara metodologis**.

**SOP:** Berhenti di sini dan menunggu peninjauan (*review*) dari pengguna dan lead team untuk:
1. Mengonfirmasi apakah file submission resmi yang akan diunggah adalah `submission_blend60_40.csv`, `submission_blend50_30_20.csv`, atau `submission_gbr_tuned.csv`.
2. Menyesuaikan format akhir dengan template atau petunjuk pengunggahan di portal resmi INCEPTION 2026.
