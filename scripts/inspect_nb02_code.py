import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '02_Validation_Baseline.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        source = "".join(c['source'])
        if 'rv_past5' in source or 'Cell 10' in str(idx) or idx in [8, 9, 10, 11, 12, 13, 14]:
            print(f"=== CELL INDEX {idx} ===")
            print(source[:1500])
            for out in c.get('outputs', []):
                if 'text' in out:
                    print("--- OUTPUT ---")
                    print("".join(out['text'])[:1000])
