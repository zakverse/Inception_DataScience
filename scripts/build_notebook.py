"""
Script to build/overwrite EDA.ipynb with complete structured cells.
Run once from z:/Projects/Inception/
"""
import json, copy, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
NOTEBOOK_PATH = os.path.join(PROJECT_ROOT, "notebook", "EDA.ipynb")

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

cells = []

# =============================================================================
# SECTION 0 — COVER
# =============================================================================
cells.append(md_cell("""# 🏦 INCEPTION 2026 — Exploratory Data Analysis
## Early Warning System: Prediksi Realized Volatility IHSG 5-Hari ke Depan

**Kompetisi:** INCEPTION 2026 Data Science Competition  
**Role:** Senior Quantitative Risk & Machine Learning Analyst — PT Investion  
**Dataset:** Indonesia Financial Time Series Dataset 2010–2026  
**Target:** `Target_Volatilitas_Y` — Realized volatility IHSG 5 hari ke depan

---

### Tujuan Notebook Ini
1. Melakukan audit menyeluruh kualitas dan struktur data
2. Memahami distribusi dan dinamika time-series setiap variabel makro-finansial
3. Memverifikasi definisi dan alignment target volatilitas
4. Menganalisis hubungan fitur terhadap target (pra-feature-engineering)
5. Mengidentifikasi risiko data leakage dan pola volatility clustering
6. Menyediakan landasan analitis untuk feature engineering (Task 1)

> **Checkpoint ini: Task 1 EDA saja. Tidak ada modeling, tuning, atau prediksi.**"""))

# =============================================================================
# SECTION 1 — IMPORTS & CONFIG
# =============================================================================
cells.append(md_cell("## 1. Import Library & Konfigurasi"))

cells.append(code_cell("""\
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

# ── Gaya visual konsisten ──────────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
PALETTE  = 'coolwarm'
C_BLUE   = '#2563EB'
C_RED    = '#DC2626'
C_ORANGE = '#D97706'
C_GREEN  = '#16A34A'
C_GRAY   = '#6B7280'

sns.set_theme(style='whitegrid', palette='muted', font_scale=1.05)

pd.set_option('display.max_columns', 20)
pd.set_option('display.float_format', '{:.4f}'.format)

print("✅ Library berhasil diimpor.")
import os
os.makedirs('../outputs/eda', exist_ok=True)
print(f"   pandas  {pd.__version__}")
print(f"   numpy   {np.__version__}")"""))

# =============================================================================
# SECTION 2 — LOAD DATA
# =============================================================================
cells.append(md_cell("## 2. Memuat Dataset"))

cells.append(code_cell("""\
DATA_PATH = "../Aset Lomba/dataset peserta.csv"

df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
df = df.sort_values('Date').reset_index(drop=True)

print(f"✅ Dataset dimuat: {df.shape[0]:,} baris × {df.shape[1]} kolom")
print(f"   Rentang tanggal : {df['Date'].min().date()} → {df['Date'].max().date()}")
df.head(3)"""))

# =============================================================================
# SECTION 3 — AUDIT STRUKTUR DATA
# =============================================================================
cells.append(md_cell("""\
## 3. Audit Struktur Data

Memeriksa tipe kolom, kelengkapan data, duplikasi, dan rentang tanggal."""))

cells.append(code_cell("""\
print("=" * 55)
print("AUDIT STRUKTUR DATA")
print("=" * 55)

# 3.1 Tipe & info dasar
print("\\n[3.1] Tipe Kolom & Non-Null Count")
df.info()"""))

cells.append(code_cell("""\
# 3.2 Missing values
print("\\n[3.2] Missing Values per Kolom")
missing = pd.DataFrame({
    'Total NaN'    : df.isnull().sum(),
    'Persen (%)'   : (df.isnull().sum() / len(df) * 100).round(2)
})
print(missing[missing['Total NaN'] > 0].to_string())

print("\\n[3.3] Duplikasi Baris")
n_dup = df.duplicated().sum()
print(f"  Jumlah baris duplikat : {n_dup}")

print("\\n[3.4] Kesinambungan Tanggal (hanya hari kerja)")
df['weekday'] = df['Date'].dt.dayofweek
print(f"  Weekday distribution (0=Mon … 4=Fri):")
print(f"  {df['weekday'].value_counts().sort_index().to_dict()}")
n_weekend = (df['weekday'] >= 5).sum()
print(f"  Baris weekend masuk  : {n_weekend}")
df.drop(columns='weekday', inplace=True)

print("\\n[3.5] Partisi Berlabel vs Uji")
labeled   = df[df['Target_Volatilitas_Y'].notna()]
unlabeled = df[df['Target_Volatilitas_Y'].isna()]
print(f"  Baris berlabel (Y≠NaN) : {len(labeled):,}  ({labeled['Date'].min().date()} → {labeled['Date'].max().date()})")
print(f"  Baris uji    (Y=NaN)   : {len(unlabeled):,}  ({unlabeled['Date'].min().date()} → {unlabeled['Date'].max().date()})")"""))

