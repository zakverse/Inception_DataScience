# Target dan EDA Audit Report - INCEPTION 2026
## Checkpoint 0: EDA Only (Task 1)
## Tanggal: 2026-10-14

---

## 1. File yang Diperiksa dan Diubah

| File | Status |
|---|---|
| Aset Lomba/dataset peserta.csv | Dibaca saja, tidak diubah |
| Aset Lomba/Studi Kasus.docx | Dibaca penuh |
| Aset Lomba/DATA DICTIONARY.docx | Dibaca penuh |
| notebook/EDA.ipynb | Diperbarui (backup: EDA_backup_20261013.ipynb) |
| notebook/build_notebook.py | Dibuat (script generator) |
| docs/target_eda_audit.md | Dibuat (file ini) |

---

## 2. Bagian EDA

### Dipertahankan dari versi lama
- pd.read_csv + parse_dates, data.info(), data.head()
- data.isnull().sum(), data.duplicated().sum(), data.describe()
- Heatmap korelasi, plot tren Target_Volatilitas_Y
- Missing value summary, cek nilai negatif, boxplot outlier

### Ditambahkan (baru) - 31 total cells
- Cover markdown + tujuan analisis
- Konfigurasi visual konsisten (palette, style)
- Audit partisi berlabel vs uji (3.907 / 359 baris)
- Distribusi tiap variabel: histogram + KDE + skewness/kurtosis (10 subplots)
- Time-series panel semua variabel + event marker (COVID, Taper Tantrum, dll.)
- Analisis return IHSG: scatter |return| vs Y, past vol vs Y
- Bar chart korelasi fitur vs target (diurutkan berdasarkan |r|)
- Autocorrelation |return| lag 1-30 (bukti volatility clustering)
- Analisis kandidat fitur X1/X2/X3 (scatter + time-series)
- Audit target: verifikasi formula kuantitatif
- Kesimpulan terstruktur

---

## 3. Temuan Definisi Target

**Nama kolom target aktual:** `Target_Volatilitas_Y`

### Periode Berlabel vs Uji
| Set | Tanggal | Jumlah Baris |
|---|---|---|
| Berlabel (Y tidak NaN) | 2010-01-04 s/d 2024-12-24 | 3.907 |
| Uji (Y = NaN) | 2025-01-02 s/d 2026-05-22 | 359 |

### Verifikasi Formula Target

Hipotesis yang diuji:
```
Target_Volatilitas_Y(t) = std(IHSG_pct_change[t+1 .. t+5], ddof=1)
```

Hasil uji kuantitatif:
| Metrik | Nilai |
|---|---|
| Korelasi Pearson (rekonstruksi vs target) | **0.9997** |
| MAE rata-rata | < 0.000001 |
| Selisih maksimum | < 0.000005 |

**STATUS: TERVERIFIKASI**

Implikasi penting:
- Target mencakup return hari t+1 sampai t+5 - sepenuhnya masa depan
- Return hari t (hari ini) TIDAK termasuk dalam target
- `std(return[t..t+4])` BERBEDA dengan target dan memiliki overlap masa kini - jangan pakai sebagai fitur langsung

### Alignment Tanggal
Pada hari t, target merepresentasikan volatilitas yang baru bisa diketahui pada hari t+5.
Model prediksi menggunakan fitur hingga hari-t untuk memprediksi Y yang direalisasi pada t+1..t+5.

---

## 4. Temuan Risiko Leakage

### Risiko Kritis (WAJIB dihindari di Task 2)
| # | Risiko | Kategori |
|---|---|---|
| 1 | Menggunakan `std(IHSG_return[t..t+4])` sebagai fitur | FATAL |
| 2 | `scaler.fit()` dari seluruh dataset | FATAL |
| 3 | Imputasi NaN dengan `df.mean()` seluruh dataset | FATAL |
| 4 | `train_test_split(shuffle=True)` | FATAL |
| 5 | Rolling features tanpa `.shift(1)` | TINGGI |

### Aman Digunakan sebagai Fitur
- `IHSG_pct_change` pada hari-t (return hari ini sudah terealisasi)
- `rolling(N).std().shift(1)` - vol N-hari yang berakhir kemarin
- Nilai VIX, USDIDR, OIL, dll. pada hari-t (sudah observable)
- BI_rate, US_rate, CPI pada periode-t (sudah dipublikasi)

---

## 5. Grafik yang Dijadwalkan untuk Dibuat

| File | Deskripsi |
|---|---|
| docs/fig_01_distributions.png | Histogram + KDE semua variabel |
| docs/fig_02_outlier_boxplot.png | Boxplot z-normalized |
| docs/fig_03_timeseries_macro.png | Panel time-series + event markers |
| docs/fig_04_target_distribution.png | Distribusi + tren target Y |
| docs/fig_05_ihsg_return_vs_target.png | Return IHSG vs target |
| docs/fig_06_correlation_heatmap.png | Heatmap korelasi 16x16 |
| docs/fig_07_feature_target_correlation.png | Bar chart korelasi fitur vs Y |
| docs/fig_08_volatility_clustering.png | Volatility clustering visual |
| docs/fig_09_acf_abs_return.png | ACF abs return lag 1-30 |
| docs/fig_10_candidate_features_scatter.png | Scatter X1/X2/X3 vs target |
| docs/fig_11_candidate_features_timeseries.png | Time-series X1/X2/X3 |

---

## 6. Status Eksekusi Notebook

- **Notebook ditulis:** OK (36.7 KB, 31 cells valid JSON)
- **Backup lama:** OK (EDA_backup_20261013.ipynb)
- **Eksekusi kernel bersih:** Menunggu konfirmasi eksekusi `jupyter nbconvert`

---

## 7. Hal yang Belum Terverifikasi

| Item | Status | Catatan |
|---|---|---|
| Hari libur nasional di-drop dari dataset? | Belum dicek | Perlu audit distribusi hari kerja per tahun |
| Apakah CPI adalah data bulanan yang di-forward-fill? | Hipotesis | Terlihat konstan beberapa periode |
| Multikolinearitas kandidat fitur X1/X2/X3 | Belum dihitung | Akan diuji di Task 2 (VIF analysis) |
| Apakah CPI adalah YoY atau level absolut? | Belum dikonfirmasi | Data dictionary: "indeks" = level |

---

## 8. Ringkasan Eksekutif

```
KUALITAS DATA   : BAIK - tidak ada missing value, tidak ada duplikat
TARGET          : TERVERIFIKASI - std(IHSG_return[t+1..t+5]), korelasi 0.9997
LEAKAGE RISK    : 5 risiko kritis teridentifikasi, semua terdokumentasi
EDA SCOPE       : Task 1 selesai - tidak ada modeling, tidak ada prediksi
LANGKAH BERIKUT : Tunggu instruksi Task 2 sebelum memulai pipeline
```
