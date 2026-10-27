# Laporan Rekonsiliasi Dokumentasi Proyek (Documentation Reconciliation) — Checkpoint 6.3

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 6.3 (Sinkronisasi Dokumentasi Pasca-Audit Konsistensi Lintas Artefak)  
**Dokumen Acuan:** [`docs/checkpoint_62_final_consistency_audit.md`](file:///z:/Projects/Inception/docs/checkpoint_62_final_consistency_audit.md)  
**Dokumen yang Diperbarui:**
1. [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) (Sinkronisasi Baseline Naif `rv_past5` & Keunggulan Model)
2. [`docs/checkpoint_5_final_submission.md`](file:///z:/Projects/Inception/docs/checkpoint_5_final_submission.md) (Sinkronisasi MAE Rezim Ekstrem Top 5%)
3. [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (Sinkronisasi MAE Rezim Normal & Ekstrem Tabel 3.2)  
**Aturan Disiplin:** Dataset mentah, arsitektur model, bobot hyperparameter, hasil prediksi test, dan seluruh berkas submission di folder `outputs/submission/` dipertahankan 100% utuh tanpa modifikasi (*strictly read-only*).

---

## 1. Ringkasan Eksekutif Rekonsiliasi

Berdasarkan temuan audit komprehensif pada Checkpoint 6.2, terdapat dua ketidaksesuaian dokumentasi numerik yang memerlukan sinkronisasi formal:
- **Prioritas A (Baseline Naif `rv_past5`):** Menyelaraskan angka Pooled MAE dan RMSE baseline naif resmi kompetisi pada laporan kepatuhan studi kasus agar cocok dengan sumber komputasi aslinya pada `notebook/02_Validation_Baseline.ipynb` Cell 10, serta merevisi persentase keunggulan model secara jujur dan akurat.
- **Prioritas B (MAE Rezim Ekstrem Top 5%):** Menyelaraskan angka MAE rezim normal dan ekstrem pada laporan Checkpoint 5 dan Checkpoint 3C.1 agar seragam dengan keluaran komputasi `notebook/06_Reconciliation_Audit.ipynb` Cell 8 berdasarkan ambang batas persentil ke-95 target yang baku.

Seluruh perbaikan telah dieksekusi secara bedah (*surgical edits*) pada dokumen terkait. Tidak ada laporan lain yang tidak terdampak diubah.

---

## 2. Tabel Rekonsiliasi Nilai Dokumentasi Lintas Artefak

Tabel berikut merangkum nilai lama, nilai terverifikasi, sumber kode komputasi, dan dokumen yang diperbarui:

| No | Parameter / Metrik | Nilai Lama (Sebelumnya) | Nilai Terverifikasi (Tersinkronisasi) | Sumber Komputasi Asli | Dokumen yang Diperbarui | Status |
|:---:|---|---|---|---|---|:---:|
| **1** | **Pooled MAE Baseline Naif `rv_past5`** | $0,003299$ | **$0,002981$** | `notebook/02_Validation_Baseline.ipynb` Cell 10 | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) (baris 157) | **RESOLVED** |
| **2** | **Pooled RMSE Baseline Naif `rv_past5`** | $0,004456$ | **$0,004088$** | `notebook/02_Validation_Baseline.ipynb` Cell 10 | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) (baris 157) | **RESOLVED** |
| **3** | **Keunggulan MAE Blend 60:40 vs `rv_past5`** | $+27,2\%$ | **$+19,5\%$** | Komputasi Riil: $\frac{0,002981 - 0,002401}{0,002981}$ | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) (baris 160) | **RESOLVED** |
| **4** | **Keunggulan MAE GBR Tuned vs `rv_past5`** | $+25,4\%$ | **$+17,4\%$** | Komputasi Riil: $\frac{0,002981 - 0,002462}{0,002981}$ | [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) (baris 159) | **RESOLVED** |
| **5** | **MAE Rezim Ekstrem Blend 60:40 (Top 5%)** | $0,007584$ | **$0,007778$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_5_final_submission.md`](file:///z:/Projects/Inception/docs/checkpoint_5_final_submission.md) (baris 24 & 34), [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 91) | **RESOLVED** |
| **6** | **MAE Rezim Ekstrem Blend 50:30:20 (Top 5%)**| $0,007604$ | **$0,007858$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_5_final_submission.md`](file:///z:/Projects/Inception/docs/checkpoint_5_final_submission.md) (baris 24 & 34), [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 88) | **RESOLVED** |
| **7** | **MAE Rezim Ekstrem Blend 40:60 (Top 5%)** | $0,007447$ | **$0,007726$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 89 & 110) | **RESOLVED** |
| **8** | **MAE Rezim Ekstrem Blend 50:50 (Top 5%)** | $0,007505$ | **$0,007752$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 90) | **RESOLVED** |
| **9** | **MAE Rezim Ekstrem Blend 70:30 (Top 5%)** | $0,007683$ | **$0,007804$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 92) | **RESOLVED** |
| **10**| **MAE Rezim Normal Blend 50:30:20 (95%)** | $0,002102$ | **$0,002085$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 88) | **RESOLVED** |
| **11**| **MAE Rezim Normal Blend 40:60 (95%)** | $0,002128$ | **$0,002111$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 89) | **RESOLVED** |
| **12**| **MAE Rezim Normal Blend 50:50 (95%)** | $0,002126$ | **$0,002110$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 90) | **RESOLVED** |
| **13**| **MAE Rezim Normal Blend 60:40 (95%)** | $0,002128$ | **$0,002115$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 91) | **RESOLVED** |
| **14**| **MAE Rezim Normal Blend 70:30 (95%)** | $0,002133$ | **$0,002125$** | `notebook/06_Reconciliation_Audit.ipynb` Cell 8 | [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md) (baris 92) | **RESOLVED** |