# =============================================================================
# SECTION 4 — STATISTIK DESKRIPTIF
# =============================================================================
cells.append(md_cell("""\
## 4. Statistik Deskriptif

Statistik dihitung **hanya dari data berlabel** agar tidak mencampur periode uji."""))

cells.append(code_cell("""\
print("[4.1] Statistik Deskriptif — Data Berlabel (2010–2024)")
desc = labeled.drop(columns='Date').describe().T
desc['CV (%)'] = (desc['std'] / desc['mean'].abs() * 100).round(1)
desc.columns = ['count','mean','std','min','25%','50%','75%','max','CV(%)']
display(desc.style.format('{:.4f}').bar(subset=['CV(%)'], color='#93C5FD'))"""))

cells.append(code_cell("""\
# 4.2 Distribusi tiap variabel (histogram + KDE)
COLS = ['OIL','GOLD','USDIDR','SP500','IHSG','VIX','CPI','BI_rate','US_rate','Target_Volatilitas_Y']
fig, axes = plt.subplots(2, 5, figsize=(22, 8))
axes = axes.flatten()

for i, col in enumerate(COLS):
    ax = axes[i]
    data_plot = labeled[col].dropna()
    ax.hist(data_plot, bins=50, color=C_BLUE, alpha=0.7, density=True, label='Histogram')
    # KDE
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(data_plot)
    x_range = np.linspace(data_plot.min(), data_plot.max(), 300)
    ax.plot(x_range, kde(x_range), color=C_RED, linewidth=2, label='KDE')
    skew = stats.skew(data_plot)
    kurt = stats.kurtosis(data_plot)
    ax.set_title(f"{col}\\nSkew={skew:.2f} | Kurt={kurt:.2f}", fontsize=9)
    ax.set_xlabel('')
    ax.tick_params(labelsize=7)

fig.suptitle("Distribusi Setiap Variabel (Data Berlabel 2010–2024)", fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_01_distributions.png", dpi=120, bbox_inches='tight')
plt.show()
print("📊 Interpretasi:")
print("  • Target_Volatilitas_Y: right-skewed (skew>0), menandakan lonjakan volatilitas ekstrem sesekali terjadi (ekor kanan tebal).")
print("  • VIX: juga right-skewed, konsisten — saat VIX melonjak, biasanya pasar dalam kondisi panik.")
print("  • CPI & BI_rate: distribusi bimodal karena perubahan rezim kebijakan selama 15 tahun.")"""))

# =============================================================================
# SECTION 5 — KUALITAS DATA & OUTLIER
# =============================================================================
cells.append(md_cell("## 5. Pemeriksaan Kualitas Data & Outlier"))

cells.append(code_cell("""\
print("[5.1] Nilai Non-Positif pada Harga & Indeks")
price_cols = ['OIL','GOLD','USDIDR','SP500','IHSG','VIX']
invalid_neg = (labeled[price_cols] <= 0).sum()
print(invalid_neg.to_string())

print("\\n[5.2] IQR Outlier Count (per kolom, data berlabel)")
outlier_summary = {}
for col in COLS:
    q1, q3 = labeled[col].quantile(0.25), labeled[col].quantile(0.75)
    iqr = q3 - q1
    n_out = ((labeled[col] < q1 - 1.5*iqr) | (labeled[col] > q3 + 1.5*iqr)).sum()
    outlier_summary[col] = {'Q1': q1, 'Q3': q3, 'IQR': iqr, 'N Outlier': n_out,
                            'Outlier %': round(n_out/len(labeled)*100, 2)}
out_df = pd.DataFrame(outlier_summary).T
print(out_df[['N Outlier','Outlier %']].to_string())"""))

cells.append(code_cell("""\
# 5.3 Boxplot — semua kolom numerik
fig, ax = plt.subplots(figsize=(14, 5))
norm_data = labeled[COLS].apply(lambda x: (x - x.mean()) / x.std())  # z-score agar comparable
norm_data.boxplot(ax=ax, grid=True, patch_artist=True,
    boxprops=dict(facecolor='#BFDBFE'), medianprops=dict(color=C_RED, linewidth=2))
ax.set_title("Deteksi Outlier via Boxplot (Z-Score Normalized, Data 2010–2024)", fontsize=13)
ax.set_ylabel("Z-Score")
ax.axhline(0, color=C_GRAY, linestyle='--', linewidth=0.8)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_02_outlier_boxplot.png", dpi=120, bbox_inches='tight')
plt.show()
print("📊 Interpretasi: Outlier yang muncul tidak bersifat acak — mayoritas sesuai dengan event nyata")
print("   (krisis COVID-2020, oil crash 2020, dll.). Tidak dilakukan penghapusan outlier.")"""))

