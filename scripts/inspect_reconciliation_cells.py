import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '06_Reconciliation_Audit.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in [4, 6, 8, 10]:
    if i < len(nb['cells']):
        c = nb['cells'][i]
        print(f"================ CELL {i} ================")
        for out in c.get('outputs', []):
            if 'text' in out:
                print("".join(out['text']))