---

## 3. Rincian Rekonsiliasi Prioritas A: Baseline Naif `rv_past5`

### 3.1 Verifikasi Cakupan Evaluasi & Sampel Data
Pemeriksaan kode komputasi pada [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb) Cell 8 dan Cell 10 memastikan bahwa metrik baseline naif `rv_past5` dihitung pada partisi:
- **Cakupan Tanggal:** `2022-01-03` hingga `2024-12-17`.
- **Jumlah Observasi:** Tepat **$772$ baris bursa**.
- **Penyelarasan dengan Model ML:** Model `Blend 60:40` dievaluasi melalui cross-validation expanding walk-forward 3-lipatan:
  - Fold 1 (2022): $260$ baris bursa.
  - Fold 2 (2023): $260$ baris bursa.
  - Fold 3 (2024): $252$ baris bursa.
  - Total Out-of-Fold: Tepat **$772$ baris bursa** dengan tanggal-tanggal yang identik $100\%$.

### 3.2 Bukti Komputasi Asli
Pada Cell 10 Notebook 02, eksekusi fungsi `evaluate_baseline_models` menghasilkan tabel benchmark:
```
       Model Baseline      MAE     RMSE  Pearson r
 Persistence rv_past5 0.002981 0.004088   0.207738
Persistence rv_past20 0.002675 0.003540   0.219665
```

### 3.3 Perhitungan Keunggulan Komparatif yang Sah
Membandingkan model rekomendasi `Blend 60:40` (Pooled MAE $= 0,002401$) terhadap baseline naif terverifikasi ($0,002981$):
$$\Delta_{\text{MAE}} = \frac{0,002981 - 0,002401}{0,002981} = \frac{0,000580}{0,002981} = \mathbf{+19,46\% \approx +19,5\%}$$
Dan terhadap baseline persistensi kuat `rv_past20` ($0,002675$):
$$\Delta_{\text{MAE}} = \frac{0,002675 - 0,002401}{0,002675} = \frac{0,000274}{0,002675} = \mathbf{+10,24\% \approx +10,2\%}$$

Untuk model tunggal `GBR Tuned` (Pooled MAE $= 0,002462$):
$$\Delta_{\text{MAE}} = \frac{0,002981 - 0,002462}{0,002981} = \frac{0,000519}{0,002981} = \mathbf{+17,41\% \approx +17,4\%}$$

### 3.4 Perubahan Aktual pada Dokumen
Pada [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md) Bagian 2.3 Butir 3, klaim numerik diperbarui menjadi:
- *Baseline Naif Resmi (`rv_past5`): Pooled MAE = $0,002981$ | Pooled RMSE = $0,004088$ (terverifikasi pada 772 hari validasi di notebook/02_Validation_Baseline.ipynb Cell 10).*
- *GBR Tuned: Pooled MAE = $0,002462$ (Unggul $+17,4\%$ vs rv_past5; $+8,0\%$ vs rv_past20).*
- *Blend 60:40: Pooled MAE = $0,002401$ (Unggul $+19,5\%$ vs rv_past5; $+10,2\%$ vs rv_past20).*

---

## 4. Rincian Rekonsiliasi Prioritas B: MAE Rezim Ekstrem (Top 5%)