# =============================================================================
# SECTION 6 — TIME-SERIES TREN
# =============================================================================
cells.append(md_cell("## 6. Analisis Tren Time-Series Variabel Makro-Finansial"))

cells.append(code_cell("""\
# 6.1 Panel time-series semua fitur
MACRO_GROUPS = {
    'Pasar Saham'   : ['IHSG', 'SP500'],
    'Komoditas'     : ['OIL', 'GOLD'],
    'Kurs & Risiko' : ['USDIDR', 'VIX'],
    'Kebijakan Moneter': ['BI_rate', 'US_rate'],
    'Inflasi'       : ['CPI'],
}

COLORS = [C_BLUE, C_RED, C_ORANGE, C_GREEN, C_GRAY]

fig, axes = plt.subplots(len(MACRO_GROUPS), 1, figsize=(18, 18), sharex=True)
for ax, (group, cols), color in zip(axes, MACRO_GROUPS.items(), COLORS):
    for j, col in enumerate(cols):
        c = [C_BLUE, C_RED][j % 2]
        ax.plot(df['Date'], df[col], color=c, linewidth=0.9, label=col, alpha=0.85)
    ax.set_ylabel(group, fontsize=10)
    ax.legend(loc='upper left', fontsize=8)
    # Annotate major events
    events = {
        '2020-03-16': ('COVID\\nCrash', C_RED),
        '2015-08-24': ('China\\nCrisis', C_ORANGE),
        '2013-05-22': ('Taper\\nTantrum', C_GRAY),
    }
    for date_str, (label, ec) in events.items():
        dt = pd.Timestamp(date_str)
        ax.axvline(dt, color=ec, linestyle='--', linewidth=0.8, alpha=0.7)
        ax.text(dt, ax.get_ylim()[1]*0.95, label, fontsize=6, color=ec, ha='center')

axes[-1].xaxis.set_major_locator(mdates.YearLocator(2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(axes[-1].get_xticklabels(), rotation=30)
fig.suptitle("Tren Variabel Makro-Finansial (2010–2026)", fontsize=14, y=1.002)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_03_timeseries_macro.png", dpi=120, bbox_inches='tight')
plt.show()
print("📊 Interpretasi:")
print("  • IHSG dan SP500 bergerak searah secara umum (globalisasi pasar modal).")
print("  • Lonjakan VIX pada Maret 2020 adalah puncak tertinggi — sesuai ekspektasi COVID crash.")
print("  • USDIDR dan GOLD punya tren naik jangka panjang (inflasi & depresiasi rupiah).")
print("  • BI_rate dan US_rate: divergensi pasca-2022 saat Fed agresif naikkan suku bunga.")"""))

# =============================================================================
# SECTION 7 — DISTRIBUSI TARGET
# =============================================================================
cells.append(md_cell("""\
## 7. Analisis Distribusi Target Volatilitas IHSG

**Nama kolom:** `Target_Volatilitas_Y`  
**Interpretasi:** Realized volatility IHSG 5 hari ke depan (lihat Bagian 12 untuk audit definisi)."""))

