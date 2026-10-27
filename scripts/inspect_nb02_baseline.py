import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '02_Validation_Baseline.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        for out in c.get('outputs', []):
            if 'text' in out:
                txt = "".join(out['text'])
                if 'rv_past5' in txt or 'Baseline' in txt or 'MAE' in txt:
                    print(f"--- Notebook 02 Cell {i} ---")
                    print(txt[:1000])
                    print("-----------------------------")