### 4.1 Definisi Protokol & Metode Threshold
Pemeriksaan kode komputasi pada [`notebook/05_Robustness_Model_Selection.ipynb`](file:///z:/Projects/Inception/notebook/05_Robustness_Model_Selection.ipynb) Cell 10 dan [`notebook/06_Reconciliation_Audit.ipynb`](file:///z:/Projects/Inception/notebook/06_Reconciliation_Audit.ipynb) Cell 8 membuktikan bahwa protokol resmi proyek adalah:
1. **Perhitungan Ambang Batas:** `pct95 = np.percentile(y_true_reconciled, 95)` pada seluruh 772 nilai target validasi out-of-fold.
2. **Nilai Ambang Batas Persentil 95 ($Y_{\text{threshold}}$):** Tepat **$0,012650$**.
3. **Jumlah Observasi Terfilter:**
   - **Rezim Ekstrem ($Y > 0,012650$):** Tepat **$39$ hari bursa** ($39 / 772 = 5,05\%$).
   - **Rezim Normal ($Y \le 0,012650$):** Tepat **$733$ hari bursa** ($733 / 772 = 94,95\%$).

### 4.2 Rasionil Pemilihan Definisi
1. **Konsistensi dengan Notebook Rekonsiliasi:** Definisi ini adalah kode yang dieksekusi secara nyata pada `notebook/06_Reconciliation_Audit.ipynb` Cell 8 dan tercetak pada visualisasi resmi [`outputs/reconciliation/fig_recon_01_metrics_and_regimes.png`](file:///z:/Projects/Inception/outputs/reconciliation/fig_recon_01_metrics_and_regimes.png).
2. **Prinsip Kejujuran Ilmiah (Non-Cherry Picking):** Angka MAE ekstrem Blend 60:40 yang baru ($0,007778$) sedikit lebih tinggi (lebih konservatif) dibanding angka draf sebelumnya ($0,007584$). Pemilihan ini didasarkan murni pada reproduksibilitas komputasi, bukan memilih angka yang tampak lebih bagus.
3. **Kestabilan Peringkat Ketahanan Model:**
   Baik pada komputasi lama maupun baru, hierarki ketahanan model pada guncangan ekstrem tetap konsisten:
   $$\text{Ridge Tuned } (0,007683) < \text{Blend 40:60 } (0,007726) < \text{Blend 60:40 } (0,007778) < \text{Blend 50:30:20 } (0,007858) < \text{GBR Tuned } (0,007882)$$
   Hal ini menegaskan bahwa pilar linier teratur Ridge berperan vital sebagai peredam risiko ekstrem saat dipadukan dengan pohon keputusan non-linier GBR.

### 4.3 Perubahan Aktual pada Dokumen
1. **Pada [`docs/checkpoint_5_final_submission.md`](file:///z:/Projects/Inception/docs/checkpoint_5_final_submission.md):**
   - Tabel 1.1 baris 24: Nilai diperbarui menjadi `0,007858` (Blend 50:30:20), `0,007778` (Blend 60:40), dan `0,007882` (GBR Tuned).
   - Bagian 1.2 Butir 2 (baris 34): Teks diperbarui menjadi *"Pada 5% volatilitas pasar tertinggi ($Y > 0,012650$, $N=39$ hari), Blend 60:40 memiliki MAE lebih rendah (0,007778 dibanding Blend 50:30:20 0,007858 dan GBR Tuned 0,007882) karena pilar Ridge bertindak sebagai peredam overreaksi non-linier."*
2. **Pada [`docs/checkpoint_3c1_reconciliation.md`](file:///z:/Projects/Inception/docs/checkpoint_3c1_reconciliation.md):**
   - Tabel 3.2 baris 88–92: Kolom `MAE Normal (95%)` dan `MAE Ekstrem (Top 5%)` disinkronkan secara presisi dengan keluaran Cell 8 Notebook 06.
   - Bagian 4 Butir 3 (baris 110): Angka diperbarui menjadi *"MAE ekstrem 0,007726 pada Blend 40:60 vs 0,007882 pada GBR tunggal"*.

---

## 5. Pemeriksaan Konsistensi Akhir Pasca-Perubahan (*Post-Change Verification*)

Skrip audit independen dijalankan ulang untuk memvalidasi bahwa seluruh ketidaksinkronan telah tereliminasi:
1. **Pemeriksaan `rv_past5`:**
   - Notebook 02 Cell 10: MAE $0,002981$ | RMSE $0,004088$.
   - Dokumen CP 6 baris 157: MAE $0,002981$ | RMSE $0,004088$.
   - **Status: SYNCHRONIZED (MATCH 100%).**
2. **Pemeriksaan MAE Rezim Ekstrem:**
   - Notebook 06 Cell 8: Blend 60:40 $= 0,007778$ | Blend 50:30:20 $= 0,007858$.
   - Dokumen CP 5 Tabel 1.1 & Dokumen CP 3C1 Tabel 3.2: Blend 60:40 $= 0,007778$ | Blend 50:30:20 $= 0,007858$.
   - **Status: SYNCHRONIZED (MATCH 100%).**
3. **Integritas Berkas Submission:**
   - Seluruh 5 file CSV submission di `outputs/submission/` tetap utuh bit-for-bit dengan checksum identik.
   - **Status: VERIFIED UNCHANGED.**

---

### Kesimpulan Rekonsiliasi
Seluruh ketidaksesuaian yang diidentifikasi pada Checkpoint 6.2 telah diselesaikan secara tuntas dan terdokumentasi dengan transparan. Dokumentasi proyek **INCEPTION 2026** kini berada pada tingkat konsistensi matematis dan faktual **$100\%$**, siap untuk presentasi akhir dan penutupan proyek.