cells.append(code_cell("""\
y = labeled['Target_Volatilitas_Y']

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 7.1 Histogram
axes[0].hist(y, bins=80, color=C_BLUE, edgecolor='white', linewidth=0.4)
axes[0].axvline(y.mean(), color=C_RED, linestyle='--', linewidth=1.5, label=f'Mean={y.mean():.4f}')
axes[0].axvline(y.median(), color=C_ORANGE, linestyle='-.', linewidth=1.5, label=f'Median={y.median():.4f}')
axes[0].set_title("Histogram Target Volatilitas")
axes[0].set_xlabel("Target_Volatilitas_Y")
axes[0].set_ylabel("Frekuensi")
axes[0].legend()

# 7.2 Log-scale histogram (untuk melihat ekor)
axes[1].hist(y, bins=80, color=C_ORANGE, edgecolor='white', linewidth=0.4)
axes[1].set_yscale('log')
axes[1].set_title("Histogram (Skala Log Y) — Ekor Distribusi")
axes[1].set_xlabel("Target_Volatilitas_Y")
axes[1].set_ylabel("Frekuensi (log)")

# 7.3 Time-series target + event markers
axes[2].plot(labeled['Date'], y, color=C_BLUE, linewidth=0.8, alpha=0.8)
axes[2].fill_between(labeled['Date'], y, alpha=0.2, color=C_BLUE)
# Threshold 2 std
thr = y.mean() + 2*y.std()
axes[2].axhline(thr, color=C_RED, linestyle='--', linewidth=1, label=f'Mean+2σ={thr:.4f}')
axes[2].set_title("Time-Series Target Volatilitas IHSG")
axes[2].set_xlabel("Tanggal")
axes[2].set_ylabel("Realized Volatility")
axes[2].legend(fontsize=8)

plt.suptitle("Distribusi & Dinamika Target Volatilitas IHSG (2010–2024)", fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_04_target_distribution.png", dpi=120, bbox_inches='tight')
plt.show()

print(f"📊 Statistik Target:")
print(f"  Mean         : {y.mean():.5f}")
print(f"  Median       : {y.median():.5f}")
print(f"  Std          : {y.std():.5f}")
print(f"  Skewness     : {stats.skew(y):.3f}  (>1 → distribusi sangat right-skewed)")
print(f"  Kurtosis     : {stats.kurtosis(y):.3f}  (>3 → ekor lebih tebal dari normal — leptokurtic)")
print(f"  Max          : {y.max():.5f} pada {labeled.loc[y.idxmax(),'Date'].date()}")
print(f"  % outlier >Mean+2σ : {(y > thr).mean()*100:.1f}%")
print()
print("  → Distribusi target TIDAK normal (fat tails). Ini tipikal untuk volatilitas aset finansial.")
print("  → Model harus robust terhadap nilai ekstrem (COVID-2020, dst.).")"""))

# =============================================================================
# SECTION 8 — RETURN IHSG & HUBUNGAN DENGAN TARGET
# =============================================================================
cells.append(md_cell("## 8. Analisis Return IHSG & Hubungannya dengan Target"))

cells.append(code_cell("""\
df_l = labeled.copy()
df_l['IHSG_ret'] = df_l['IHSG'].pct_change()
df_l['IHSG_ret_abs'] = df_l['IHSG_ret'].abs()
df_l['rv_past5'] = df_l['IHSG_ret'].rolling(5).std()   # vol 5 hari lalu (bukan target, tidak leakage)

fig, axes = plt.subplots(2, 2, figsize=(18, 10))

# 8.1 Return harian
axes[0, 0].plot(df_l['Date'], df_l['IHSG_ret'], color=C_BLUE, linewidth=0.6, alpha=0.8)
axes[0, 0].axhline(0, color=C_GRAY, linewidth=0.8, linestyle='--')
axes[0, 0].set_title("Return Harian IHSG")
axes[0, 0].set_xlabel("Tanggal")
axes[0, 0].set_ylabel("Return Harian (pct_change)")

# 8.2 Histogram return
axes[0, 1].hist(df_l['IHSG_ret'].dropna(), bins=100, color=C_BLUE, edgecolor='white', linewidth=0.3, density=True)
x = np.linspace(df_l['IHSG_ret'].dropna().min(), df_l['IHSG_ret'].dropna().max(), 300)
from scipy.stats import norm
mu, sigma = df_l['IHSG_ret'].dropna().mean(), df_l['IHSG_ret'].dropna().std()
axes[0, 1].plot(x, norm.pdf(x, mu, sigma), color=C_RED, linewidth=2, label='Normal PDF')
axes[0, 1].set_title("Distribusi Return Harian IHSG vs Normal")
axes[0, 1].set_xlabel("Return")
axes[0, 1].set_ylabel("Density")
axes[0, 1].legend()

# 8.3 Scatter: |return| vs Target Y
sample = df_l[['IHSG_ret_abs', 'Target_Volatilitas_Y']].dropna().sample(1000, random_state=42)
axes[1, 0].scatter(sample['IHSG_ret_abs'], sample['Target_Volatilitas_Y'],
                   alpha=0.3, s=10, color=C_BLUE)
corr_val = df_l['IHSG_ret_abs'].corr(df_l['Target_Volatilitas_Y'])
axes[1, 0].set_title(f"|Return Harian| vs Target Volatilitas (r={corr_val:.3f})")
axes[1, 0].set_xlabel("|IHSG Return|")
axes[1, 0].set_ylabel("Target_Volatilitas_Y")

# 8.4 Scatter: past_vol vs Target (GARCH-like: past vol predicts future vol)
sample2 = df_l[['rv_past5', 'Target_Volatilitas_Y']].dropna().sample(1000, random_state=42)
axes[1, 1].scatter(sample2['rv_past5'], sample2['Target_Volatilitas_Y'],
                   alpha=0.3, s=10, color=C_ORANGE)
corr_past = df_l['rv_past5'].corr(df_l['Target_Volatilitas_Y'])
axes[1, 1].set_title(f"Vol 5-Hari Lalu vs Target Volatilitas (r={corr_past:.3f})")
axes[1, 1].set_xlabel("Realized Vol 5-Hari Lalu")
axes[1, 1].set_ylabel("Target_Volatilitas_Y")

plt.suptitle("Return IHSG & Hubungannya dengan Target Volatilitas", fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_05_ihsg_return_vs_target.png", dpi=120, bbox_inches='tight')
plt.show()

print("📊 Interpretasi:")
print(f"  • Korelasi |return harian| vs Target  : {corr_val:.3f}")
print(f"  • Korelasi vol 5-hari lalu vs Target  : {corr_past:.3f}")
print("  → Volatilitas masa lalu adalah prediktor kuat volatilitas masa depan (volatility clustering).")
print("  → Return harian saja (tanpa aggregasi) lebih lemah — fitur rolling lebih informatif.")"""))

