"""
INCEPTION 2026 — Feature Engineering & Preprocessing Module
Checkpoint 1B: Finalisasi Feature Engineering

Modul ini bertanggung jawab untuk:
1. Pembersihan terkontrol anomali kurs USD/IDR tanpa mengubah data mentah CSV.
2. Rekayasa fitur prediktor volatilitas historis (multi-scale volatility, momentum, macro spread).
3. Implementasi 3 fitur wajib (X1, X2, X3) beserta alternatif formula yang robust.
4. Pengujian integritas temporal dan uji anti-leakage independen.

Asumsi Waktu Prediksi:
- Seluruh fitur pada baris t dihitung menggunakan data yang observable pada End-of-Day (EOD) hari t.
- Target adalah realized volatility pada horizon [t+1, t+5], sehingga tidak ada overlap dengan fitur historis t.
"""

import os
from typing import Dict, Tuple, Any
import numpy as np
import pandas as pd


def preprocess_usdidr(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Melakukan koreksi eksplisit terhadap anomali desimal kurs USD/IDR.
    
    Aturan Integritas:
    - Tidak mengubah file CSV mentah.
    - Kolom 'USDIDR' asli disalin ke 'USDIDR_raw' untuk transparansi audit.
    - Koreksi hanya diterapkan pada baris yang secara spesifik teridentifikasi
      mengalami pergeseran koma desimal (faktor 10x).
    - Fungsi akan gagal (raise ValueError) jika kondisi eksak tidak terpenuhi.
    """
    df_out = df.copy()
    if 'Date' not in df_out.columns or 'USDIDR' not in df_out.columns:
        raise ValueError("DataFrame harus memiliki kolom 'Date' dan 'USDIDR'.")
        
    df_out['Date'] = pd.to_datetime(df_out['Date'])
    df_out['USDIDR_raw'] = df_out['USDIDR'].copy()
    df_out['USDIDR_clean'] = df_out['USDIDR'].copy()
    
    # ── Identifikasi Anomali Eksak ─────────────────────────────────────────────
    # Anomali 1: 2010-11-01 (nilai tercatat ~888.11, tetangga ~8920)
    target_dt1 = pd.Timestamp('2010-11-01')
    row1 = df_out[df_out['Date'] == target_dt1]
    if row1.empty:
        raise ValueError(f"Validasi gagal: Tanggal {target_dt1.date()} tidak ditemukan dalam dataset.")
    val1_raw = row1['USDIDR'].values[0]
    if not (800.0 <= val1_raw <= 950.0):
        raise ValueError(f"Validasi gagal: Nilai USDIDR pada {target_dt1.date()} ({val1_raw}) "
                         f"tidak berada pada rentang anomali yang diharapkan (~888.11).")
    
    # Anomali 2: 2012-02-07 (nilai tercatat 892.00, tetangga ~8928)
    target_dt2 = pd.Timestamp('2012-02-07')
    row2 = df_out[df_out['Date'] == target_dt2]
    if row2.empty:
        raise ValueError(f"Validasi gagal: Tanggal {target_dt2.date()} tidak ditemukan dalam dataset.")
    val2_raw = row2['USDIDR'].values[0]
    if not (800.0 <= val2_raw <= 950.0):
        raise ValueError(f"Validasi gagal: Nilai USDIDR pada {target_dt2.date()} ({val2_raw}) "
                         f"tidak berada pada rentang anomali yang diharapkan (892.00).")
    
    # Terapkan koreksi faktor 10x
    df_out.loc[df_out['Date'] == target_dt1, 'USDIDR_clean'] = val1_raw * 10.0
    df_out.loc[df_out['Date'] == target_dt2, 'USDIDR_clean'] = val2_raw * 10.0
    
    val1_clean = df_out.loc[df_out['Date'] == target_dt1, 'USDIDR_clean'].values[0]
    val2_clean = df_out.loc[df_out['Date'] == target_dt2, 'USDIDR_clean'].values[0]
    
    audit_log = {
        'total_corrections': 2,
        'records': [
            {
                'date': str(target_dt1.date()),
                'raw_value': float(val1_raw),
                'clean_value': float(val1_clean),
                'factor': 10.0,
                'evidence': 'Surrounding neighbor ~8923 IDR/USD; historical JISDOR ref ~8900 IDR/USD'
            },
            {
                'date': str(target_dt2.date()),
                'raw_value': float(val2_raw),
                'clean_value': float(val2_clean),
                'factor': 10.0,
                'evidence': 'Surrounding neighbor ~8928 IDR/USD; exactly matches 2012-02-10 price of 8920.0 IDR/USD'
            }
        ]
    }
    
    return df_out, audit_log


def engineer_features(df: pd.DataFrame, use_cleaned_usdidr: bool = True) -> pd.DataFrame:
    """
    Menghasilkan seluruh kandidat fitur historis dengan proteksi matematis terhadap
    nilai tak hingga (inf) dan pembagian nol.
    
    Seluruh fitur dihitung HANYA menggunakan informasi masa lalu dan masa kini (<= t).
    Target_Volatilitas_Y TIDAK PERNAH digunakan dalam perhitungan fitur apa pun.
    """
    # Pastikan data terurut berdasarkan tanggal
    df_feat = df.sort_values('Date').reset_index(drop=True).copy()
    
    # Pilih kurs yang digunakan
    usdidr_col = 'USDIDR_clean' if (use_cleaned_usdidr and 'USDIDR_clean' in df_feat.columns) else 'USDIDR'
    
    # ── 1. Return Harian IHSG ─────────────────────────────────────────────────
    # r_t = (IHSG_t - IHSG_{t-1}) / IHSG_{t-1}
    df_feat['IHSG_ret'] = df_feat['IHSG'].pct_change()
    
    # ── 2. Volatilitas Historis IHSG (Multi-Scale) ────────────────────────────
    # Mengukur dispersi return historis selama jendela 5, 10, dan 20 hari perdagangan
    # ddof=1 (unbiased sample standard deviation)
    df_feat['rv_past5']  = df_feat['IHSG_ret'].rolling(5).std(ddof=1)
    df_feat['rv_past10'] = df_feat['IHSG_ret'].rolling(10).std(ddof=1)
    df_feat['rv_past20'] = df_feat['IHSG_ret'].rolling(20).std(ddof=1)
    
    # ── 3. Momentum IHSG ──────────────────────────────────────────────────────
    # Mengukur arah dan kekuatan tren pasar saham domestik (asymmetric leverage effect)
    df_feat['mom_ihsg_5']  = df_feat['IHSG'].pct_change(5)
    df_feat['mom_ihsg_10'] = df_feat['IHSG'].pct_change(10)
    
    # ── 4. Perubahan Kurs USD/IDR 5 Hari ──────────────────────────────────────
    # Mengukur laju depresiasi/apresiasi Rupiah selama 5 hari
    df_feat['usdidr_ret5'] = df_feat[usdidr_col].pct_change(5)
    
    # ── 5. Perbandingan VIX terhadap Rata-rata Historis ─────────────────────────
    # Mengukur kejutan kepanikan pasar global jangka pendek terhadap baseline 20 hari
    vix_ma20 = df_feat['VIX'].rolling(20).mean()
    # Proteksi pembagian nol
    df_feat['vix_ratio_ma20'] = df_feat['VIX'] / vix_ma20.replace(0, np.nan)
    df_feat['vix_diff_ma20']  = df_feat['VIX'] - vix_ma20
    
    # ── 6. Fitur Wajib X1: Fear Liquidity Composite ───────────────────────────
    # Interaksi ketakutan global (VIX) x deviasi kurs Rupiah dari moving average 20 hari
    usdidr_ma20 = df_feat[usdidr_col].rolling(20).mean().replace(0, np.nan)
    ratio_usdidr = (df_feat[usdidr_col] / usdidr_ma20).replace(0, np.nan)
    
    # Formula Original: VIX * ln(USDIDR / MA20(USDIDR))
    # Proteksi: jika ratio <= 0, ganti dengan NaN sebelum logaritma
    valid_ratio = ratio_usdidr.where(ratio_usdidr > 0, np.nan)
    df_feat['X1_Fear_Liquidity_Original'] = df_feat['VIX'] * np.log(valid_ratio)
    
    # Formula Alternatif (Robust Taylor approximation): VIX * ((USDIDR - MA20) / MA20)
    # Menghindari singularity logaritmik dan tetap terdefinisi linier
    df_feat['X1_Fear_Liquidity_Robust'] = df_feat['VIX'] * ((df_feat[usdidr_col] - usdidr_ma20) / usdidr_ma20)
    
    # ── 7. Fitur Wajib X2: Rate Differential Pressure ─────────────────────────
    # Selisih suku bunga domestik vs The Fed dikalikan momentum pergerakan kurs 5 hari
    rate_diff = df_feat['BI_rate'] - df_feat['US_rate']
    df_feat['rate_differential'] = rate_diff
    
    # Formula Original: (BI_rate - US_rate) * usdidr_ret5
    df_feat['X2_Rate_Diff_Pressure_Original'] = rate_diff * df_feat['usdidr_ret5']
    
    # Formula Alternatif: Magnitudo absolut stres suku bunga & valas
    df_feat['X2_Rate_Diff_Pressure_Abs'] = rate_diff.abs() * df_feat['usdidr_ret5'].abs()
    
    # ── 8. Fitur Wajib X3: Commodity Macro Shock ──────────────────────────────
    oil_ret5   = df_feat['OIL'].pct_change(5)
    gold_ret5  = df_feat['GOLD'].pct_change(5)
    sp500_ret5 = df_feat['SP500'].pct_change(5)
    
    df_feat['oil_ret5']   = oil_ret5
    df_feat['gold_ret5']  = gold_ret5
    df_feat['sp500_ret5'] = sp500_ret5
    
    # Formula Original: perkalian 3 return 5-hari
    df_feat['X3_Commodity_Shock_Original'] = oil_ret5 * gold_ret5 * sp500_ret5
    
    # Formula Alternatif: Norma Euclidean L2 dari vektor guncangan makro global
    # sqrt((OIL_ret5)^2 + (GOLD_ret5)^2 + (SP500_ret5)^2)
    df_feat['X3_Commodity_Shock_L2Norm'] = np.sqrt(oil_ret5**2 + gold_ret5**2 + sp500_ret5**2)
    
    return df_feat


def run_anti_leakage_and_quality_tests(df_raw: pd.DataFrame) -> Dict[str, Any]:
    """
    Suite pengujian komprehensif untuk memvalidasi:
    1. Urutan temporal tanggal
    2. Akurasi koreksi kurs USD/IDR
    3. Integritas numerik (tidak ada nilai tak hingga)
    4. Alignment jendela observasi historis
    5. Proteksi Anti-Leakage (uji invariansi masa depan)
    """
    test_results = {}
    
    # ── Test 1: Monotonisitas Tanggal ──────────────────────────────────────────
    df_clean, log = preprocess_usdidr(df_raw)
    is_monotonic = df_clean['Date'].is_monotonic_increasing
    test_results['test_1_date_monotonic'] = {
        'passed': bool(is_monotonic),
        'min_date': str(df_clean['Date'].min().date()),
        'max_date': str(df_clean['Date'].max().date()),
        'total_rows': int(len(df_clean))
    }
    assert is_monotonic, "Test 1 Gagal: Tanggal tidak terurut secara monoton naik."
    
    # ── Test 2: Nilai Kurs Sebelum & Sesudah Koreksi ───────────────────────────
    dt1 = pd.Timestamp('2010-11-01')
    dt2 = pd.Timestamp('2012-02-07')
    val1_raw = df_clean.loc[df_clean['Date'] == dt1, 'USDIDR_raw'].values[0]
    val1_clean = df_clean.loc[df_clean['Date'] == dt1, 'USDIDR_clean'].values[0]
    val2_raw = df_clean.loc[df_clean['Date'] == dt2, 'USDIDR_raw'].values[0]
    val2_clean = df_clean.loc[df_clean['Date'] == dt2, 'USDIDR_clean'].values[0]
    
    test_2_pass = (
        np.isclose(val1_clean, val1_raw * 10.0) and
        np.isclose(val2_clean, val2_raw * 10.0) and
        (val1_clean > 8000.0) and (val2_clean > 8000.0)
    )
    test_results['test_2_usdidr_correction'] = {
        'passed': bool(test_2_pass),
        'row_215_raw': float(val1_raw),
        'row_215_clean': float(val1_clean),
        'row_546_raw': float(val2_raw),
        'row_546_clean': float(val2_clean)
    }
    assert test_2_pass, "Test 2 Gagal: Nilai kurs sebelum dan sesudah koreksi tidak cocok."
    
    # ── Test 3: Integritas Numerik (Tidak ada Infinitas) ───────────────────────
    df_features = engineer_features(df_clean, use_cleaned_usdidr=True)
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    has_pos_inf = np.isposinf(df_features[numeric_cols]).any().any()
    has_neg_inf = np.isneginf(df_features[numeric_cols]).any().any()
    test_3_pass = (not has_pos_inf) and (not has_neg_inf)
    
    test_results['test_3_numerical_sanity'] = {
        'passed': bool(test_3_pass),
        'has_positive_infinity': bool(has_pos_inf),
        'has_negative_infinity': bool(has_neg_inf),
        'features_tested_count': int(len(numeric_cols))
    }
    assert test_3_pass, "Test 3 Gagal: Ditemukan nilai tak terhingga (np.inf) pada fitur."
    
    # ── Test 4: Alignment Jendela Historis ─────────────────────────────────────
    # Fitur rolling(W) harus memiliki persis W NaN di awal (atau W-1 tergantung min_periods)
    # rv_past5: pct_change menghasilkan 1 NaN, rolling(5) butuh 5 data -> total 5 NaN di awal
    n_nan_rv5 = df_features['rv_past5'].isna().sum()
    n_nan_rv20 = df_features['rv_past20'].isna().sum()
    # Pastikan baris ke-20 terisi
    test_4_pass = (n_nan_rv5 == 5) and (n_nan_rv20 == 20) and df_features.loc[20, 'rv_past20'] > 0
    test_results['test_4_window_alignment'] = {
        'passed': bool(test_4_pass),
        'rv_past5_initial_nans': int(n_nan_rv5),
        'rv_past20_initial_nans': int(n_nan_rv20),
        'row_20_rv20_value': float(df_features.loc[20, 'rv_past20'])
    }
    assert test_4_pass, f"Test 4 Gagal: Alignment rolling window tidak sesuai (NaN rv5={n_nan_rv5}, rv20={n_nan_rv20})."
    
    # ── Test 5: Pengujian Anti-Leakage (Invariansi Masa Depan) ─────────────────
    # Membuktikan bahwa fitur pada baris t TIDAK BERUBAH jika data pada t+1..t+K dimutilasi
    t_idx = 1000
    df_mutated = df_clean.copy()
    # Simpan nilai fitur asli pada baris t
    val_orig_t = df_features.loc[t_idx, 'rv_past20']
    val_orig_x1 = df_features.loc[t_idx, 'X1_Fear_Liquidity_Robust']
    val_orig_x3 = df_features.loc[t_idx, 'X3_Commodity_Shock_L2Norm']
    
    # Mutilasi data masa depan (t+1 hingga selesai): kalikan harga IHSG, VIX, OIL 1000x
    future_indices = df_mutated.index[df_mutated.index > t_idx]
    df_mutated.loc[future_indices, ['IHSG', 'VIX', 'OIL', 'GOLD', 'SP500', 'USDIDR_clean']] *= 1000.0
    
    # Hitung ulang fitur dari dataset termutilasi
    df_feat_mutated = engineer_features(df_mutated, use_cleaned_usdidr=True)
    val_mut_t = df_feat_mutated.loc[t_idx, 'rv_past20']
    val_mut_x1 = df_feat_mutated.loc[t_idx, 'X1_Fear_Liquidity_Robust']
    val_mut_x3 = df_feat_mutated.loc[t_idx, 'X3_Commodity_Shock_L2Norm']
    
    diff_rv = abs(val_orig_t - val_mut_t)
    diff_x1 = abs(val_orig_x1 - val_mut_x1)
    diff_x3 = abs(val_orig_x3 - val_mut_x3)
    
    test_5_pass = (diff_rv == 0.0) and (diff_x1 == 0.0) and (diff_x3 == 0.0)
    test_results['test_5_anti_leakage_invariance'] = {
        'passed': bool(test_5_pass),
        'evaluated_row_index': t_idx,
        'rv_past20_diff': float(diff_rv),
        'x1_robust_diff': float(diff_x1),
        'x3_l2norm_diff': float(diff_x3),
        'status': 'VERIFIED: Future data perturbation has exactly zero effect on row t features.'
    }
    assert test_5_pass, "Test 5 Gagal: Fitur pada baris t berubah saat data masa depan dimutilasi (Lookahead Leakage Terdeteksi!)."
    
    return test_results


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    raw_csv_path = os.path.join(project_root, 'Aset Lomba', 'dataset peserta.csv')
    
    print("=" * 65)
    print("INCEPTION 2026 - RUNNING FEATURE ENGINEERING & TESTS")
    print("=" * 65)
    print(f"Loading raw dataset from: {raw_csv_path}")
    df_raw = pd.read_csv(raw_csv_path)
    
    print("\n[Step 1] Preprocessing USD/IDR...")
    df_clean, audit_log = preprocess_usdidr(df_raw)
    print(f"  Total koreksi: {audit_log['total_corrections']}")
    for r in audit_log['records']:
        print(f"  - Tanggal: {r['date']} | Raw: {r['raw_value']:.2f} -> Clean: {r['clean_value']:.2f}")
    
    print("\n[Step 2] Engineering Features...")
    df_features = engineer_features(df_clean, use_cleaned_usdidr=True)
    feat_cols = [c for c in df_features.columns if c not in df_raw.columns and c not in ['USDIDR_raw', 'USDIDR_clean']]
    print(f"  Fitur baru berhasil dibuat ({len(feat_cols)} kolom):")
    for col in feat_cols:
        print(f"    * {col}")
        
    print("\n[Step 3] Running Automated Tests...")
    results = run_anti_leakage_and_quality_tests(df_raw)
    all_passed = all(v['passed'] for v in results.values())
    for t_name, res in results.items():
        print(f"  [{'PASS' if res['passed'] else 'FAIL'}] {t_name}")
    
    print("\n" + "=" * 65)
    if all_passed:
        print("ALL 5 FEATURE ENGINEERING TESTS PASSED SUCCESSFULLY! [OK]")
    else:
        print("SOME TESTS FAILED! [FAIL]")
    print("=" * 65)

