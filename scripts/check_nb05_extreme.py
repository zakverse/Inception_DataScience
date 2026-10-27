import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '05_Robustness_Model_Selection.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        for out in c.get('outputs', []):
            if 'text' in out:
                txt = "".join(out['text'])
                if 'Ekstrem' in txt or '0.007584' in txt or '0.007604' in txt or 'Top 5%' in txt:
                    print(f"--- Notebook 05 Cell {i} ---")
                    print(txt[:1000])
                    print("-----------------------------")
