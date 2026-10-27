import os
import json

PROJECT_ROOT = r'z:\Projects\Inception'

def search_text(target):
    print(f"Searching for {target}...")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for f in files:
            if f.endswith(('.py', '.ipynb', '.md', '.txt')):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        if target in content:
                            print(f"Found in: {p}")
                except Exception as e:
                    pass

search_text("0.007584")
search_text("0,007584")
search_text("0.007604")
search_text("0,007604")
