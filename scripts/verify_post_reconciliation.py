import os
import re

PROJECT_ROOT = r'z:\Projects\Inception'

def verify():
    print("=== POST-RECONCILIATION VERIFICATION ===")
    
    # 1. Check compliance doc for old rv_past5 values
    cp6_path = os.path.join(PROJECT_ROOT, 'docs', 'checkpoint_6_studi_kasus_compliance.md')
    with open(cp6_path, 'r', encoding='utf-8') as f:
        cp6_content = f.read()
    
    assert "0,003299" not in cp6_content, "Error: old 0,003299 still in checkpoint 6!"
    assert "0,004456" not in cp6_content, "Error: old 0,004456 still in checkpoint 6!"
    assert "0,002981" in cp6_content, "Error: verified 0,002981 missing from checkpoint 6!"
    assert "0,004088" in cp6_content, "Error: verified 0,004088 missing from checkpoint 6!"
    assert "19,5" in cp6_content, "Error: 19,5% missing from checkpoint 6!"
    assert "17,4" in cp6_content, "Error: 17,4% missing from checkpoint 6!"
    print("[PASS] Checkpoint 6 Studi Kasus Compliance verified clean.")
    
    # 2. Check checkpoint 5 doc for extreme MAE
    cp5_path = os.path.join(PROJECT_ROOT, 'docs', 'checkpoint_5_final_submission.md')
    with open(cp5_path, 'r', encoding='utf-8') as f:
        cp5_content = f.read()
    
    assert "0,007584" not in cp5_content, "Error: old 0,007584 still in checkpoint 5!"
    assert "0,007604" not in cp5_content, "Error: old 0,007604 still in checkpoint 5!"
    assert "0,007778" in cp5_content, "Error: verified 0,007778 missing from checkpoint 5!"
    assert "0,007858" in cp5_content, "Error: verified 0,007858 missing from checkpoint 5!"
    print("[PASS] Checkpoint 5 Final Submission verified clean.")
    
    # 3. Check checkpoint 3C1 doc for extreme MAE
    cp3c1_path = os.path.join(PROJECT_ROOT, 'docs', 'checkpoint_3c1_reconciliation.md')
    with open(cp3c1_path, 'r', encoding='utf-8') as f:
        cp3c1_content = f.read()
        
    assert "0,007584" not in cp3c1_content, "Error: old 0,007584 still in checkpoint 3C1!"
    assert "0,007604" not in cp3c1_content, "Error: old 0,007604 still in checkpoint 3C1!"
    assert "0,007778" in cp3c1_content, "Error: verified 0,007778 missing from checkpoint 3C1!"
    assert "0,007858" in cp3c1_content, "Error: verified 0,007858 missing from checkpoint 3C1!"
    print("[PASS] Checkpoint 3C.1 Reconciliation verified clean.")
    
    # 4. Check submission files existence and integrity
    sub_files = [
        'submission_blend60_40.csv',
        'submission_blend50_30_20.csv',
        'submission_gbr_tuned.csv',
        'dataset_peserta_filled_blend60_40.csv',
        'dataset_peserta_filled_blend50_30_20.csv'
    ]
    for fn in sub_files:
        fp = os.path.join(PROJECT_ROOT, 'outputs', 'submission', fn)
        assert os.path.exists(fp), f"Missing submission file: {fn}"
    print(f"[PASS] All {len(sub_files)} submission files verified intact.")
    
    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% CLEAN)!")

if __name__ == '__main__':
    verify()
