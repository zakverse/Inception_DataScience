# Laporan Strategi Validasi Time-Series & Baseline Benchmarking — Checkpoint 2

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 2 (Task 2: Time-Series Split, Purging, & Baseline Benchmarking)  
**Notebook Utama:** [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb)  
**Modul Kode Terkait:** [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py), [`scripts/build_validation_nb.py`](file:///z:/Projects/Inception/scripts/build_validation_nb.py)  
**Folder Output Visualisasi:** [`outputs/validation/`](file:///z:/Projects/Inception/outputs/validation/)  
**Status Eksekusi Kernel Bersih:** **100% PASS** (8/8 code cells tereksekusi tanpa error)

---

## 1. Executive Summary & Tujuan Checkpoint 2

Checkpoint 2 membangun arsitektur validasi temporal yang ketat dan menetapkan standar performa (*benchmark baseline*) yang adil sebelum melangkah ke pemodelan Machine Learning (Task 3). Misi utama dari tahapan ini meliputi:
1. **Penerapan Pipeline Preprocessing & Feature Engineering:** Memanfaatkan modul terisolasi [`scripts/feature_engineering.py`](file:///z:/Projects/Inception/scripts/feature_engineering.py) untuk mengoreksi kurs USD/IDR dan membentuk fitur historis tanpa mengubah CSV mentah.
2. **Definisi Skema Pemisahan Temporal Ketat:** Menetapkan partisi Train (2010–2021), Validation (2022–2024), dan Test Kompetisi (2025–2026) dengan urutan kronologis yang tidak dapat dibalik.
3. **Penerapan Purging Matematis ($H=5$):** Menghapus tepat 5 hari perdagangan terakhir dari set latih untuk mengeliminasi tumpang tindih (*overlap*) target label ke periode validasi.
4. **Penetapan & Komparasi Kinerja Baseline:** Mengevaluasi model naif konstan (*Constant Mean*, *Constant Median*) serta model persistensi volatilitas (`rv_past5`, `rv_past10`, `rv_past20`) menggunakan metrik MAE dan RMSE pada periode validasi yang identik.
5. **Evaluasi Tambahan Expanding-Window Walk-Forward:** Menguji stabilitas baseline melintasi 3 lipatan tahun (2022, 2023, 2024) untuk memverifikasi ketahanan terhadap pergeseran rezim pasar.
6. **Verifikasi Kepatuhan Anti-Leakage Otomatis:** Membuktikan bahwa seluruh proses pemisahan dan baseline bebas dari kebocoran informasi masa depan melalui 6 unit test otomatis.

---

## 2. Arsitektur Pemisahan Data Temporal (Time-Series Split Architecture)

Sesuai instruksi kompetisi, pengacakan data (*random train-test split*) dilarang keras. Data dipartisi berdasarkan urutan waktu nyata dengan batas-batas yang terdefinisi secara kuantitatif:

### 2.1 Ringkasan Partisi Dataset

| Partisi Data | Rentang Tanggal Aktual | Jumlah Observasi (Baris) | Status Label Target ($Y$) | Peran Metodologis |
|---|---|---|---|---|
| **Training (Mentah)** | 2010-01-04 s/d 2021-12-31 | 3.130 baris | Lengkap ($Y \neq \text{NaN}$) | Data historis 12 tahun (fase pra-purge). |
| **Purged Buffer ($H=5$)** | **2021-12-27 s/d 2021-12-31** | **5 baris** | Lengkap ($Y \neq \text{NaN}$) | **Dikeluarkan dari Train** untuk mencegah target overlap ke 2022. |
| **Training (Purged Resmi)** | **2010-01-04 s/d 2021-12-24** | **3.125 baris** | Lengkap ($Y \neq \text{NaN}$) | Data latih resmi untuk fitting baseline & model ML. |
| **Validation (Clean)** | **2022-01-03 s/d 2024-12-17** | **772 baris** | Lengkap ($Y \neq \text{NaN}$) | **Partisi validasi utama** (bebas dari artefak batas akhir 2024). |
| **Boundary Purge 2024** | **2024-12-18 s/d 2024-12-24** | **5 baris** | Lengkap ($Y \neq \text{NaN}$) | 5 baris artefak pemotongan kalender CSV peserta. |
| **Validation (All)** | 2022-01-03 s/d 2024-12-24 | 777 baris | Lengkap ($Y \neq \text{NaN}$) | Partisi validasi pembanding (menyertakan 5 baris batas). |
| **Test Kompetisi** | **2025-01-02 s/d 2026-05-22** | **359 baris** | **Kosong ($Y = \text{NaN}$)** | Data evaluasi akhir panitia (**dilarang untuk evaluasi metrik**). |

*Visualisasi arsitektur partisi tersimpan di [`outputs/validation/fig_val_01_timeline_split.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_01_timeline_split.png).*

### 2.2 Perlakuan Khusus Terhadap 5 Label Terakhir Tahun 2024
Sebagaimana dibuktikan pada Checkpoint 1A, tanggal perdagangan pada `dataset peserta.csv` melompat langsung dari `2024-12-24` ke `2025-01-02` (hari bursa 27 dan 30 Desember 2024 tidak ada di CSV peserta). Karena target $Y$ berorientasi 5 hari ke depan, 5 baris terakhir (18–24 Desember 2024):
1. Mengalami deviasi mikro pada formula rekonstruksi karena melompati hari bursa akhir tahun.
2. Memiliki horizon target yang berbatasan langsung dengan awal data uji 2025.
3. **Keputusan Metodologis:** Periode validasi resmi dibatasi hingga **17 Desember 2024** (`val_clean`, 772 baris) agar bebas dari distorsi kalender bursa, sementara komparasi pada seluruh data validasi (`val_all`, 777 baris) tetap dilaporkan secara transparan.

---

## 3. Mekanisme Purging vs Embargo: Landasan Metodologis

Terdapat perbedaan mendasar antara **Purging** dan **Embargo** dalam ekonometrika deret waktu finansial (López de Prado, 2018):

### 3.1 Purging Matematis ($H=5$ Hari Kerja)
- **Definisi:** Menghapus observasi dari set latih yang memiliki *label target* yang tumpang tindih (*overlap*) dengan periode pengujian/validasi.
- **Rasionalitas Eksak:**
  Target pada hari $t$ dihitung menggunakan return harian pada interval $[t+1, t+5]$.
  Jika set validasi dimulai pada hari pertama bursa tahun 2022 ($T_{\text{val}} = \text{2022-01-03}$):
  - Observasi latih tanggal **2021-12-31**: Targetnya menggunakan return 3, 4, 5, 6, dan 7 Januari 2022 (**5 hari berada di dalam validasi**).
  - Observasi latih tanggal **2021-12-30**: Targetnya menggunakan return 31 Des, serta 3, 4, 5, dan 6 Januari 2022 (**4 hari di validasi**).
  - Observasi latih tanggal **2021-12-29**: Targetnya menggunakan return 3 hari di validasi.
  - Observasi latih tanggal **2021-12-28**: Targetnya menggunakan return 2 hari di validasi.
  - Observasi latih tanggal **2021-12-27**: Targetnya menggunakan return 1 hari di validasi (3 Januari 2022).
  - Observasi latih tanggal **2021-12-24**: Targetnya menggunakan return tanggal 27, 28, 29, 30, dan 31 Desember 2021 (**0 hari di validasi**).
- **Kesimpulan:** Panjang purging yang diwajibkan secara matematis adalah **tepat 5 hari perdagangan ($P = H = 5$)**. Menghapus 5 baris (27–31 Desember 2021) menjamin secara mutlak bahwa tidak ada satu pun observasi target training yang terkontaminasi oleh return dari periode validasi.

### 3.2 Mengapa Embargo 15 atau 30 Hari Tidak Dipilih Sembarangan?
- **Hakikat Embargo:** Embargo adalah jeda waktu tambahan yang diterapkan *setelah* periode pengujian (misalnya saat melakukan cross-validation lipat ganda) untuk mengatasi autokorelasi serial yang tersisa atau memori fitur.
- **Kausalitas Waktu Alami:** Pada pemisahan walk-forward searah di mana Training berada di masa lalu ($t \le 2021$) dan Validation berada di masa depan ($t \ge 2022$), informasi mengalir secara kausal dari masa lalu ke masa depan. Informasi masa lalu mempengaruhi masa depan adalah realitas ekonomi, bukan kebocoran data (*leakage*).
- **Efisiensi Informasi:** Memilih embargo arbitrer 15 atau 30 hari tanpa dasar matematis justru akan membuang observasi berharga di awal Januari 2022 tanpa memberikan perlindungan leakage tambahan. Purging $H=5$ hari telah 100% menyelesaikan masalah kebocoran label target.

---

## 4. Waktu Prediksi EOD $t$ & Keabsahan Fitur Historis Lintas Batas

Salah satu kesalahan pemahaman umum dalam machine learning deret waktu adalah menganggap bahwa penggunaan data historis sebelum batas split merupakan kebocoran data (*data leakage*). Evaluasi Checkpoint 2 menegaskan prinsip operasional berikut:

```
            Titik Potong Pemisahan (Cut-off Split: 2021-12-31)
                                      │
 ──[Set Latih: 2010 s/d 2021-12-24]───┼──[Set Validasi: 2022 s/d 2024]───> Waktu
                  │                   │       │
                  ▼                   │       ▼
       Target di-purge 5 hari         │    Hari Pertama Validasi (t = 2022-01-03)
      agar tidak menyeberang          │    • Target Y: return [Jan 4 .. Jan 10] (Masa Depan)
                                      │    • Fitur rv_past20: return [Des 6 .. Jan 3]
                                      │      (Fakta Sejarah, SUDAH OBSERVABLE saat EOD t)
```

1. **Ketersediaan Informasi EOD $t$:** Pada tanggal 3 Januari 2022 pukul 16:30 WIB (penutupan bursa hari pertama validasi), harga saham IHSG hari itu sudah terbentuk. Analis di dunia nyata memiliki akses penuh ke harga penutupan hari itu dan 19 hari sebelumnya (Desember 2021).
2. **Keabsahan Metodologis:** Menghitung fitur `rv_past20` pada tanggal 3 Januari 2022 dengan menarik harga dari bulan Desember 2021 adalah **SAH SECARA METODOLOGIS DAN BUKAN LEAKAGE**. Data tersebut berada di masa lalu ($< t$), bukan di masa depan ($> t$).
3. **Batas Leakage Sesungguhnya:** Leakage hanya terjadi jika:
   - Model menggunakan harga penutupan tanggal $> t$ (misal 4 Januari 2022 ke atas).
   - Target label masa depan dilibatkan dalam fitur.
   - Parameter standarisasi (`StandardScaler.fit()`) dipelajari dari data validasi atau uji.

---

## 5. Evaluasi Baseline Benchmarking & Hasil Numerik Komparatif

Seluruh model baseline dievaluasi pada periode validasi yang persis sama. Metrik yang digunakan adalah **Mean Absolute Error (MAE)**, **Root Mean Squared Error (RMSE)**, dan korelasi linier Pearson ($r$).

### 5.1 Parameter Fitting Baseline
- **Constant Mean:** $\bar{Y}_{\text{train}} = \mathbf{0,008802}$ (dihitung murni dari 3.125 baris `train_purged`).
- **Constant Median:** $\text{Median}(Y_{\text{train}}) = \mathbf{0,007452}$ (dihitung murni dari 3.125 baris `train_purged`).
- **Persistence Baselines:** Menggunakan nilai fitur historis yang tersedia pada hari $t$ (`rv_past5`, `rv_past10`, `rv_past20`).

### 5.2 Tabel Komparasi Kinerja Baseline

Tabel berikut menyajikan hasil numerik aktual yang dieksekusi dari notebook [`notebook/02_Validation_Baseline.ipynb`](file:///z:/Projects/Inception/notebook/02_Validation_Baseline.ipynb):

| Setup Evaluasi | Model / Baseline | MAE | RMSE | Pearson $r$ | Observasi Valid ($N$) | Peringkat MAE |
|---|---|---|---|---|---|---|
| **Validation Clean (2022–2024)** | **Persistence `rv_past20`** | **0,002675** | **0,003540** | **0,2197** | **772** | **1 (Terbaik)** |
| Validation Clean (2022–2024) | **Constant Median** | **0,002776** | **0,003392** | 0,0000 | 772 | 2 |
| Validation Clean (2022–2024) | Persistence `rv_past10` | 0,002791 | 0,003716 | 0,2259 | 772 | 3 |
| Validation Clean (2022–2024) | Persistence `rv_past5` (Naif Kompetisi) | 0,002981 | 0,004088 | 0,2077 | 772 | 4 |
| Validation Clean (2022–2024) | Constant Mean | 0,003455 | 0,003984 | 0,0000 | 772 | 5 (Terburuk) |
|---|---|---|---|---|---|---|
| *Validation All (2022–2024)* | *Persistence `rv_past20`* | *0,002687* | *0,003551* | *0,2191* | *777* | *1* |
| *Validation All (2022–2024)* | *Constant Median* | *0,002775* | *0,003390* | *0,0000* | *777* | *2* |
| *Validation All (2022–2024)* | *Persistence `rv_past10`* | *0,002796* | *0,003720* | *0,2242* | *777* | *3* |
| *Validation All (2022–2024)* | *Persistence `rv_past5`* | *0,003003* | *0,004118* | *0,1987* | *777* | *4* |
| *Validation All (2022–2024)* | *Constant Mean* | *0,003452* | *0,003981* | *0,0000* | *777* | *5* |

*Visualisasi komparasi grafik time-series dan diagram batang tersimpan di [`outputs/validation/fig_val_02_baseline_comparison.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_02_baseline_comparison.png).*

### 5.3 Analisis Ekonometrika & Temuan Kunci

1. **Fenomena Pergeseran Rezim (*Regime Shift*):**
   - Rata-rata target pada periode latih (2010–2021) adalah **$0,008802$** ($\sigma = 0,005947$, nilai maksimum $0,058497$ akibat krisis pandemi 2020).
   - Rata-rata target pada periode validasi (2022–2024) turun drastis menjadi **$0,006509$** ($\sigma = 0,003260$, nilai maksimum hanya $0,019745$).
   - **Dampak:** *Constant Mean* mengalami bias overprediksi konstan di seluruh rentang validasi, menjadikannya model dengan error MAE terburuk ($0,003455$).
2. **Ketahanan Constant Median:**
   - Karena distribusi target memiliki ekor kanan tebal (*fat-tailed*), *Constant Median* ($0,007452$) jauh lebih dekat ke pusat sebaran data validasi dibanding mean, sehingga menghasilkan error yang jauh lebih rendah ($\text{MAE} = 0,002776$, $\text{RMSE} = 0,003392$).
3. **Keunggulan Persistence Volatilitas 20-Hari (`rv_past20`):**
   - Di antara seluruh model persistensi, `rv_past20` keluar sebagai pemenang dengan $\text{MAE} = \mathbf{0,002675}$ dan $\text{RMSE} = \mathbf{0,003540}$.
   - Model naif kompetisi (`rv_past5`) menghasilkan error lebih tinggi ($\text{MAE} = 0,002981$, $\text{RMSE} = 0,004088$) karena jendela 5 hari terlalu sensitif terhadap guncangan harian sesaat (*noisy*), sedangkan `rv_past20` berhasil menangkap level varians lokal secara lebih stabil.

---

## 6. Evaluasi Tambahan: Expanding Window Walk-Forward (3 Folds)

Untuk membuktikan bahwa performa baseline bukan kebetulan pada satu pemotongan split saja, evaluasi *Expanding Window Walk-Forward* dijalankan melintasi 3 tahun validasi dengan urutan kronologis ketat:

### 6.1 Hasil Komparasi Lintas Lipatan (Fold 1, 2, 3)

| Fold | Periode Validasi | Jumlah Train (Purged) | Jumlah Val | Model Baseline | MAE | RMSE |
|---|---|---|---|---|---|---|
| **Fold 1** | **Tahun 2022** (Rezim Kenaikan Suku Bunga The Fed) | 3.125 | 260 | **Persistence `rv_past20`** | **0,002546** | 0,003625 |
| Fold 1 | Tahun 2022 | 3.125 | 260 | Constant Median | 0,002567 | **0,003312** |
| Fold 1 | Tahun 2022 | 3.125 | 260 | Persistence `rv_past10` | 0,002819 | 0,003849 |
| Fold 1 | Tahun 2022 | 3.125 | 260 | Constant Mean | 0,003041 | 0,003676 |
| Fold 1 | Tahun 2022 | 3.125 | 260 | Persistence `rv_past5` | 0,003078 | 0,004296 |
|---|---|---|---|---|---|---|
| **Fold 2** | **Tahun 2023** (Rezim Inflasi & Normalisasi Pasar) | 3.385 | 260 | **Persistence `rv_past10`** | **0,002194** | **0,002907** |
| Fold 2 | Tahun 2023 | 3.385 | 260 | Persistence `rv_past5` | 0,002255 | 0,002971 |
| Fold 2 | Tahun 2023 | 3.385 | 260 | Persistence `rv_past20` | 0,002265 | 0,002946 |
| Fold 2 | Tahun 2023 | 3.385 | 260 | Constant Median | 0,002960 | 0,003313 |
| Fold 2 | Tahun 2023 | 3.385 | 260 | Constant Mean | 0,003902 | 0,004256 |
|---|---|---|---|---|---|---|
| **Fold 3** | **Tahun 2024** (Rezim Rekor Tertinggi IHSG & Pemilu) | 3.645 | 252 | **Constant Median** | **0,002644** | **0,003459** |
| Fold 3 | Tahun 2024 | 3.645 | 252 | Constant Mean | 0,003137 | 0,003736 |
| Fold 3 | Tahun 2024 | 3.645 | 252 | Persistence `rv_past20` | 0,003232 | 0,003987 |
| Fold 3 | Tahun 2024 | 3.645 | 252 | Persistence `rv_past10` | 0,003377 | 0,004278 |
| Fold 3 | Tahun 2024 | 3.645 | 252 | Persistence `rv_past5` | 0,003628 | 0,004801 |

### 6.2 Rata-rata Kinerja Walk-Forward Lintas 3 Lipatan

| Peringkat | Model / Baseline | Rata-rata MAE (3 Folds) | Rata-rata RMSE (3 Folds) | Catatan Metodologis |
|---|---|---|---|---|
| **1** | **Persistence `rv_past20`** | **0,002681** | 0,003519 | **Paling stabil dan adaptif** terhadap transisi rezim tahunan. |
| **2** | **Constant Median** | **0,002724** | **0,003361** | Menghasilkan RMSE rata-rata terendah. |
| **3** | Persistence `rv_past10` | 0,002797 | 0,003678 | Unggul di tahun 2023 saat volatilitas rendah stabil. |
| **4** | Persistence `rv_past5` | 0,002987 | 0,004023 | Terlalu fluktuatif di tahun 2022 dan 2024. |
| **5** | Constant Mean | 0,003360 | 0,003889 | Paling terdistorsi oleh outlier krisis masa lalu. |

*Visualisasi grafik batang stabilitas walk-forward tersimpan di [`outputs/validation/fig_val_03_walk_forward_metrics.png`](file:///z:/Projects/Inception/outputs/validation/fig_val_03_walk_forward_metrics.png).*

---

## 7. Hasil Pemeriksaan Kepatuhan Anti-Leakage Otomatis

Seluruh pipeline validasi telah melewati 6 pengujian otomatis (*automated assertions*) yang tercantum pada notebook Section 7:

```
=================================================================
HASIL PEMERIKSAAN KEPATUHAN & INTEGRITAS ANTI-LEAKAGE
=================================================================
[PASS] Check 1: Urutan Waktu Monotonik
       Train Max (2021-12-24) < Val Min (2022-01-03) < Val Max (2024-12-17) < Test Min (2025-01-02)
[PASS] Check 2: Isolasi Target Validasi dari Fitting Baseline
       Fit Mean Train (0.008802) != Val Mean (0.006509)
[PASS] Check 3: Isolasi Data Uji Kompetisi
       100% Target pada test set bernilai NaN (359/359 baris, tidak pernah disentuh)
[PASS] Check 4: Verifikasi Purge Sesuai Horizon Target H=5
       Tepat 5 hari bursa (2021-12-27 s/d 2021-12-31) di-purge dari set latih
[PASS] Check 5: Isolasi Fitur Prediktor dari Target
       29 fitur prediktor terkonfirmasi bebas dari kolom Target_Volatilitas_Y
[PASS] Check 6: Kausalitas Ketersediaan EOD t
       Seluruh fitur terverifikasi hanya memanfaatkan data historis <= t
=================================================================
STATUS: SELURUH 6 PEMERIKSAAN KEPATUHAN DINYATAKAN PASS! [VERIFIED]
=================================================================
```

---

## 8. Keterbatasan & Keputusan Strategis Menuju Task 3 (Modeling)

### 8.1 Keterbatasan Metodologis yang Harus Diakui
1. **Keterbatasan Model Baseline:**
   Seluruh model baseline bersifat univariat atau konstan. Model ini tidak memperhitungkan sinyal makroekonomi eksternal seperti kepanikan global (`VIX`), tekanan nilai tukar (`USDIDR`), selisih suku bunga (`rate_differential`), maupun guncangan harga minyak (`OIL`).
2. **Ketergantungan Rezim:**
   Pergeseran rezim dari era volatilitas tinggi 2020 menuju era normalisasi 2022–2024 membuktikan bahwa model yang mengandalkan rata-rata global akan gagal. Model Machine Learning pada Task 3 harus mampu mengidentifikasi rezim volatilitas secara adaptif.

### 8.2 Ambang Batas Performa (*Benchmark Hurdle*) untuk Task 3
Untuk membuktikan bahwa solusi Machine Learning (LightGBM / Tree Ensembles) yang dibangun pada Task 3 memang memberikan nilai tambah nyata bagi PT Investion, model tersebut **wajib mengalahkan performa baseline terbaik**:

$$\mathbf{\text{Target Ambang Batas Task 3:}} \quad \text{MAE} < \mathbf{0,002675} \quad \text{dan} \quad \text{RMSE} < \mathbf{0,003392}$$

Jika model Machine Learning gagal melampaui angka tersebut, maka model dinyatakan mengalami overfitting atau terdistorsi oleh noise pasar.

### 8.3 Keputusan Pipeline Teknis yang Wajib Diterapkan di Task 3:
1. **Gunakan Skema Purged TimeSeriesSplit:** Lakukan cross-validation lipatan ganda dengan purge $H=5$ di setiap batas train-val.
2. **Bungkus Standarisasi dalam Pipeline:** Pastikan modul `StandardScaler` atau normalisasi apapun dioperasikan melalui `sklearn.pipeline.Pipeline` agar parameter $\mu$ dan $\sigma$ hanya dipelajari dari set latih lipatan terkait.
3. **Optimasi Loss Function:** Mengingat target bersifat *fat-tailed*, optimasikan model menggunakan loss function yang tangguh terhadap outlier (Huber Loss / L1 MAE objective).

> **Penyelesaian Checkpoint 2:** Tidak ada pelatihan model Machine Learning lanjutan, hyperparameter tuning, pembuatan SHAP, atau inferensi test set pada tahap ini sesuai batasan SOP kompetisi.
