import os
import sys
import json
import pandas as pd
import numpy as np

PROJECT_ROOT = r'z:\Projects\Inception'

def check_metrics_reconciliation():
    print("=== 1. CHECKING RECONCILIATION & VALIDATION METRICS ===")
    # Load 06_Reconciliation_Audit.ipynb outputs if available
    nb_path = os.path.join(PROJECT_ROOT, 'notebook', '06_Reconciliation_Audit.ipynb')
    if os.path.exists(nb_path):
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        print(f"Found {nb_path}, total cells: {len(nb['cells'])}")
        for i, c in enumerate(nb['cells']):
            if c['cell_type'] == 'code':
                for out in c.get('outputs', []):
                    if 'text' in out:
                        txt = "".join(out['text'])
                        if 'POOLED' in txt or 'Blend 60:40' in txt or 'GBR Tuned' in txt:
                            print(f"--- Output from Cell {i} ---")
                            print(txt[:1000])
                            print("-----------------------------")

def check_submission_files():
    print("\n=== 2. CHECKING SUBMISSION CSV STATS ===")
    sub_dir = os.path.join(PROJECT_ROOT, 'outputs', 'submission')
    files = [
        'submission_blend60_40.csv',
        'submission_blend50_30_20.csv',
        'submission_gbr_tuned.csv',
        'dataset_peserta_filled_blend60_40.csv',
        'dataset_peserta_filled_blend50_30_20.csv'
    ]
    for fn in files:
        fp = os.path.join(sub_dir, fn)
        if os.path.exists(fp):
            df = pd.read_csv(fp)
            size = os.path.getsize(fp)
            print(f"\nFile: {fn} (Size: {size} bytes)")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"Date min: {df['Date'].min()} | max: {df['Date'].max()}")
            if 'Target_Volatilitas_Y' in df.columns:
                target_col = df['Target_Volatilitas_Y']
                if len(df) == 359:
                    s = target_col
                else:
                    # filled file, examine test part (last 359 rows)
                    s = df.iloc[-359:]['Target_Volatilitas_Y']
                print(f"Stats (Test 359 rows):")
                print(f"  Mean   : {s.mean():.6f}")
                print(f"  Std(ddof=0): {s.std(ddof=0):.6f} | Std(ddof=1): {s.std(ddof=1):.6f}")
                print(f"  Min    : {s.min():.6f}")
                print(f"  25%    : {s.quantile(0.25):.6f}")
                print(f"  Median : {s.median():.6f}")
                print(f"  75%    : {s.quantile(0.75):.6f}")
                print(f"  Max    : {s.max():.6f}")
                print(f"  NaNs   : {s.isna().sum()} | Infs: {np.isinf(s).sum()} | Negs: {(s < 0).sum()}")

if __name__ == '__main__':
    check_metrics_reconciliation()
    check_submission_files()