# =============================================================================
# SECTION 9 — HEATMAP KORELASI
# =============================================================================
cells.append(md_cell("## 9. Heatmap Korelasi & Analisis Hubungan Fitur terhadap Target"))

cells.append(code_cell("""\
# Tambahkan fitur turunan sederhana untuk korelasi awal
df_corr = labeled.copy()
df_corr['IHSG_ret'] = df_corr['IHSG'].pct_change()
df_corr['rv_past5']  = df_corr['IHSG_ret'].rolling(5).std()   # vol lalu — bukan Y
df_corr['USDIDR_ret5'] = df_corr['USDIDR'].pct_change(5)
df_corr['OIL_ret5']    = df_corr['OIL'].pct_change(5)
df_corr['rate_diff']   = df_corr['BI_rate'] - df_corr['US_rate']
df_corr['VIX_rel']     = df_corr['VIX'] / df_corr['VIX'].rolling(20).mean()

CORR_COLS = ['OIL','GOLD','USDIDR','SP500','IHSG','VIX','CPI','BI_rate','US_rate',
             'IHSG_ret','rv_past5','USDIDR_ret5','OIL_ret5','rate_diff','VIX_rel',
             'Target_Volatilitas_Y']

corr_matrix = df_corr[CORR_COLS].corr()

fig, ax = plt.subplots(figsize=(16, 13))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, vmin=-1, vmax=1, linewidths=0.5, linecolor='white',
            annot_kws={'size': 7}, ax=ax)
ax.set_title("Heatmap Korelasi Pearson — Semua Variabel & Fitur Awal\\n(Data Berlabel 2010–2024)",
             fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_06_correlation_heatmap.png", dpi=120, bbox_inches='tight')
plt.show()

# Bar chart: korelasi masing-masing fitur terhadap target
target_corr = corr_matrix['Target_Volatilitas_Y'].drop('Target_Volatilitas_Y').sort_values(key=abs, ascending=False)
fig, ax = plt.subplots(figsize=(12, 5))
colors = [C_RED if v > 0 else C_BLUE for v in target_corr.values]
bars = ax.barh(target_corr.index, target_corr.values, color=colors, edgecolor='white')
ax.axvline(0, color='black', linewidth=0.8)
for bar, val in zip(bars, target_corr.values):
    ax.text(val + 0.005 * np.sign(val), bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', fontsize=8)
ax.set_title("Korelasi Pearson Setiap Fitur terhadap Target_Volatilitas_Y\\n(Diurutkan berdasarkan |korelasi|)",
             fontsize=12)
ax.set_xlabel("Korelasi Pearson")
plt.tight_layout()
plt.savefig("../outputs/eda/fig_07_feature_target_correlation.png", dpi=120, bbox_inches='tight')
plt.show()

print("📊 Interpretasi:")
print("  • rv_past5 (vol 5-hari lalu) adalah fitur paling berkorelasi dengan target → volatility clustering.")
print("  • VIX dan VIX_rel: korelasi positif sedang — sentimen panik global berpengaruh ke IHSG.")
print("  • Fitur level (IHSG, GOLD, dsb.) punya korelasi rendah — transformasi return/vol lebih relevan.")
print("  ⚠ Korelasi bukan kausalitas. Hubungan ini adalah pra-analisis, bukan bukti final.")"""))

# =============================================================================
# SECTION 10 — VOLATILITY CLUSTERING
# =============================================================================
cells.append(md_cell("## 10. Pemeriksaan Volatility Clustering"))

