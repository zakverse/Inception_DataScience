import os
import json
import pandas as pd

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '06_Reconciliation_Audit.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

c8 = nb['cells'][8]
for out in c8.get('outputs', []):
    if 'text' in out:
        print("".join(out['text']))
