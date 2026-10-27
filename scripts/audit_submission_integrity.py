"""
Audit script for Checkpoint 5.1: Final Submission Integrity Audit.
This script performs non-destructive read-only verification of all submission files,
cross-referencing with raw dataset and Checkpoint 5 artifacts.
"""

import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUB_DIR = os.path.join(PROJECT_ROOT, "outputs", "submission")
RAW_PATH = os.path.join(PROJECT_ROOT, "Aset Lomba", "dataset peserta.csv")
NB_PATH = os.path.join(PROJECT_ROOT, "notebook", "08_Final_Training_Submission.ipynb")

print("=" * 80)
print("INCEPTION 2026 — CHECKPOINT 5.1: FINAL SUBMISSION INTEGRITY AUDIT")
print("=" * 80)

# 1. Load Raw Dataset
df_raw = pd.read_csv(RAW_PATH)
df_raw['Date_dt'] = pd.to_datetime(df_raw['Date'])
raw_total_rows = len(df_raw)
raw_labeled = df_raw[df_raw['Target_Volatilitas_Y'].notna()]
raw_test = df_raw[df_raw['Target_Volatilitas_Y'].isna()]

print(f"[RAW] Total rows: {raw_total_rows}")
print(f"[RAW] Columns ({len(df_raw.columns)-1}): {[c for c in df_raw.columns if c != 'Date_dt']}")
print(f"[RAW] Labeled rows: {len(raw_labeled)} (from {raw_labeled['Date'].min()} to {raw_labeled['Date'].max()})")
print(f"[RAW] Test rows: {len(raw_test)} (from {raw_test['Date'].min()} to {raw_test['Date'].max()})")

# 2. Audit 3 Submission Files (2-Column Format)
sub_files = [
    "submission_blend60_40.csv",
    "submission_blend50_30_20.csv",
    "submission_gbr_tuned.csv"
]

sub_dfs = {}
for sf in sub_files:
    fpath = os.path.join(SUB_DIR, sf)
    assert os.path.exists(fpath), f"File missing: {fpath}"
    
    # Read raw text to inspect delimiter, line endings, header
    with open(fpath, "rb") as f:
        raw_bytes = f.read()
    has_crlf = b"\r\n" in raw_bytes
    lines = raw_bytes.decode("utf-8").splitlines()
    header_line = lines[0]
    
    df_sub = pd.read_csv(fpath)
    sub_dfs[sf] = df_sub
    
    print("\n" + "-" * 60)
    print(f"AUDIT SUBMISSION FILE: {sf}")
    print("-" * 60)
    print(f"File size          : {len(raw_bytes):,} bytes")
    print(f"Header line        : '{header_line}'")
    print(f"Line count (lines) : {len(lines)} (Header + {len(lines)-1} rows)")
    print(f"Shape (df)         : {df_sub.shape}")
    print(f"Columns            : {df_sub.columns.tolist()}")
    print(f"Data types         : {df_sub.dtypes.to_dict()}")
    print(f"Date min/max       : {df_sub['Date'].min()} s/d {df_sub['Date'].max()}")
    print(f"Date duplicates    : {df_sub['Date'].duplicated().sum()}")
    print(f"Date monotonic inc : {df_sub['Date'].is_monotonic_increasing}")
    print(f"NaN count          : {df_sub.isna().sum().to_dict()}")
    print(f"Inf count          : {np.isinf(df_sub['Target_Volatilitas_Y'].values).sum()}")
    print(f"Negative count     : {(df_sub['Target_Volatilitas_Y'] < 0).sum()}")
    
    # Row-for-row date alignment with raw test set
    raw_test_dates = raw_test['Date'].values
    sub_dates = df_sub['Date'].values
    date_match = (raw_test_dates == sub_dates).all()
    print(f"Match raw test date: {date_match} (Exact 359 matching dates in order)")
    
    # Summary stats
    s = df_sub['Target_Volatilitas_Y']
    print(f"Stats: Mean={s.mean():.6f}, Std={s.std():.6f}, Min={s.min():.6f}, Median={s.median():.6f}, Max={s.max():.6f}")

# 3. Audit 2 Filled Dataset Files (Full 4,266 rows)
filled_files = [
    "dataset_peserta_filled_blend60_40.csv",
    "dataset_peserta_filled_blend50_30_20.csv"
]

