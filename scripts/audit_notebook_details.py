import json
import os
import hashlib

def run():
    nb_path = 'DSC_GajahHitam_Notebook.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    code_cells = [c for c in cells if c['cell_type'] == 'code']
    md_cells = [c for c in cells if c['cell_type'] == 'markdown']

    print(f"Total cells: {len(cells)}")
    print(f"Code cells: {len(code_cells)}, Markdown cells: {len(md_cells)}")

    file_size = os.path.getsize(nb_path)
    with open(nb_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
    print(f"SHA256: {sha256}")

    print("\n--- CELL BREAKDOWN ---")
    c_idx = 0
    m_idx = 0
    for idx, c in enumerate(cells):
        ctype = c['cell_type']
        if ctype == 'code':
            c_idx += 1
            exc = c.get('execution_count')
            outs = c.get('outputs', [])
            has_err = any(o.get('output_type') == 'error' for o in outs)
            types = [o.get('output_type') for o in outs]
            first_line = c['source'][0].strip() if c['source'] else ''
            print(f"Cell {idx+1:02d} [CODE #{c_idx:02d}] (exec: {exc}): {len(c['source'])} lines | outputs: {len(outs)} {types} | error: {has_err} | {first_line[:60]}")
        else:
            m_idx += 1
            first_line = c['source'][0].strip() if c['source'] else ''
            print(f"Cell {idx+1:02d} [MARKDOWN #{m_idx:02d}]: {len(c['source'])} lines | {first_line[:60]}")

if __name__ == '__main__':
    run()
