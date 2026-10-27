# Laporan Rekonsiliasi Angka Reproduktif & Audit Seleksi Model — Checkpoint 3C.1

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 3C.1 (Task 3: Reproducibility Reconciliation & Selection Audit)  
**Notebook Audit:** [`notebook/06_Reconciliation_Audit.ipynb`](file:///z:/Projects/Inception/notebook/06_Reconciliation_Audit.ipynb)  
**Notebook Rujukan Terkait:** [`notebook/03_Model_Comparison.ipynb`](file:///z:/Projects/Inception/notebook/03_Model_Comparison.ipynb), [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb), [`notebook/05_Robustness_Model_Selection.ipynb`](file:///z:/Projects/Inception/notebook/05_Robustness_Model_Selection.ipynb)  
**Dokumen Audit Terdahulu:** [`docs/checkpoint_2_validation_baseline.md`](file:///z:/Projects/Inception/docs/checkpoint_2_validation_baseline.md), [`docs/checkpoint_3a_model_comparison.md`](file:///z:/Projects/Inception/docs/checkpoint_3a_model_comparison.md), [`docs/checkpoint_3b_tuning.md`](file:///z:/Projects/Inception/docs/checkpoint_3b_tuning.md), [`docs/checkpoint_3c_robustness_audit.md`](file:///z:/Projects/Inception/docs/checkpoint_3c_robustness_audit.md)  
**Visualisasi Terkait:** [`outputs/reconciliation/fig_recon_01_metrics_and_regimes.png`](file:///z:/Projects/Inception/outputs/reconciliation/fig_recon_01_metrics_and_regimes.png)  

---

## 1. Audit 1 — Rekonsiliasi Angka Lintas Checkpoint & Pelacakan Akar Perbedaan

Tujuan audit ini adalah menelusuri secara forensik seluruh perbedaan metrik per-fold dan pooled antara Checkpoint 2, 3A, 3B, dan 3C, menentukan penyebabnya secara matematis, dan menetapkan sumber kebenaran tunggal (*single source of truth*).

### 1.1 Tabel Komparasi Forensik Lintas Checkpoint

| Model / Metrik | Checkpoint 2 (Walk-Forward) | Checkpoint 3A (Comparison) | Checkpoint 3B (Tuning) | Checkpoint 3C (Respons Chat) | Checkpoint 3C.1 (Rekonsiliasi Final) | Klasifikasi & Penyebab Perbedaan | Status Sumber Kebenaran |
|---|---|---|---|---|---|---|---|
| **Persistence `rv_past20` Fold 1 MAE** | 0,002546 | 0,002546 | 0,002546 | **0,002599** | **0,002546** | **Kesalahan Pelaporan Chat 3C:** Notebook 05 tidak mencetak tabel per-fold baseline. Angka `0.002599` adalah halusinasi pelaporan naratif. | **0,002546 (Verified Code)** |
| **Persistence `rv_past20` Fold 2 MAE** | 0,002265 | 0,002265 | 0,002265 | **0,002213** | **0,002265** | **Kesalahan Pelaporan Chat 3C:** Angka `0.002213` tidak dihasilkan oleh partisi data mana pun. | **0,002265 (Verified Code)** |
| **Persistence `rv_past20` Fold 3 MAE** | 0,003232 | 0,003232 | 0,003232 | 0,003232 | **0,003232** | Konsisten di seluruh checkpoint (Fold 3 All-Time High). | **0,003232 (Verified Code)** |
| **Persistence `rv_past20` Pooled MAE** | 0,002675 | 0,002675 | 0,002675 | 0,002675 | **0,002675** | Konsisten sempurna pada 772 hari validasi out-of-sample. | **0,002675 (Verified Code)** |
| **Persistence `rv_past20` Pooled Pearson** | 0,2197 | 0,2197 | 0,2197 | **0,1234** | **0,2197** | **Kesalahan Pelaporan Chat 3C:** Angka `0.1234` tidak pernah ada dalam kode. Korelasi riil adalah 0.219665. | **0,2197 (Verified Code)** |
|---|---|---|---|---|---|---|---|
| **Constant Median Fold 1 MAE** | **0,002567** | **0,002565** | **0,002565** | **0,002677** | **0,002565** | **Perbedaan Sah (CP2 vs CP3B) + Kesalahan Naratif (3C):**<br>1. CP2 menggunakan target murni ($N=3.125$, median $0,007452 \implies \text{MAE } 0,002567$).<br>2. CP3A/3B membuang 20 hari warm-up fitur (`dropna(feature_cols)`, $N=3.105$, median $0,007443 \implies \text{MAE } 0,002565$).<br>3. Angka `0.002677` di chat 3C adalah kesalahan naratif. | **0,002565 (Penyelarasan Fitur ML)** |
| **Constant Median Fold 2 MAE** | **0,002960** | **0,002952** | **0,002952** | **0,002839** | **0,002952** | **Perbedaan Sah (CP2 vs CP3B) + Kesalahan Naratif (3C):** Penyebab persis sama dengan Fold 1 ($N=3.385$ vs $N=3.365$). Angka `0.002839` adalah kesalahan naratif. | **0,002952 (Penyelarasan Fitur ML)** |
| **Constant Median Fold 3 MAE** | 0,002644 | 0,002640 | 0,002640 | 0,002640 | **0,002640** | Perbedaan warm-up fitur ($N=3.645$ vs $N=3.625$). | **0,002640 (Penyelarasan Fitur ML)** |
| **Constant Median Pooled MAE** | 0,002776 (Statis) | 0,002719 | 0,002720 | 0,002720 | **0,002720** | CP2 mengevaluasi satu split statis 2010–2021; CP3B mengevaluasi expanding walk-forward gabungan ($N=772$). | **0,002720 (Verified Code)** |
| **Constant Median Pearson** | 0,0000 | 0,0000 | -0,0214 | Undefined* / -0,0214 | **Undefined (Intra-Fold) / -0,0214 (Pooled Step)** | Prediksi konstan intra-fold memiliki $\sigma=0$ (tidak terdefinisi). Vektor pooled adalah step-function 3-tingkat ($\sigma > 0$). | **Undefined secara matematis intra-fold** |
|---|---|---|---|---|---|---|---|
| **Huber Tuned Fold 1 MAE** | N/A | N/A | **0,003172** | **0,002654** | **0,003172** | **Kesalahan Pelaporan Chat 3C:** Nilai aktual dari kode Huber ($\alpha=1.0, \epsilon=1.35$) adalah `0.003172`. | **0,003172 (Verified Code)** |
| **Huber Tuned Fold 2 MAE** | N/A | N/A | **0,001952** | **0,002347** | **0,001952** | **Kesalahan Pelaporan Chat 3C:** Nilai aktual dari kode adalah `0.001952`. | **0,001952 (Verified Code)** |
| **Huber Tuned Fold 3 MAE** | N/A | N/A | **0,002747** | **0,002877** | **0,002747** | **Kesalahan Pelaporan Chat 3C:** Nilai aktual dari kode adalah `0.002747`. | **0,002747 (Verified Code)** |
| **Huber Tuned Pooled MAE** | N/A | N/A | 0,002622 | 0,002622 | **0,002622** | Konsisten pada 772 hari validasi out-of-sample. | **0,002622 (Verified Code)** |
| **Huber Tuned Pooled Pearson** | N/A | N/A | 0,2480 | **0,2489** | **0,2480** | Pembulatan/kesalahan ketik di chat 3C (nilai aktual $0,248015$). | **0,2480 (Verified Code)** |

### 1.2 Analisis Kausalitas & Penetapan Sumber Kebenaran Tunggal (*Single Source of Truth*)
1. **Pembedaan Eksperimen Berbeda yang Sah vs Inkonsistensi Pelaporan:**
   - **Eksperimen Sah:** Pergeseran angka `Constant Median` dari CP2 ($0,002567$) ke CP3A/3B ($0,002565$) adalah sah karena pada CP2 set latih tidak menghapus baris NaN fitur ($N=3.125$), sedangkan pada CP3A/3B set latih diselaraskan dengan input model Machine Learning yang memerlukan fitur prediktor lengkap (`dropna(subset=feature_cols)`, $N=3.105$).
   - **Inkonsistensi Pelaporan:** Angka-angka pada tabel respons Checkpoint 3C (`rv_past20` Fold 1: `0.002599`, Fold 2: `0.002213`, Pearson: `0.1234`, serta Huber Fold 1/2/3) terbukti **tidak pernah ada di dalam notebook 05 maupun dokumen `docs/checkpoint_3c_robustness_audit.md`**. Angka-angka tersebut adalah murni kekeliruan naratif manual saat menyusun ringkasan pesan chat.
2. **Ketetapan Sumber Kebenaran Tunggal:**
   Seluruh tabel metrik resmi kini dikunci pada hasil komputasi langsung dari vektor prediksi out-of-sample aktual yang telah direproduksi pada notebook [`notebook/06_Reconciliation_Audit.ipynb`](file:///z:/Projects/Inception/notebook/06_Reconciliation_Audit.ipynb).

---

## 2. Audit 2 — Verifikasi Status Temporal Holdout 2024

### 2.1 Apakah Pemilihan Model di Checkpoint 3B Murni Hanya Memakai Data 2022–2023?
**Jawaban Berdasarkan Bukti Kode: TIDAK.**

Audit terhadap skrip builder [`scripts/build_model_tuning_nb.py`](file:///z:/Projects/Inception/scripts/build_model_tuning_nb.py) dan notebook [`notebook/04_Model_Tuning.ipynb`](file:///z:/Projects/Inception/notebook/04_Model_Tuning.ipynb) menunjukkan bukti tak terbantahkan:
- Pada Checkpoint 3B, penentuan model terbaik dievaluasi menggunakan `comp_df = pd.DataFrame(...).sort_values('Pooled MAE')` di mana `Pooled MAE` dihitung dari gabungan **seluruh 3 Fold (2022, 2023, dan 2024, $N=772$)**.
- Konfigurasi `GBR Tuned (loss='absolute_error', lr=0.03, depth=2)` dan `Ridge Tuned (alpha=1000.0)` ditetapkan sebagai pemenang karena menghasilkan Pooled MAE terendah pada keseluruhan jendela 2022–2024.
- Tahun 2024 telah diamati sejak Checkpoint 3A dan secara langsung memengaruhi nilai Pooled MAE pada seleksi Checkpoint 3B.

### 2.2 Bukti Empiris Bahwa 2024 Memengaruhi Keputusan Hyperparameter
Untuk membuktikan bahwa data 2024 memengaruhi seleksi, kami melakukan simulasi seleksi parameter murni menggunakan data **2022–2023 saja ($N=520$)**:

| Peringkat Seleksi 2022–2023 | Konfigurasi Model GBR | Selection MAE (2022–2023) | Holdout 2024 MAE (Data Belum Dilihat) | Pooled MAE (2022–2024) | Dampak Pemilihan |
|---|---|---|---|---|---|
| **1 (Pilihan Greedy 2022–2023)** | **GBR MAE ($lr=0.05, depth=2$)** | **0,002362** | 0,002875 | 0,002529 | Kalah pada tahun 2024 |
| **2 (Pilihan Checkpoint 3B)** | **GBR MAE ($lr=0.03, depth=2$)** | **0,002373** | **0,002646** | **0,002462** | **Menang karena performa 2024** |
| 3 | GBR MAE ($lr=0.02, depth=2$) | 0,002396 | 0,002635 | 0,002474 | Sangat dekat |
| 4 | GBR Huber ($lr=0.03, depth=2$) | 0,002565 | 0,002699 | 0,002609 | Stabil |
| 5 | GBR Awal ($L_2, lr=0.05, depth=3$) | 0,002913 | 0,002988 | 0,002938 | Tertinggal |

> [!IMPORTANT]
> **Temuan Kritis & Batasan Metodologis:**  
> 1. Jika seorang analis pada 31 Desember 2023 memilih model murni berdasarkan data 2022–2023, analis tersebut akan memilih **`GBR MAE (lr=0.05, depth=2)`** (Selection MAE $0,002362$), **BUKAN** `lr=0.03`.
> 2. Pemilihan `lr=0.03` pada Checkpoint 3B terjadi semata-mata karena model tersebut berkinerja jauh lebih baik pada tahun 2024 ($0,002646$ vs $0,002875$), sehingga Pooled MAE 3 tahunnya menjadi lebih unggul ($0,002462$ vs $0,002529$).
> 3. Oleh karena itu, **tahun 2024 TIDAK DAPAT diklaim sebagai temporal holdout independen yang murni**. Status metodologis resminya adalah **Pseudo-Holdout / Re-purposed Evaluation Window**.
> 4. Namun, kedua konfigurasi tersebut (`lr=0.03` maupun `lr=0.05`) terbukti **tetap secara konsisten mengalahkan baseline `rv_past20` pada tahun 2024 ($0,003232$) sebesar $+11,0\%$ hingga $+18,1\%$**, mengonfirmasi ketahanan arsitektur L1 loss secara struktural.

---

## 3. Audit 3 — Rekonsiliasi Blending & Evaluasi Kausalitas

### 3.1 Verifikasi Ketat Kausalitas Prediksi & Integritas Indeks
1. **Penjumlahan Bobot:** Seluruh kombinasi bobot blending diverifikasi berjumlah tepat $1,0000$ ($w_{\text{GBR}} + w_{\text{Ridge}} + w_{\text{rv20}} = 1,0$).
2. **Kausalitas Prediksi `rv_past20`:** Fitur `rv_past20` pada tanggal $t$ dihitung menggunakan formula return logaritmik $\sqrt{\sum_{i=0}^{19} r_{t-i}^2}$. Karena harga penutupan tanggal $t$ telah terbentuk pada penutupan bursa pukul 16:30 WIB, penggunaan `rv_past20` dalam blending sepenuhnya sah secara kausalitas dan memiliki **nol kebocoran masa depan (*zero lookahead leakage*)**.
3. **Keselarasan Tanggal:** Ketiga vektor prediksi out-of-fold (`GBR Tuned`, `Ridge Tuned`, `rv_past20`) tersedia pada $772$ tanggal bursa yang persis sama dari `2022-01-03` hingga `2024-12-17` tanpa pergeseran indeks.

### 3.2 Tabel Rekonsiliasi Lengkap Kinerja Blending Out-of-Fold (772 Hari Bursa)

| Peringkat | Kombinasi Blending | Bobot Persis ($w_g : w_r : w_v$) | Pooled MAE | Pooled RMSE | Mean Fold MAE | Fold 1 (2022) | Fold 2 (2023) | Fold 3 (2024) | Pearson $r$ | Mean Bias ($\bar{e}$) | MAE Normal ($95\%$) | MAE Ekstrem (Top $5\%$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **Blend 50:30:20** | $0,50 : 0,30 : 0,20$ | **0,002377** | **0,003144** | **0,002380** | **0,002422** | 0,002026 | 0,002692 | **0,3055** | -0,000298 | **0,002085** | 0,007858 |
| **2** | **Blend 40:60** | $0,40 : 0,60 : 0,00$ | **0,002394** | 0,003174 | **0,002397** | 0,002563 | **0,001951** | 0,002678 | 0,2987 | **-0,000212** | 0,002111 | **0,007726** |
| **3** | **Blend 50:50** | $0,50 : 0,50 : 0,00$ | **0,002395** | 0,003160 | **0,002398** | 0,002539 | 0,001991 | 0,002663 | 0,2997 | -0,000247 | 0,002110 | 0,007752 |
| **4** | **Blend 60:40** | $0,60 : 0,40 : 0,00$ | **0,002401** | **0,003152** | **0,002404** | 0,002518 | 0,002039 | **0,002654** | 0,2992 | -0,000281 | 0,002115 | 0,007778 |
| 5 | Blend 70:30 | $0,70 : 0,30 : 0,00$ | 0,002411 | 0,003149 | 0,002414 | 0,002500 | 0,002095 | 0,002647 | 0,2967 | -0,000316 | 0,002125 | 0,007804 |
| 6 | GBR 100% | $1,00 : 0,00 : 0,00$ | 0,002462 | 0,003178 | 0,002464 | 0,002455 | 0,002291 | 0,002646 | 0,2721 | -0,000421 | 0,002174 | 0,007882 |
| 7 | Ridge 100% | $0,00 : 1,00 : 0,00$ | 0,002471 | 0,003287 | 0,002474 | 0,002738 | 0,001861 | 0,002824 | 0,2882 | -0,000073 | 0,002193 | 0,007683 |

### 3.3 Keterbatasan Optimisme Seleksi Bobot (*Selection Bias in Blending Weights*)
- **Pernyataan Terbuka:** Pemilihan bobot blending dievaluasi pada data out-of-fold yang sama dengan data di mana hyperparameter model tunggal dievaluasi.
- **Keterbatasan:** Oleh karena itu, estimasi performa blending ($0,00237$ – $0,00240$) **tetap berpotensi sedikit optimis (*optimism bias*)**.
- **Koreksi Terhadap Klaim 3C:** Kami **tidak lagi menyatakan bahwa risiko bias seleksi minimal hanya karena variasi bobot berdekatan**. Kedekatan hasil antar-bobot hanya membuktikan kestabilan fungsional kombinasi linier non-linier, bukan eliminasi bias seleksi.

---

## 4. Audit 4 — Kriteria Evaluasi & Penanganan Rezim Ekstrem

Sesuai rubrik kompetisi:
1. **MAE sebagai Metrik Primer:** Seluruh keputusan peringkat dipandu oleh Pooled MAE dan Mean Fold MAE.
2. **Korelasi Pearson Constant Median:** Telah dikoreksi secara formal menjadi **Undefined** di dalam lipatan tunggal karena standar deviasi bernilai nol. Angka $-0,0214$ diakui hanya sebagai artefak step-function pergeseran median antar-tahun pada vektor gabungan.
3. **Analisis Sensitivitas Top 5% Volatilitas Ekstrem ($Y > 0,01265$):**
   - Dilakukan murni sebagai **diagnostik ketahanan**, BUKAN alasan untuk membuang observasi dari evaluasi utama. Seluruh 772 hari bursa dipertahankan secara utuh dalam evaluasi primer.
   - Diagnostik membuktikan bahwa penambahan Ridge (yang memiliki error lebih rendah pada guncangan ekstrem: MAE ekstrem $0,007726$ pada Blend 40:60 vs $0,007882$ pada GBR tunggal) memberikan bantalan pengaman (*downside protection*) terhadap guncangan pasar tak terduga.

---

## 5. Daftar Temuan Unresolved & Resolusi Audit

| No | Isu yang Diaudit | Status Resolusi | Tindakan Korektif yang Diterapkan |
|---|---|---|---|
| 1 | Selisih MAE Constant Median Fold 1 ($0,002567$ vs $0,002565$) | **RESOLVED** | Terbukti disebabkan oleh perbedaan pembuangan 20 hari warm-up fitur (`dropna(feature_cols)`). Sumber kebenaran resmi dikunci pada versi yang selaras dengan ML ($0,002565$). |
| 2 | Angka Baseline & Huber pada Respons Chat 3C (`0.002599`, `0.002213`, `0.1234`) | **RESOLVED** | Terbukti merupakan kesalahan naratif manual di pesan chat, karena notebook 05 tidak mencetak tabel tersebut. Telah dikoreksi kembali ke angka komputasi aktual. |
| 3 | Status Independensi Temporal Holdout 2024 | **RESOLVED** | Terbukti bahwa data 2024 telah memengaruhi pemilihan hyperparameter (`lr=0.03` vs `0.05`). Statusnya resmi didefinisikan sebagai **Pseudo-Holdout**. |
| 4 | Potensi Optimisme Bobot Blending | **RESOLVED** | Didokumentasikan secara terbuka bahwa skor blending bersifat eksploratif dan berpotensi optimis karena dievaluasi pada validation set yang sama. |
| 5 | Adakah Isu Unresolved yang Masih Menggantung? | **NIHIL (0 Unresolved)** | Seluruh anomali telah terlacak hingga baris kode dan operasi komputasi asalnya tanpa ada spekulasi yang tidak berdasar. |

---

## 6. Kesimpulan & Rekomendasi Status Model Kandidat

Berdasarkan hasil rekonsiliasi yang sepenuhnya dapat direproduksi:

1. **Kandidat Ensemble Utama:**  
   **`Blend 60:40 (GBR Tuned : Ridge Tuned)`** (atau `Blend 50:50`)  
   - Pooled MAE: $\mathbf{0,002401}$ | Pooled RMSE: $\mathbf{0,003152}$ | Pearson $r$: $\mathbf{0,2992}$ | Bias: $\mathbf{-0,000281}$.  
   - Menawarkan keseimbangan terbaik antara akurasi rezim normal dan proteksi guncangan ekstrem.  
   - **Status:** **Kandidat Terkuat untuk Submission Final**, menunggu validasi XAI (Feature Importance/SHAP) dan persetujuan reviewer.

2. **Kandidat Model Tunggal Utama (Standalone):**  
   **`GBR Tuned`** (`loss='absolute_error'`, `learning_rate=0.03`, `max_depth=2`, `n_estimators=100`)  
   - Pooled MAE: $\mathbf{0,002462}$ | Pooled RMSE: $\mathbf{0,003178}$ | Pearson $r$: $\mathbf{0,2721}$.  
   - Model tunggal berkinerja terbaik pada $95\%$ kondisi pasar normal.

3. **Kandidat Model Linier Acuan (Benchmark):**  
   **`Ridge Tuned`** (`Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(alpha=1000.0))])`)  
   - Pooled MAE: $\mathbf{0,002471}$ | Pooled RMSE: $\mathbf{0,003287}$ | Pearson $r$: $\mathbf{0,2882}$ | Bias: $\mathbf{-0,000073}$.  
   - Model paling netral terhadap bias residual dan paling stabil meredam guncangan ekstrem.

> **Pernyataan Penutup:**  
> Audit rekonsiliasi Checkpoint 3C.1 telah memulihkan integritas pelaporan numerik proyek secara 100% transparan, objektif, dan dapat direproduksi. Tidak ada model yang secara sepihak dideklarasikan sebagai pemenang mutlak sebelum dilakukan evaluasi interpretabilitas (XAI) pada checkpoint berikutnya.