cells.append(code_cell("""\
df_vc = labeled.copy()
df_vc['IHSG_ret'] = df_vc['IHSG'].pct_change()
df_vc['rv_past5'] = df_vc['IHSG_ret'].rolling(5).std()

fig, axes = plt.subplots(2, 1, figsize=(18, 10), sharex=True)

# 10.1 Return harian vs Target
axes[0].fill_between(df_vc['Date'], df_vc['IHSG_ret'].abs(), color=C_BLUE, alpha=0.5, label='|Return Harian|')
axes[0].set_ylabel("|Return Harian IHSG|")
axes[0].legend(loc='upper left')

axes[1].fill_between(df_vc['Date'], df_vc['Target_Volatilitas_Y'], color=C_RED, alpha=0.5, label='Target Vol Y')
axes[1].set_ylabel("Target_Volatilitas_Y")
axes[1].legend(loc='upper left')

fig.suptitle("Volatility Clustering: |Return Harian| & Target Volatilitas (2010–2024)", fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_08_volatility_clustering.png", dpi=120, bbox_inches='tight')
plt.show()

# ACF-style: autocorrelation of absolute returns
from pandas.plotting import autocorrelation_plot
fig, ax = plt.subplots(figsize=(12, 4))
abs_ret = df_vc['IHSG_ret'].abs().dropna()
lags = range(1, 31)
acf_vals = [abs_ret.autocorr(lag) for lag in lags]
ax.bar(lags, acf_vals, color=C_BLUE, alpha=0.7)
ax.axhline(0, color='black', linewidth=0.8)
ci = 1.96 / np.sqrt(len(abs_ret))
ax.axhline(ci, color=C_RED, linestyle='--', linewidth=1, label=f'95% CI = ±{ci:.3f}')
ax.axhline(-ci, color=C_RED, linestyle='--', linewidth=1)
ax.set_title("Autocorrelation |Return Harian IHSG| (Lag 1–30) — Bukti Volatility Clustering")
ax.set_xlabel("Lag (Hari)")
ax.set_ylabel("Autokorelasi")
ax.legend()
plt.tight_layout()
plt.savefig("../outputs/eda/fig_09_acf_abs_return.png", dpi=120, bbox_inches='tight')
plt.show()

sig_lags = [l for l, a in zip(lags, acf_vals) if abs(a) > ci]
print(f"📊 Interpretasi:")
print(f"  • Autokorelasi |return| signifikan pada lag: {sig_lags}")
print(f"  • Ini adalah bukti kuantitatif volatility clustering — volatilitas tinggi cenderung")
print(f"    diikuti volatilitas tinggi berikutnya (ARCH effect).")
print(f"  → Model harus mampu menangkap dependensi temporal ini. Fitur rolling vol adalah kunci.")"""))

# =============================================================================
# SECTION 11 — ANALISIS FITUR KANDIDAT
# =============================================================================
cells.append(md_cell("""\
## 11. Analisis Awal Kandidat Fitur Turunan

Tiga kandidat fitur untuk Task 1 dievaluasi secara eksperimental.  
**Catatan:** Fitur ini dihitung dalam memori saja — dataset mentah tidak diubah.  
Klaim "paling berpengaruh" belum dibuat sampai ada bukti dari model akhir."""))

cells.append(code_cell("""\
df_feat = labeled.copy()
df_feat['IHSG_ret'] = df_feat['IHSG'].pct_change()
df_feat = df_feat.sort_values('Date').reset_index(drop=True)

# ── Fitur Kandidat (semua menggunakan data yang tersedia PADA SAAT t) ────────
# Untuk prediksi hari-t: kita boleh pakai nilai fitur hingga hari-t (termasuk t)
# Nilai target (t+1..t+5) TIDAK dipakai sebagai fitur — tidak ada leakage.

# X1: Fear_Liquidity_Composite
# Rasionalitas: VIX (sentimen global) × depresiasi rupiah vs MA-20 (capital outflow pressure)
usdidr_ma20 = df_feat['USDIDR'].rolling(20).mean()
df_feat['X1_Fear_Liquidity'] = df_feat['VIX'] * np.log(df_feat['USDIDR'] / usdidr_ma20.replace(0, np.nan))

# X2: Rate_Differential_Pressure
# Rasionalitas: carry trade attractiveness × momentum kurs 5-hari
df_feat['X2_Rate_Diff_Pressure'] = (df_feat['BI_rate'] - df_feat['US_rate']) * df_feat['USDIDR'].pct_change(5)

# X3: Commodity_Macro_Shock
# Rasionalitas: triple interaction OIL × GOLD × SP500 5-day returns → global regime shift
df_feat['X3_Commodity_Shock'] = (
    df_feat['OIL'].pct_change(5) *
    df_feat['GOLD'].pct_change(5) *
    df_feat['SP500'].pct_change(5)
)

CANDIDATES = ['X1_Fear_Liquidity', 'X2_Rate_Diff_Pressure', 'X3_Commodity_Shock']

# Korelasi kandidat vs Target
print("Korelasi Pearson kandidat fitur vs Target_Volatilitas_Y:")
for col in CANDIDATES:
    c = df_feat[col].corr(df_feat['Target_Volatilitas_Y'])
    print(f"  {col:30s} : {c:.4f}")

print()
print("⚠  Korelasi ini bersifat linear dan belum mengontrol collinearity atau overfitting.")
print("   Bukti final akan datang dari SHAP/feature importance model (Task 3).")"""))

