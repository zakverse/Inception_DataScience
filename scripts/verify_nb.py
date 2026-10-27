import os, json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
path = os.path.join(PROJECT_ROOT, "notebook", "EDA.ipynb")

nb = json.load(open(path, encoding="utf-8"))
cells = nb["cells"]

code_cells = [c for c in cells if c["cell_type"] == "code"]
executed = [c for c in code_cells if c.get("execution_count") is not None]

errors = []
for i, c in enumerate(cells):
    if c["cell_type"] == "code":
        for out in c.get("outputs", []):
            if out.get("output_type") == "error":
                errors.append((i, out.get("ename", ""), out.get("evalue", "")))

print(f"Total cells      : {len(cells)}")
print(f"Code cells       : {len(code_cells)}")
print(f"Executed cells   : {len(executed)}")
print(f"Error cells      : {len(errors)}")
for idx, ename, evalue in errors:
    print(f"  Cell {idx}: {ename}: {evalue[:120]}")

outputs_eda = os.path.join(PROJECT_ROOT, "outputs", "eda")
figs = sorted([f for f in os.listdir(outputs_eda) if f.endswith(".png")])
print(f"\nFigures in outputs/eda/ : {len(figs)}")
for f in figs:
    size = os.path.getsize(os.path.join(outputs_eda, f))
    print(f"  {f}  ({size:,} bytes)")