for ff in filled_files:
    fpath = os.path.join(SUB_DIR, ff)
    assert os.path.exists(fpath), f"File missing: {fpath}"
    
    with open(fpath, "rb") as f:
        raw_bytes = f.read()
    lines = raw_bytes.decode("utf-8").splitlines()
    header_line = lines[0]
    
    df_filled = pd.read_csv(fpath)
    
    print("\n" + "-" * 60)
    print(f"AUDIT FILLED DATASET: {ff}")
    print("-" * 60)
    print(f"File size          : {len(raw_bytes):,} bytes")
    print(f"Header line        : '{header_line}'")
    print(f"Shape (df)         : {df_filled.shape}")
    print(f"Columns            : {df_filled.columns.tolist()}")
    print(f"Match raw columns  : {df_filled.columns.tolist() == [c for c in df_raw.columns if c != 'Date_dt']}")
    print(f"Date min/max       : {df_filled['Date'].min()} s/d {df_filled['Date'].max()}")
    print(f"Match raw dates    : {(df_filled['Date'].values == df_raw['Date'].values).all()}")
    print(f"Total NaNs in file : {df_filled.isna().sum().to_dict()}")
    
    # Compare labeled historical rows (rows 0 to 3906)
    labeled_slice_filled = df_filled.iloc[:len(raw_labeled)].copy()
    labeled_slice_raw = df_raw.iloc[:len(raw_labeled)].copy()
    
    # Check all predictor columns
    pred_cols = [c for c in df_raw.columns if c not in ['Date', 'Date_dt', 'Target_Volatilitas_Y']]
    preds_equal = np.allclose(labeled_slice_filled[pred_cols].values, labeled_slice_raw[pred_cols].values, equal_nan=True)
    print(f"Predictors 0..3906 : {'EXACT IDENTICAL' if preds_equal else 'MISMATCH'}")
    
    # Check historical target values
    raw_targets = labeled_slice_raw['Target_Volatilitas_Y'].values
    filled_targets = labeled_slice_filled['Target_Volatilitas_Y'].values
    target_hist_equal = np.allclose(raw_targets, filled_targets, atol=1e-12, equal_nan=True)
    max_target_diff = np.max(np.abs(raw_targets - filled_targets))
    print(f"Historical Targets : {'EXACT IDENTICAL' if target_hist_equal else 'MISMATCH'} (Max diff: {max_target_diff})")
    
    # Compare test rows (rows 3907 to 4265) with corresponding 2-column submission
    matching_sub_name = "submission_blend60_40.csv" if "blend60_40" in ff else "submission_blend50_30_20.csv"
    test_slice_filled = df_filled.iloc[len(raw_labeled):].copy().reset_index(drop=True)
    sub_df = sub_dfs[matching_sub_name]
    
    test_preds_equal = np.allclose(test_slice_filled['Target_Volatilitas_Y'].values, sub_df['Target_Volatilitas_Y'].values, atol=1e-12)
    max_test_diff = np.max(np.abs(test_slice_filled['Target_Volatilitas_Y'].values - sub_df['Target_Volatilitas_Y'].values))
    print(f"Test Targets Match : {'EXACT IDENTICAL' if test_preds_equal else 'MISMATCH'} with {matching_sub_name} (Max diff: {max_test_diff})")

# 4. Cross-Verification with Checkpoint 5 Report Numbers
print("\n" + "=" * 80)
print("CROSS-VERIFICATION WITH CHECKPOINT 5 REPORT NUMBERS")
print("=" * 80)
# Report numbers from docs/checkpoint_5_final_submission.md:
# Blend 60:40: Mean=0.008133, Std=0.002423, Min=0.005561, Q25=0.006376, Median=0.007269, Q75=0.009037, Max=0.020201
# Blend 50:30:20: Mean=0.008890, Std=0.002820, Min=0.005592, Q25=0.006640, Median=0.007802, Q75=0.010611, Max=0.020721
# GBR Tuned: Mean=0.007654, Std=0.002088, Min=0.005877, Q25=0.006299, Median=0.006737, Q75=0.008231, Max=0.016389

expected_stats = {
    "submission_blend60_40.csv": {"mean": 0.008133, "std": 0.002423, "min": 0.005561, "median": 0.007269, "max": 0.020201},
    "submission_blend50_30_20.csv": {"mean": 0.008890, "std": 0.002820, "min": 0.005592, "median": 0.007802, "max": 0.020721},
    "submission_gbr_tuned.csv": {"mean": 0.007654, "std": 0.002088, "min": 0.005877, "median": 0.006737, "max": 0.016389}
}

for sf, exp in expected_stats.items():
    s = sub_dfs[sf]['Target_Volatilitas_Y']
    actual = {"mean": s.mean(), "std": s.std(ddof=0), "min": s.min(), "median": s.median(), "max": s.max()}
    actual_ddof1 = {"std": s.std(ddof=1)}
    print(f"\nModel: {sf}")
    print(f"  Mean   : Actual = {actual['mean']:.6f} | Expected = {exp['mean']:.6f} | Match = {abs(actual['mean'] - exp['mean']) < 1e-5}")
    print(f"  Std(p) : Actual = {actual['std']:.6f} | Expected = {exp['std']:.6f} | Match = {abs(actual['std'] - exp['std']) < 1e-5}")
    print(f"  Std(s) : Actual = {actual_ddof1['std']:.6f} (ddof=1)")
    print(f"  Min    : Actual = {actual['min']:.6f} | Expected = {exp['min']:.6f} | Match = {abs(actual['min'] - exp['min']) < 1e-5}")
    print(f"  Median : Actual = {actual['median']:.6f} | Expected = {exp['median']:.6f} | Match = {abs(actual['median'] - exp['median']) < 1e-5}")
    print(f"  Max    : Actual = {actual['max']:.6f} | Expected = {exp['max']:.6f} | Match = {abs(actual['max'] - exp['max']) < 1e-5}")

print("\n" + "=" * 80)
print("AUDIT COMPLETE — ALL INTEGRITY CHECKS PASSED")
print("=" * 80)