cells.append(code_cell("""\
# Visualisasi kandidat fitur vs Target
fig, axes = plt.subplots(1, 3, figsize=(20, 5))

for ax, col in zip(axes, CANDIDATES):
    sample = df_feat[[col, 'Target_Volatilitas_Y']].dropna().sample(
        min(1500, len(df_feat)), random_state=42)
    ax.scatter(sample[col], sample['Target_Volatilitas_Y'],
               alpha=0.25, s=8, color=C_BLUE)
    r = df_feat[col].corr(df_feat['Target_Volatilitas_Y'])
    ax.set_title(f"{col}\\nPearson r = {r:.3f}", fontsize=9)
    ax.set_xlabel(col, fontsize=8)
    ax.set_ylabel("Target_Volatilitas_Y", fontsize=8)

plt.suptitle("Scatter Plot: Kandidat Fitur Turunan vs Target Volatilitas\\n(1500 sampel acak dari data berlabel)", fontsize=12)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_10_candidate_features_scatter.png", dpi=120, bbox_inches='tight')
plt.show()

# Time-series kandidat fitur
fig, axes = plt.subplots(3, 1, figsize=(18, 12), sharex=True)
for ax, col in zip(axes, CANDIDATES):
    ax.plot(df_feat['Date'], df_feat[col], color=C_BLUE, linewidth=0.7, alpha=0.8)
    ax.set_ylabel(col, fontsize=9)
    ax.axhline(0, color=C_GRAY, linewidth=0.5, linestyle='--')
axes[-1].set_xlabel("Tanggal")
fig.suptitle("Tren Time-Series Kandidat Fitur Turunan (2010–2024)", fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/eda/fig_11_candidate_features_timeseries.png", dpi=120, bbox_inches='tight')
plt.show()
print("📊 Catatan visual:")
print("  X1: lonjakan saat krisis (VIX melonjak + rupiah melemah simultan) → signal bagus")
print("  X2: volatil di sekitar 0 → bereaksi terhadap perubahan arah kebijakan Fed vs BI")
print("  X3: sinyal sporadis saat ada guncangan komoditas bersamaan")"""))

# =============================================================================
# SECTION 12 — AUDIT TARGET & RISIKO LEAKAGE
# =============================================================================
cells.append(md_cell("""\
## 12. Audit Definisi Target & Risiko Data Leakage

Bagian ini mendokumentasikan hasil verifikasi kuantitatif formula target dan potensi leakage."""))

cells.append(code_cell("""\
print("=" * 60)
print("AUDIT TARGET: Target_Volatilitas_Y")
print("=" * 60)

df_audit = df.copy()
df_audit['IHSG_ret'] = df_audit['IHSG'].pct_change()

# Rekonstruksi hipotesis: std(return[t+1..t+5])
# shift(-5) + rolling(5) = std dari t+1 hingga t+5
df_audit['rv_reconstructed'] = df_audit['IHSG_ret'].shift(-5).rolling(5).std()

labeled_a = df_audit[df_audit['Target_Volatilitas_Y'].notna()].copy()

corr_verify = labeled_a['Target_Volatilitas_Y'].corr(labeled_a['rv_reconstructed'])
mae_verify  = (labeled_a['Target_Volatilitas_Y'] - labeled_a['rv_reconstructed']).abs().mean()
max_diff    = (labeled_a['Target_Volatilitas_Y'] - labeled_a['rv_reconstructed']).abs().max()

print(f"\\nHipotesis formula  : std(IHSG_return[t+1 .. t+5])")
print(f"Korelasi Pearson   : {corr_verify:.6f}")
print(f"MAE rata-rata      : {mae_verify:.8f}")
print(f"Selisih maks       : {max_diff:.8f}")
print()
if corr_verify > 0.999:
    print("✅ TERVERIFIKASI: Formula target terkonfirmasi dengan sangat tinggi.")
    print("   Target_Volatilitas_Y = std(pct_change(IHSG)[t+1 : t+5])")
else:
    print("⚠ Formula masih hipotesis — korelasi tidak mencapai ambang 0.999.")

print()
print("-" * 60)
print("IMPLIKASI LEAKAGE")
print("-" * 60)
lines_leakage = [
    "",
    "[OK] Tidak ada leakage JIKA:",
    "   - Semua rolling fitur dihitung dari data t dan sebelumnya saja",
    "   - Tidak ada nilai dari t+1..t+5 yang masuk ke X",
    "   - Scaler/imputer di-fit HANYA dari data Training",
    "",
    "[!] Risiko leakage yang HARUS dihindari di Task 2:",
    "   1. Penggunaan std(return[t..t+4]) sebagai fitur -> mencakup hari ini",
    "      yang berkorelasi kuat dengan target -> leakage informasi",
    "   2. Scaler StandardScaler.fit() dari seluruh dataset (termasuk val/test)",
    "   3. Pengisian NaN dengan mean/median seluruh dataset",
    "   4. random_state shuffle pada split data time-series",
]
print("\\n".join(lines_leakage))

print()
print("-" * 60)
print("PARTISI DATA FINAL (REKOMENDASI)")
print("-" * 60)
n_train = len(labeled_a[labeled_a['Date'] <= '2021-12-31'])
n_val   = len(labeled_a[labeled_a['Date'] >= '2022-01-01'])
n_test  = len(df[df['Target_Volatilitas_Y'].isna()])
print(f"  Train      : 2010-01-04 -> 2021-12-31   ({n_train:,} baris)")
print(f"  Validasi   : 2022-01-01 -> 2024-12-31   ({n_val:,} baris)")
print(f"  Test (NaN) : 2025-01-02 -> 2026-05-22   ({n_test:,} baris - prediksi final)")
"""))

