import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'
nb_path = os.path.join(PROJECT_ROOT, 'notebook', '06_Reconciliation_Audit.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

c8 = nb['cells'][8] # 0-indexed cell 8
print("".join(c8['source']))
