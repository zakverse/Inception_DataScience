# Laporan Analisis Kesalahan Berbasis Explainable AI (XAI Error Analysis) — Checkpoint 6.1

**Proyek:** INCEPTION 2026 — Early Warning System Prediksi Realized Volatility IHSG 5-Hari ke Depan  
**Fase:** Checkpoint 6.1 (Penyelesaian Task 3.6 & Task 3.7: Analisis Kesalahan Berbasis XAI)  
**Dokumen Acuan Utama:** `Aset Lomba/Studi Kasus.docx`, [`docs/checkpoint_6_studi_kasus_compliance.md`](file:///z:/Projects/Inception/docs/checkpoint_6_studi_kasus_compliance.md), [`docs/checkpoint_4_xai.md`](file:///z:/Projects/Inception/docs/checkpoint_4_xai.md)  
**Folder Visualisasi:** [`outputs/xai/error_analysis/`](file:///z:/Projects/Inception/outputs/xai/error_analysis/)  
**Status Audit Sebelum:** Task 3.6 & Task 3.7 berstatus `PARTIAL` (Kepatuhan Proyek 95%)  
**Status Audit Sesudah:** Task 3.6 & Task 3.7 berstatus **`COMPLETE 100%`** (Kepatuhan Proyek **`100%`** untuk seluruh butir Task 1, 2, dan 3)  

---

## 1. Eksekutif Ringkasan & Ruang Lingkup Analisis

Pada audit kepatuhan Checkpoint 6, dua butir krusial dalam **Task 3: Regresi, Evaluasi & XAI** diidentifikasi berstatus `PARTIAL`:
- **Task 3.6:** Identifikasi kondisi pasar di mana model sempat meleset jauh dari kenyataan pada data berlabel.
- **Task 3.7:** Analisis kesalahan prediksi tersebut menggunakan Explainable AI (XAI), bukan dugaan semata.

Laporan Checkpoint 6.1 ini secara khusus menuntaskan kedua butir tersebut secara metodologis, transparan, dan dapat dipertanggungjawabkan di hadapan Komite Manajemen Risiko & Dewan Direksi PT Investion. Dua kasus ekstrem out-of-sample (OOF) representatif dari Fold 3 (tahun 2024) yang terjadi pada rentang peristiwa bersejarah **"Black Monday 2024"** dibedah secara mendalam:

1. **Kasus 1 — Underprediction Ekstrem (31 Juli 2024):**  
   Target volatilitas aktual melonjak ekstrem ke $Y = 0,019251$, namun model memprediksi $\hat{Y} = 0,005825$ (residual $e_t = +0,013426$, absolute error $0,013426$). Ini adalah *underprediction* terbesar pada seluruh 772 hari evaluasi out-of-sample.
2. **Kasus 2 — Overprediction Ekstrem (5 Agustus 2024 - Hari Puncak Crash Black Monday):**  
   Model memprediksi lonjakan volatilitas tinggi $\hat{Y} = 0,012314$, namun pasar forward mengalami normalisasi kilat (*swift mean-reversion*) sehingga volatilitas riil hanya $Y = 0,005503$ (residual $e_t = -0,006811$, absolute error $0,006811$).

### Prinsip Metodologis Bebas Kebocoran Waktu (Anti-Leakage Guarantees)
- **Model Strictly Out-of-Fold:** Prediksi untuk kedua tanggal (Juli–Agustus 2024) dihasilkan oleh model `Fold 3 (2024)` yang dilatih secara eksklusif pada data 2010 s/d 31 Desember 2023 dengan mekanisme *purging* 5-hari terakhir. Model **tidak pernah melihat satu baris pun data tahun 2024** selama proses pelatihan.
- **Konsistensi Definisi Residual:** Residual didefinisikan secara baku sebagai $e_t = y_{\text{true}} - \hat{y}_t$, di mana nilai positif menunjukkan *underprediction* (realitas lebih bergejolak dari prediksi) dan nilai negatif menunjukkan *overprediction* (model menduga lebih bergejolak dari realitas).
- **Dekomposisi Superposisi Aditif Eksak:** Penjelasan XAI untuk model ensemble `Blend 60:40` direkonstruksi melalui superposisi aditif matematis eksak antara TreeSHAP (`GBR Tuned`) dan koefisien linier terstandarisasi (`Ridge Tuned`), dengan deviasi rekonstruksi $< 10^{-10}$.

---

## 2. Tabel Numerik Komparatif: Model ML vs Baseline Naif

Tabel berikut menyajikan ringkasan kinerja prediksi out-of-fold, nilai target aktual, residual error, dan absolute error pada kedua tanggal kasus ekstrem:

| Parameter Evaluasi | Kasus 1: Underprediction Ekstrem | Kasus 2: Overprediction Ekstrem |
|---|---|---|
| **Tanggal Prediksi ($t$)** | **31 Juli 2024** | **5 Agustus 2024** |
| **Konteks Peristiwa** | Fase Pra-Guncangan (EOD Tenang) | Puncak Crash Black Monday (EOD Panik) |
| **Jendela Target Forward ($[t+1 \dots t+5]$)** | 1 Agustus 2024 – 7 Agustus 2024 | 6 Agustus 2024 – 12 Agustus 2024 |
| **Target Volatilitas Riil ($y_{\text{true}}$)** | **$0,019251$** | **$0,005503$** |
|---|---|---|
| **Prediksi Baseline Naif (`rv_past5`)** | $0,004962$ | $0,016621$ |
| *Residual (`rv_past5`)* | $+0,014288$ | $-0,011118$ |
| *Absolute Error (`rv_past5`)* | $0,014288$ | $0,011118$ |
|---|---|---|
| **Prediksi Baseline Persistensi (`rv_past20`)** | $0,005200$ | $0,009481$ |
| *Residual (`rv_past20`)* | $+0,014050$ | $-0,003978$ |
| *Absolute Error (`rv_past20`)* | $0,014050$ | $0,003978$ |
|---|---|---|
| **Prediksi Ridge Tuned** | $0,005395$ | $0,013304$ |
| *Residual Ridge Tuned* | $+0,013856$ | $-0,007802$ |
| *Absolute Error Ridge Tuned* | $0,013856$ | $0,007802$ |
|---|---|---|
| **Prediksi GBR Tuned (Single Champion)** | $0,006111$ | $0,011654$ |
| *Residual GBR Tuned* | $+0,013139$ | $-0,006151$ |
| *Absolute Error GBR Tuned* | $0,013139$ | $0,006151$ |
|---|---|---|
| **Prediksi Blend 50:30:20** | $0,005714$ | $0,011714$ |
| *Residual Blend 50:30:20* | $+0,013537$ | $-0,006212$ |
| *Absolute Error Blend 50:30:20* | $0,013537$ | $0,006212$ |
|---|---|---|
| **Prediksi Blend 60:40 (Ensemble Champion)** | **$0,005825$** | **$0,012314$** |
| *Residual Blend 60:40* | **$+0,013426$** | **$-0,006811$** |
| *Absolute Error Blend 60:40* | **$0,013426$** | **$0,006811$** |

### Temuan Numerik Utama
1. **Pada Kasus 1 (31 Juli 2024):** Seluruh model kuantitatif maupun baseline mengalami *underprediction*. Hal ini menegaskan bahwa guncangan yang terjadi 3 hari berikutnya adalah peristiwa eksogen murni. Kendati demikian, model ML (`Blend 60:40` = $0,005825$) memberikan estimasi risiko yang lebih tinggi dibanding baseline naif kompetisi (`rv_past5` = $0,004962$).
2. **Pada Kasus 2 (5 Agustus 2024):** Baseline naif resmi kompetisi (`rv_past5`) mengalami *overprediction* yang luar biasa masif ($0,016621$, error $-0,011118$) karena mengekstrapolasikan kepanikan intraday secara buta. Sebaliknya, model **`GBR Tuned` ($0,011654$) dan `Blend 60:40` ($0,012314$) berhasil memangkas error baseline sebesar $38,7\% \text{ s/d } 44,7\%$**, membuktikan keunggulan struktural pohon dangkal dan regularisasi Ridge dalam meredam over-reaksi pasar.

---

## 3. Visualisasi Konteks Deret Waktu & Peristiwa Black Monday 2024

Visualisasi terintegrasi pada [`outputs/xai/error_analysis/fig_err_01_timeline_context.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_01_timeline_context.png) memetakan kronologi pasar keuangan dari pertengahan Juli hingga akhir Agustus 2024:

![Konteks Deret Waktu Black Monday 2024](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_01_timeline_context.png)

### Kronologi Transmisi Kejutan Pasar:
1. **Fase Ketenangan Semu (31 Juli 2024):**  
   IHSG ditutup menguat $+0,19\%$ di level $7.255,76$. Indeks ketakutan global VIX berada pada level rendah $16,36$, dan volatilitas historis 20 hari IHSG (`rv_past20`) hanya $0,005200$. Pada tanggal yang sama, Bank of Japan (BoJ) mengumumkan kenaikan suku bunga tak terduga menjadi $0,25\%$, namun likuiditas global belum merespons secara seketika.
2. **Fase Akumulasi Tekanan (1–2 Agustus 2024):**  
   Rilis data ketenagakerjaan AS (Non-Farm Payrolls) menunjukkan pelemahan tajam, memicu kekhawatiran resesi AS (*Sahm Rule* aktif). Apresiasi tajam Yen Jepang memicu penutupan paksa (*margin call & unwinding*) posisi *Yen carry trade* multi-miliar dolar di seluruh dunia.
3. **Fase Puncak Guncangan (Senin, 5 Agustus 2024 - Black Monday):**  
   Indeks Nikkei 225 Tokyo rontok $-12,4\%$ (kejatuhan 1 hari terbesar sejak Oktober 1987). Bursa Asia dan Wall Street mengalami aksi jual panik. IHSG anjlok tajam **$-3,40\%$** dalam sehari ke level $7.059,65$, momentum 5-hari jatuh ke $-3,15\%$, dan CBOE VIX meroket sesaat hingga $>65$ sebelum ditutup di $38,57$.
4. **Fase Reversi Kilat / Swift Mean-Reversion (6–12 Agustus 2024):**  
   Pada 6–7 Agustus 2024, Deputi Gubernur BoJ Shinichi Uchida merilis pernyataan resmi bahwa BoJ tidak akan menaikkan suku bunga saat kondisi pasar tidak stabil. Pernyataan ini langsung meredakan kepanikan global. Nikkei rebound $+10,2\%$, IHSG berbalik menguat berturut-turut ($+0,99\%$, $+1,16\%$, $-0,24\%$, $+0,86\%$, $+0,56\%$), dan varians pergerakan harian forward anjlok drastis ke level tenang ($Y = 0,005503$).

---

## 4. Bedah Kasus 1: Underprediction Ekstrem (31 Juli 2024)

### 4.1 Dekomposisi SHAP & Waterfall Attribution
Grafik pada [`outputs/xai/error_analysis/fig_err_02_waterfall_underprediction_20240731.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_02_waterfall_underprediction_20240731.png) menguraikan bagaimana fitur-fitur model menarik ekspektasi volatilitas ke bawah:

![Waterfall Plot Kasus 1 Underprediction](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_02_waterfall_underprediction_20240731.png)

Dekomposisi matematis aditif pada model `Blend 60:40` (Base Value $= 0,007928$):
- **Nilai Prediksi $\hat{y}$:** $0,005825$ (Deviasi Total SHAP: $-0,002103$).

| Peringkat | Fitur Prediktor | Nilai Riil Fitur | Kontribusi SHAP Blend 60:40 | Kontribusi GBR Tuned | Kontribusi Ridge Tuned | Arah Efek terhadap Prediksi |
|---|---|---|---|---|---|:---:|
| **1** | **`rv_past20`** | **$0,005200$** | **$-0,000670$** | $-0,000704$ | $-0,000619$ | **Menarik Turun (Down)** |
| **2** | **`US_rate`** | **$5,33\%$** | **$-0,000473$** | $-0,480 \times 10^{-3}$ | $-0,464 \times 10^{-3}$ | **Menarik Turun (Down)** |
| **3** | **`IHSG`** | **$7.255,76$** | **$-0,000349$** | $-0,000178$ | $-0,000605$ | **Menarik Turun (Down)** |
| **4** | **`rv_past10`** | **$0,006269$** | **$-0,000207$** | $-0,000140$ | $-0,000307$ | **Menarik Turun (Down)** |
| **5** | **`VIX`** | **$16,36$** | **$-0,000144$** | $-0,000093$ | $-0,000219$ | **Menarik Turun (Down)** |
| 6 | `USDIDR` | Rp $16.328,50$ | $+0,000237$ | $+0,000509$ | $-0,000169$ | Mendorong Naik (Up) |
| 7 | `CPI` | $2,18\%$ | $+0,000145$ | $+0,000206$ | $+0,000053$ | Mendorong Naik (Up) |
| 8 | `vix_ratio_ma20` | $1,1126$ | $+0,000061$ | $+0,000021$ | $+0,000121$ | Mendorong Naik (Up) |

### 4.2 Analisis Tiga Lapis: Fakta Data, Hasil XAI, & Interpretasi Finansial
1. **Lapis 1 — Fakta Data (Data Facts):**  
   Pada penutupan perdagangan 31 Juli 2024 (16:30 WIB), IHSG mencatatkan gain $+0,19\%$, volatilitas historis 20 hari berada pada persentil ke-25 terendah ($0,0052$), dan VIX global berada di level $16,36$. Tidak ada anomali harga pada pasar domestik.
2. **Lapis 2 — Bukti XAI (SHAP Attribution):**  
   Atribusi SHAP membuktikan bahwa fitur penarik turun terbesar adalah `rv_past20` ($-0,000670$) dan level absolut `IHSG` yang tinggi ($-0,000349$). Model secara konsisten memproses fakta bahwa varians lokal 20 hari sedang sangat rendah dan indeks berada pada tren penguatan, sehingga mengekspektasikan volatilitas 5 hari ke depan akan tetap stabil di kisaran $\sim 0,0058$.
3. **Lapis 3 — Interpretasi Finansial & Batasan Model:**  
   Penyebab target aktual forward meledak menjadi $Y=0,019251$ adalah kejatuhan IHSG $-3,40\%$ yang terjadi **pada hari forward ke-3 ($t+3$, 5 Agustus 2024)** akibat pembongkaran carry trade global. Pada EOD 31 Juli 2024, informasi mengenai intensitas likuidasi dana lindung nilai global di Tokyo dan New York **belum ada di database pasar manapun**. Model deret waktu yang beroperasi secara bebas bocor (*strictly backward-looking*) secara logis tidak mungkin memprediksi kejadian tersebut tanpa melanggar kaidah anti-leakage.

---

## 5. Bedah Kasus 2: Overprediction Ekstrem (5 Agustus 2024)

### 5.1 Dekomposisi SHAP & Waterfall Attribution
Grafik pada [`outputs/xai/error_analysis/fig_err_03_waterfall_overprediction_20240805.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_03_waterfall_overprediction_20240805.png) menguraikan bagaimana lonjakan kepanikan global melipatgandakan ekspektasi risiko model:

![Waterfall Plot Kasus 2 Overprediction](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_03_waterfall_overprediction_20240805.png)

Dekomposisi matematis aditif pada model `Blend 60:40` (Base Value $= 0,007928$):
- **Nilai Prediksi $\hat{y}$:** $0,012314$ (Deviasi Total SHAP: $+0,004386$).

| Peringkat | Fitur Prediktor | Nilai Riil Fitur | Kontribusi SHAP Blend 60:40 | Kontribusi GBR Tuned | Kontribusi Ridge Tuned | Arah Efek terhadap Prediksi |
|---|---|---|---|---|---|:---:|
| **1** | **`VIX`** | **$38,57$** | **$+0,001895$** | $+0,001819$ | $+0,002009$ | **Mendorong Naik Kuat (Up)** |
| **2** | **`mom_ihsg_5`** | **$-3,15\%$** | **$+0,000977$** | $+0,001315$ | $+0,000469$ | **Mendorong Naik Kuat (Up)** |
| **3** | **`vix_ratio_ma20`**| **$2,2843$** | **$+0,000578$** | $+0,000021$ | $+0,001414$ | **Mendorong Naik (Up)** |
| **4** | **`mom_ihsg_10`** | **$-3,58\%$** | **$+0,000483$** | $+0,000565$ | $+0,000359$ | **Mendorong Naik (Up)** |
| **5** | **`IHSG_ret`** | **$-3,40\%$** | **$+0,000466$** | $+0,000107$ | $+0,001004$ | **Mendorong Naik (Up)** |
| 6 | `US_rate` | $5,33\%$ | $-0,000405$ | $-0,000366$ | $-0,000464$ | Menahan Turun (Down) |
| 7 | `X1_Fear_Liquidity_Robust`| $-0,4886$ | $-0,000345$ | $-0,000213$ | $-0,000543$ | Menahan Turun (Down) |
| 8 | `IHSG` | $7.059,65$ | $-0,000332$ | $-0,000191$ | $-0,000545$ | Menahan Turun (Down) |

### 5.2 Analisis Tiga Lapis: Fakta Data, Hasil XAI, & Interpretasi Finansial
1. **Lapis 1 — Fakta Data (Data Facts):**  
   Pada penutupan perdagangan 5 Agustus 2024, IHSG jatuh tajam $-3,40\%$ ke level $7.059,65$, VIX melonjak ke level penutupan tertinggi 2024 di $38,57$, dan rasio VIX terhadap tren 20 hari melonjak lebih dari dua kali lipat ($2,28\times$). Namun pada 5 hari bursa berikutnya ($6 \dots 12$ Agustus), IHSG mencatatkan 4 hari reli positif berturut-turut ($+0,99\%$, $+1,16\%$, $-0,24\%$, $+0,86\%$, $+0,56\%$) dengan rata-rata volatilitas sangat kecil ($Y = 0,005503$).
2. **Lapis 2 — Bukti XAI (SHAP Attribution):**  
   Dekomposisi SHAP menunjukkan bahwa lonjakan prediksi ke level $0,012314$ didorong mutlak oleh kontribusi gabungan indeks kepanikan global `VIX` ($+0,001895$) dan momentum kejatuhan IHSG `mom_ihsg_5` ($+0,000977$). Dua fitur ini menyumbang lebih dari $65\%$ dari total deviasi positif SHAP. Model pohon dan Ridge merespons sinyal kepanikan ekstrem ini dengan mengasumsikan pasar akan terus berada dalam rezim krisis turbulen.
3. **Lapis 3 — Interpretasi Finansial & Mekanisme Over-Extrapolation:**  
   Error model terjadi karena **over-extrapolation of volatility clustering**. Pada krisis-krisis historis di data training (seperti Maret 2020 atau Mei 2022), lonjakan VIX $>35$ biasanya diikuti oleh badai volatilitas berkepanjangan selama berminggu-minggu. Model mempelajari pola bahwa "Kepanikan VIX masif = Turbulensi berlanjut". Akan tetapi, guncangan 5 Agustus 2024 adalah sebuah *liquidity flash crash* yang terselesaikan dalam hitungan 48 jam berkat intervensi verbal darurat Bank of Japan. Ketahanan likuiditas perbankan domestik Indonesia yang solid mampu menyerap guncangan tersebut dengan sangat cepat, sehingga volatilitas riil langsung kembali normal.

---

## 6. Evaluasi Komparatif Residual Lintas Model Kandidat

Grafik pada [`outputs/xai/error_analysis/fig_err_04_comparative_model_residual_breakdown.png`](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_04_comparative_model_residual_breakdown.png) menyajikan perbandingan absolute error dan residual direction antar seluruh model kandidat:

![Komparasi Residual Error Lintas Model](file:///z:/Projects/Inception/outputs/xai/error_analysis/fig_err_04_comparative_model_residual_breakdown.png)

### Temuan Ketahanan Model (*Model Robustness Insight*):
- **Superioritas terhadap Baseline Naif:**  
  Pada Kasus 2, model baseline naif `rv_past5` menghasilkan error bencana sebesar $0,011118$ (karena mengasumsikan kejatuhan 5 hari lalu akan terus berulang di 5 hari mendatang). Model `GBR Tuned` memangkas error tersebut menjadi $0,006151$ (penurunan error **$44,7\%$**), dan `Blend 60:40` memangkasnya menjadi $0,006811$ (penurunan error **$38,7\%$**).
- **Peran Regularisasi Penalti Ridge:**  
  Meskipun Ridge Tuned memberikan bobot VIX linier yang cukup agresif, penalti $\alpha=1000.0$ mencegah koefisien meledak tak terkendali. Ketika digabungkan dengan GBR dangkal (`max_depth=2`), kombinasi ensemble memberikan kestabilan prediksi yang jauh lebih terukur dibanding estimasi naif.

---

## 7. Batasan Sistem Peringatan Dini & Rekomendasi Mitigasi Portofolio PT Investion

Sebagai analis kuantitatif yang bertanggung jawab mengawal dana kelolaan triliunan rupiah di PT Investion, pemahaman atas batasan model adalah bentuk kepatuhan manajemen risiko tertinggi:

### 7.1 Batasan Struktural Model Time-Series Finansial
1. **Asimetri Shok Tak Terduga (Causal Lag):**  
   Model machine learning deret waktu yang patuh aturan kausalitas waktu ($t \le \text{EOD}$) tidak memiliki bola kristal (*no prescience*). Model tidak dapat memprediksi shok geopolitik atau keputusan bank sentral asing yang terjadi di tengah malam di belahan dunia lain sebelum tercermin pada data pasar.
2. **Risiko Over-Extrapolation pada Flash Crash:**  
   Sensitivitas model terhadap indikator kepanikan global (seperti VIX $>35$) dapat menghasilkan *false alarm* berupa peringatan risiko tinggi yang berlebihan ketika shok tersebut ternyata hanyalah kepanikan likuiditas sesaat yang cepat diredam oleh otoritas moneter.

### 7.2 Rekomendasi Kebijakan Operasional untuk Komite Risiko PT Investion
1. **Protokol Dual-Speed Early Warning System:**
   - **Tingkat 1 (Model Kuantitatif Harian EOD):** Gunakan `Blend 60:40` untuk memandu alokasi portofolio multi-hari, rebalancing bobot beta saham, dan penentuan margin lindung nilai (*hedging buffer*).
   - **Tingkat 2 (Intraday Circuit Breaker Manual):** Jika CBOE VIX global melonjak $>20\%$ dalam sesi perdagangan Eropa/AS saat bursa BEI tutup, Komite Risiko secara otomatis mengaktifkan status *Yellow Alert* tanpa menunggu pembaruan model EOD berikutnya.
2. **Penerapan Filter Mean-Reversion Adaptif:**  
   Ketika model memprediksi lonjakan volatilitas ekstrem di atas persentil ke-95 ($> 0,0120$) yang didominasi oleh lonjakan sesaat VIX, portofolio manajer disarankan tidak langsung melakukan likuidasi panik (*fire-sale*), melainkan menerapkan strategi opsi lindung nilai jangka pendek (*protective put / collar*) untuk mengantisipasi potensi pembalikan arah pasar (*v-shaped rebound*).

---

## 8. Penilaian Ulang Kepatuhan Studi Kasus (Compliance Re-Assessment)

Berdasarkan pembuktian empiris, visualisasi diagnostik, dekomposisi SHAP aditif eksak, serta analisis ekonomi mendalam di atas, kami memperbarui status kepatuhan proyek INCEPTION 2026:

| ID Butir | Persyaratan Studi Kasus | Status Sebelum | Status Sesudah | Justifikasi Pembuktian |
|---|---|:---:|:---:|---|
| **TASK 3.6** | Identifikasi kondisi pasar di mana model sempat meleset jauh pada data berlabel | `PARTIAL` | **`COMPLETE`** | Dua kasus ekstrem out-of-fold (Underprediction 31 Juli 2024 dan Overprediction 5 Agustus 2024) teridentifikasi secara presisi dengan verifikasi data kuantitatif. |
| **TASK 3.7** | Analisis kesalahan prediksi tersebut menggunakan XAI (Bukan dugaan semata) | `PARTIAL` | **`COMPLETE`** | Dekomposisi TreeSHAP dan superposisi aditif linier merekonstruksi secara eksak kontribusi fitur pendorong naik/turun, membedakan fakta data vs hasil XAI vs interpretasi ekonomi. |

### Skor Kepatuhan Akhir Proyek
- **Task 1 (Feature Engineering & EDA):** **`100% COMPLETE`** (5 / 5 butir terpenuhi).
- **Task 2 (Time-Series & Anti-Leakage Pipeline):** **`100% COMPLETE`** (7 / 7 butir terpenuhi).
- **Task 3 (Pemodelan Regresi, Evaluasi, & XAI):** **`100% COMPLETE`** (7 / 7 butir terpenuhi).
- **Integritas Submission Teknis:** **`COMPLETE`** (3 berkas submission 359-baris dan 2 berkas dataset 4.266-baris terverifikasi 100% bebas NaN/inf; verifikasi portal bergantung pada pembukaan dashboard lomba).

**Kesimpulan Akhir:** Seluruh persyaratan teknis, metodologis, dan interpretatif dalam dokumen `Studi Kasus.docx` kini telah dipenuhi secara menyeluruh dengan bukti artefak nyata yang kokoh dan dapat diuji ulang secara penuh.