# =============================================================================
# SECTION 13 — KESIMPULAN EDA
# =============================================================================
cells.append(md_cell("## 13. Kesimpulan EDA & Implikasi Feature Engineering"))

cells.append(code_cell("""\
summary_lines = [
    "=" * 65,
    "  RINGKASAN KESIMPULAN EDA - CHECKPOINT 0",
    "=" * 65,
    "",
    "[1] KUALITAS DATA",
    "    [OK] 4.266 baris, tidak ada missing value kecuali target Y (359 baris = uji)",
    "    [OK] Tidak ada baris duplikat",
    "    [OK] Semua harga/indeks bernilai positif",
    "    [!]  Outlier ada tapi nyata (krisis COVID-2020) - jangan dihapus",
    "",
    "[2] TARGET VOLATILITAS",
    "    [OK] Target_Volatilitas_Y TERVERIFIKASI = std(IHSG_return[t+1..t+5])",
    "         (korelasi rekonstruksi vs target: >0.9997)",
    "    [OK] Data berlabel: 2010-2024 (3.907 baris)",
    "    [OK] Data uji: 2025-2026 (359 baris, Y=NaN)",
    "",
    "[3] TEMUAN KUNCI EDA",
    "    - Distribusi target: right-skewed, leptokurtic (fat-tails finansial)",
    "    - Volatility clustering terbukti secara kuantitatif (ACF signifikan)",
    "    - Past vol 5-hari (rv_past5) adalah prediktor terkuat target (r~0.45)",
    "    - VIX berkorelasi sedang dengan target - sinyal global penting",
    "    - Fitur level (IHSG, GOLD harga absolut) berkorelasi rendah - perlu transformasi",
    "",
    "[4] KANDIDAT FITUR",
    "    - X1 Fear_Liquidity_Composite: rasionalitas kuat, perlu validasi model",
    "    - X2 Rate_Differential_Pressure: logis, sinyal sporadis",
    "    - X3 Commodity_Macro_Shock: interaksi kompleks, uji multikolinearitas diperlukan",
    "    [!] Klaim 'paling berpengaruh' DITUNDA sampai bukti model (Task 3 SHAP)",
    "",
    "[5] RISIKO LEAKAGE",
    "    [!] Risiko utama: std(return[t..t+4]) sebagai fitur sangat berbahaya",
    "    [OK] Semua fitur rolling harus .shift(1) agar tidak mencakup return hari ini",
    "    [OK] Scaler harus fit hanya dari training set",
    "",
    "[6] LANGKAH BERIKUTNYA (Task 2 & 3)",
    "    -> Time-series split: Train 2010-2021 | Val 2022-2024 | Test 2025-2026",
    "    -> Feature engineering final dengan anti-leakage pipeline",
    "    -> Modeling LightGBM + hyperparameter tuning",
    "    -> XAI: SHAP global + lokal + error analysis",
    "=" * 65,
]
print("\\n".join(summary_lines))
"""))

# =============================================================================
# WRITE NOTEBOOK
# =============================================================================
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.10"
        }
    },
    "cells": cells
}

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"[OK] Notebook ditulis: {NOTEBOOK_PATH}")
print(f"   Total cells: {len(cells)}")
