import nbformat
import hashlib
import os

nb_path = 'DSC_GajahHitam_Notebook.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

code_cells = [c for c in nb.cells if c.cell_type == 'code']
md_cells   = [c for c in nb.cells if c.cell_type == 'markdown']

print("=" * 80)
print(f"VERIFIKASI EKSEKUSI NOTEBOOK: {nb_path}")
print("=" * 80)
print(f"Total Sel    : {len(nb.cells)} sel (Markdown: {len(md_cells)}, Code: {len(code_cells)})")
print(f"Ukuran Berkas: {os.path.getsize(nb_path):,} bytes")

has_error = False
total_images = 0

for i, c in enumerate(code_cells):
    ec = c.get('execution_count')
    outputs = c.get('outputs', [])
    errs = [o for o in outputs if o.get('output_type') == 'error']
    img_count = sum(1 for o in outputs if 'data' in o and 'image/png' in o['data'])
    txt_streams = [o for o in outputs if o.get('output_type') == 'stream']
    total_images += img_count
    
    first_line = c.source.strip().split('\n')[0] if c.source.strip() else 'Empty'
    if errs:
        has_error = True
        ename = errs[0].get('ename', 'UnknownError')
        evalue = errs[0].get('evalue', '')
        print(f"Sel Code {i+1:2d} [ERROR] Execution #{ec}: {ename}: {evalue}")
    else:
        sample_txt = txt_streams[0].text.strip().split('\n')[0] if txt_streams else 'No stream'
        print(f"Sel Code {i+1:2d} [PASS] Exec #{ec:2d} | Img: {img_count} | Out: {len(outputs)} | First line: {first_line[:40]}... -> {sample_txt[:35]}")

print("=" * 80)
print(f"Total Visualisasi Inline Ter-render: {total_images} grafik.")
if not has_error:
    print("STATUS VERIFIKASI: 100% SUKSES BERSIH TANPA KESALAHAN (CLEAN EXECUTION PASS)")
else:
    print("STATUS VERIFIKASI: GAGAL")
print("=" * 80)

print("\n" + "=" * 80)
print("RINCIAN KELUARAN TEKS SELURUH SEL EKSEKUSI:")
print("=" * 80)
for i, c in enumerate(code_cells):
    print(f"\n--- [SEL CODE {i+1:2d} | EXECUTION #{c.get('execution_count')}] ---")
    for o in c.get('outputs', []):
        if o.get('output_type') == 'stream':
            print(o.get('text', '').strip())

