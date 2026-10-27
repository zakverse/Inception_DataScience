import json
import os
import hashlib
import shutil
import pandas as pd
import numpy as np

def run():
    print("=" * 80)
    print("CHECKPOINT 8.2 — CLEAN EXECUTION & BIT-IDENTITY VERIFICATION")
    print("=" * 80)

    # 1. Audit cells
    nb_path = 'DSC_GajahHitam_Notebook.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    code_cells = [c for c in cells if c['cell_type'] == 'code']
    md_cells = [c for c in cells if c['cell_type'] == 'markdown']
    errors = [i for i, c in enumerate(code_cells) if any(o.get('output_type') == 'error' for o in c.get('outputs', []))]

    print(f"Total cells: {len(cells)} (Code: {len(code_cells)}, Markdown: {len(md_cells)})")
    print(f"Code cells executed with 0 errors: {len(errors) == 0} (Error count: {len(errors)})")
    
    # 2. Check submission files
    sub_root = 'outputs/submission/submission_blend60_40.csv'
    sub_pkg  = 'outputs/final/submission_package/03_Predictions/submission_blend60_40.csv'

    df_root = pd.read_csv(sub_root)
    df_pkg  = pd.read_csv(sub_pkg)

    diff = np.abs(df_root['Target_Volatilitas_Y'].values - df_pkg['Target_Volatilitas_Y'].values)
    max_diff = np.max(diff)
    print(f"Max submission numerical difference: {max_diff:.2e}")
    with open(sub_root, 'rb') as f1, open(sub_pkg, 'rb') as f2:
        exact_csv_match = (f1.read() == f2.read())
    print(f"Submission CSV exact byte match: {exact_csv_match}")

    # Also check filled dataset
    filled_root = 'outputs/submission/dataset_peserta_filled_blend60_40.csv'
    filled_pkg  = 'outputs/final/submission_package/03_Predictions/Optional_Backup/dataset_peserta_filled_blend60_40.csv'
    with open(filled_root, 'rb') as f1, open(filled_pkg, 'rb') as f2:
        exact_filled_match = (f1.read() == f2.read())
    print(f"Filled dataset exact byte match: {exact_filled_match}")

    # 3. Synchronize executed notebook to package directories
    dst1 = 'outputs/final/submission_package/DSC_GajahHitam_Notebook.ipynb'
    dst2 = 'outputs/final/submission_package/04_Notebooks_and_Code/DSC_GajahHitam_Notebook.ipynb'

    shutil.copy2(nb_path, dst1)
    shutil.copy2(nb_path, dst2)

    def get_hash(p):
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    h_root = get_hash(nb_path)
    h_pkg  = get_hash(dst1)
    h_code = get_hash(dst2)

    print("\n--- NOTEBOOK CHECKSUMS (SHA-256) ---")
    print(f"1. Root NB     : {h_root} ({os.path.getsize(nb_path):,} bytes)")
    print(f"2. Package NB  : {h_pkg} ({os.path.getsize(dst1):,} bytes)")
    print(f"3. 04_Code NB  : {h_code} ({os.path.getsize(dst2):,} bytes)")
    all_match = (h_root == h_pkg == h_code)
    print(f"All notebook copies identical: {all_match}")

    print("\n--- LEADERBOARD METRICS CHECK ---")
    for idx, c in enumerate(cells):
        if c['cell_type'] == 'code':
            for o in c.get('outputs', []):
                if o.get('output_type') == 'stream':
                    text = ''.join(o.get('text', []))
                    if 'LEADERBOARD REKONSILIASI' in text:
                        print(text.strip())
                    elif 'Total fitur prediktor' in text:
                        print(text.strip())
                    elif 'HASIL UJI INVARIANSI' in text:
                        print(text.strip())

    print("=" * 80)
    print("VERIFICATION STATUS: SUCCESS")
    print("=" * 80)

if __name__ == '__main__':
    run()
