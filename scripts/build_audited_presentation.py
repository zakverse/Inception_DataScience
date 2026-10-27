# -*- coding: utf-8 -*-
"""
INCEPTION 2026 - FINAL AUDITED EDITORIAL QUANTITATIVE RISK PRESENTATION BUILDER
Checkpoint 7.1 Accuracy & Traceability Reconciliation
Target Output: outputs/final/INCEPTION_2026_GajahHitam_PPT_Final_Audit.pptx
Format: 16:9 Widescreen (13.333 x 7.5 inches)
Slide Count: Exactly 15 slides
Strict Rules:
- 100% reconciled numbers from Checkpoint 6.1 and Checkpoint 6.3.
- Slide 4: Target stats from labeled 3.887 days (Mean 0.00834, Median 0.00705, Skewness +2.636, Kurtosis +12.213).
- Slide 8 & 10: Ridge Tuned (Pooled MAE 0.002471, RMSE 0.003287, Fold 3 0.002824, Extreme MAE 0.007683).
- Slide 12: 11 May 2022 from Notebook 07 Cell 6 (Actual 0.019739, Pred Blend 0.012739, GBR 0.012095, Ridge 0.013705).
- Slide 13: Checkpoint 6.1 exact numbers:
    * 31 July 2024: Actual 0.019251, Pred 0.005825, Residual +0.013426, Abs Error 0.013426.
    * 5 August 2024: Actual 0.005503, Pred 0.012314, Residual -0.006811, Abs Error 0.006811.
    * Naive Baseline 5 Aug: Pred 0.016621, Abs Error 0.011118 (Blend 60:40 error is 38.7% lower).
- Slide 14: Asset allocation labeled explicitly as Policy Proposals (Usulan Kebijakan Komite Risiko), not empirically backtested findings.
- Do NOT overwrite previous remake PPT.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = r'z:\Projects\Inception'
OUTPUT_PPTX = os.path.join(PROJECT_ROOT, 'outputs', 'final', 'INCEPTION_2026_GajahHitam_PPT_Final_Audit.pptx')

# =============================================================================
# INSTITUTIONAL COLOR PALETTE
# =============================================================================
NAVY_PRIMARY    = RGBColor(11, 25, 44)       # #0B192C - Deep Midnight Navy (Authoritative)
NAVY_DEEP       = RGBColor(15, 23, 42)       # #0F172A - Rich Slate Navy
NAVY_CARD       = RGBColor(24, 38, 62)       # #18263E - Dark Card Background for Dark Slides
WHITE           = RGBColor(255, 255, 255)    # #FFFFFF - Crisp Surface
CANVAS_BG       = RGBColor(248, 250, 252)    # #F8FAFC - Editorial Off-White Slide Canvas
SLATE_DARK      = RGBColor(30, 41, 59)       # #1E293B - Headings & High Contrast Text
SLATE_BODY      = RGBColor(51, 65, 85)       # #334155 - Body Prose Text
SLATE_MUTED     = RGBColor(100, 116, 139)    # #64748B - Metadata, Footnotes, Captions
BORDER_SUBTLE   = RGBColor(226, 232, 240)    # #E2E8F0 - Fine Hairlines & Dividers
BORDER_CARD     = RGBColor(203, 213, 225)    # #CBD5E1 - Structural Borders
TEAL_PRIMARY    = RGBColor(13, 148, 136)     # #0D9488 - Institutional Teal (Outperformance & Verifications)
TEAL_DARK       = RGBColor(15, 118, 110)     # #0F766E - Deep Teal
TEAL_TINT       = RGBColor(240, 253, 250)    # #F0FDFA - Soft Teal Highlight Fill
AMBER_ACCENT    = RGBColor(217, 119, 6)      # #D97706 - Ochre Amber (Risk Warnings & Regimes)
AMBER_TINT      = RGBColor(254, 243, 199)    # #FEF3C7 - Soft Amber Wash
CRIMSON_ACCENT  = RGBColor(185, 28, 28)      # #B91C1C - Error / Loss / Critical Risk
CRIMSON_TINT    = RGBColor(254, 242, 242)    # #FEF2F2 - Soft Crimson Wash
TABLE_ZEBRA     = RGBColor(241, 245, 249)    # #F1F5F9 - Table Alternate Row Fill

def set_flat_style(shape, fill_color, border_color=None, border_width=1):
    """Applies flat color fill and crisp clean border."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()

def add_editorial_header(slide, tag_text, title_text, subtitle_text):
    """Creates a refined editorial header with tracking tag, title, and thesis subtitle."""
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.24))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.size = Pt(9.0)
    p_tag.font.bold = True
    p_tag.font.color.rgb = TEAL_PRIMARY

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.42))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(19.5)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.12), Inches(11.733), Inches(0.28))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = SLATE_MUTED

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Pt(1))
    set_flat_style(line, BORDER_SUBTLE, border_color=None)

def add_editorial_footer(slide, current_slide, total_slides=15):
    """Creates a consistent, low-profile institutional footer."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Pt(1))
    set_flat_style(line, BORDER_SUBTLE, border_color=None)

    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.5), Inches(0.25))
    tf_l = foot_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "INCEPTION 2026 Data Science Competition | Tim GajahHitam — PT Investion Quantitative Risk Division"
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = SLATE_MUTED

    foot_right = slide.shapes.add_textbox(Inches(9.5), Inches(7.08), Inches(3.033), Inches(0.25))
    tf_r = foot_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} dari {total_slides}"
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = NAVY_PRIMARY

def add_framed_image(slide, img_path, left, top, width, height, caption=None):
    """Embeds an image inside an elegant editorial card with caption."""
    abs_path = os.path.abspath(img_path)
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    set_flat_style(card, WHITE, BORDER_SUBTLE, 1)

    cap_height = Inches(0.28) if caption else Inches(0)
    img_pad = Inches(0.08)

    if os.path.exists(abs_path):
        img_left = left + img_pad
        img_top = top + img_pad
        img_w = width - (img_pad * 2)
        img_h = height - (img_pad * 2) - cap_height
        slide.shapes.add_picture(abs_path, img_left, img_top, img_w, img_h)
    else:
        tb = slide.shapes.add_textbox(left, top, width, height - cap_height)
        p = tb.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"[Grafik Tidak Ditemukan: {os.path.basename(img_path)}]"
        p.font.size = Pt(10)
        p.font.color.rgb = CRIMSON_ACCENT

    if caption:
        cap_box = slide.shapes.add_textbox(left, top + height - cap_height - Inches(0.04), width, cap_height)
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = caption
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE_MUTED
        p.font.italic = True

def add_table_styled(slide, left, top, width, height, headers, rows_data, col_widths=None, align_right_cols=[]):
    """Creates a clean institutional data table with crisp borders, clear header, and zebra striping."""
    n_rows = len(rows_data) + 1
    n_cols = len(headers)
    table_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    tbl = table_shape.table

    if col_widths and len(col_widths) == n_cols:
        for idx, w in enumerate(col_widths):
            tbl.columns[idx].width = w

    # Header Row
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = WHITE
        if c_idx in align_right_cols:
            p.alignment = PP_ALIGN.RIGHT
        else:
            p.alignment = PP_ALIGN.LEFT

    # Data Rows
    for r_idx, row in enumerate(rows_data):
        row_num = r_idx + 1
        bg_col = TABLE_ZEBRA if (r_idx % 2 == 1) else WHITE
        for c_idx, val in enumerate(row):
            cell = tbl.cell(row_num, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(8.5)
            p.font.color.rgb = SLATE_DARK
            if c_idx in align_right_cols:
                p.alignment = PP_ALIGN.RIGHT
                p.font.bold = True if c_idx == len(headers) - 1 else False
            else:
                p.alignment = PP_ALIGN.LEFT

    return table_shape

def build_audited_presentation():
    print("=" * 70)
    print("BUILDING FINAL AUDITED PRESENTATION DECK (CHECKPOINT 7.1)")
    print(f"Target file: {OUTPUT_PPTX}")
    print("=" * 70)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER & TITLE (Dark Navy Institutional Elegance)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    set_flat_style(bg1, NAVY_PRIMARY, border_color=None)

    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
    set_flat_style(accent_bar, TEAL_PRIMARY, border_color=None)

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.15), Inches(5.8), Inches(0.38))
    set_flat_style(badge, NAVY_CARD, border_color=TEAL_PRIMARY, border_width=1)
    p_b = badge.text_frame.paragraphs[0]
    p_b.text = "INCEPTION 2026 DATA SCIENCE COMPETITION  •  FINANCIAL TRACK"
    p_b.font.size = Pt(9.0)
    p_b.font.bold = True
    p_b.font.color.rgb = TEAL_PRIMARY
    p_b.alignment = PP_ALIGN.CENTER

    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(1.3))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Sistem Peringatan Dini Realized Volatility IHSG"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE
    
    p_sub = tf_t.add_paragraph()
    p_sub.text = "Arsitektur Regresi Prediktif 5-Hari Forward dan Dekomposisi Explainable AI (SHAP) dalam Mengawal Portofolio Triliunan Rupiah"
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_sub.space_before = Pt(8)

    line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.45), Inches(11.333), Pt(1))
    set_flat_style(line1, RGBColor(51, 65, 85), border_color=None)

    meta_items = [
        ("TIM PENGEMBANG", "Tim GajahHitam", "Peserta Resmi Babak Penyisihan"),
        ("PERAN INSTITUSI", "Senior Quantitative Risk Analyst", "Divisi Manajemen Risiko PT Investion"),
        ("TARGET PREDIKSI", "Target_Volatilitas_Y", "Realized Volatility IHSG [t+1 .. t+5]"),
        ("STATUS AUDIT", "100% Bebas Kebocoran", "Rekonsiliasi Lengkap Checkpoint 7.1")
    ]
    card_w = Inches(2.65)
    for i, (m_tag, m_val, m_sub) in enumerate(meta_items):
        c_left = Inches(1.0) + (i * Inches(2.88))
        card_m = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(3.8), card_w, Inches(2.2))
        set_flat_style(card_m, NAVY_CARD, border_color=RGBColor(30, 41, 59), border_width=1)
        
        tb_m = s1.shapes.add_textbox(c_left + Inches(0.18), Inches(3.95), card_w - Inches(0.36), Inches(1.9))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p1 = tf_m.paragraphs[0]
        p1.text = m_tag
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY
        
        p2 = tf_m.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(6)
        
        p3 = tf_m.add_paragraph()
        p3.text = m_sub
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = RGBColor(148, 163, 184)
        p3.space_before = Pt(6)

    tb_foot1 = s1.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.35))
    p_df = tb_foot1.text_frame.paragraphs[0]
    p_df.text = "Kompetisi Sains Data INCEPTION 2026 | Financial Time Series Track | Jakarta, Oktober 2026"
    p_df.font.size = Pt(9.5)
    p_df.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY (Problem, Solution, Key Results)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s2, "01 / Konteks Eksekutif",
                         "Tesis Eksekutif: Mengawal Portofolio Triliunan di Tengah Turbulensi Pasar",
                         "Mengganti estimasi historis yang reaktif dengan sistem proyeksi volatilitas 5-hari forward yang akuntabel dan transparan.")
    add_editorial_footer(s2, 2)

    # 3 Analytical Columns: Problem, Solution, Results
    p1_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.0))
    set_flat_style(p1_box, WHITE, BORDER_SUBTLE, 1)
    
    p1_tag = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(3.7), Inches(0.45))
    set_flat_style(p1_tag, CRIMSON_ACCENT, border_color=None)
    tb = s2.shapes.add_textbox(Inches(0.95), Inches(1.78), Inches(3.4), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = "TANTANGAN & MASALAH BISNIS"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_p1 = s2.shapes.add_textbox(Inches(0.95), Inches(2.3), Inches(3.4), Inches(4.2))
    tf = tb_p1.text_frame
    tf.word_wrap = True
    bullets_p1 = [
        ("Eksposur Triliunan Rupiah:", "Portofolio ekuitas PT Investion di pasar berkembang (emerging market) sangat rentan terhadap penularan risiko makro global dan capital outflow masif."),
        ("Kelemahan Estimator Naif:", "Estimator varians historis masa lalu bersifat lagging murni. Sinyal bahaya baru melonjak setelah koreksi harga terjadi dan NAB portofolio terlanjur tergerus."),
        ("Mandat Anti-Black Box:", "Direksi dan Komite Risiko melarang penggunaan model kotak hitam untuk keputusan bernilai triliunan. Setiap peringatan wajib memiliki atribusi faktor yang dapat diaudit.")
    ]
    for b_title, b_desc in bullets_p1:
        p_t = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p_t.text = f"• {b_title}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_d = tf.add_paragraph()
        p_d.text = b_desc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = SLATE_BODY
        p_d.space_after = Pt(10)

    p2_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.0))
    set_flat_style(p2_box, WHITE, BORDER_SUBTLE, 1)
    
    p2_tag = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.8), Inches(1.7), Inches(3.7), Inches(0.45))
    set_flat_style(p2_tag, TEAL_DARK, border_color=None)
    tb2 = s2.shapes.add_textbox(Inches(4.95), Inches(1.78), Inches(3.4), Inches(0.3))
    p = tb2.text_frame.paragraphs[0]
    p.text = "ARSITEKTUR SOLUSI KUANTITATIF"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_p2 = s2.shapes.add_textbox(Inches(4.95), Inches(2.3), Inches(3.4), Inches(4.2))
    tf2 = tb_p2.text_frame
    tf2.word_wrap = True
    bullets_p2 = [
        ("Sinyal Makro Orisinal (X1, X2, X3):", "Merancang 3 fitur inovatif yang menangkap kepanikan likuiditas valas, disparitas suku bunga BI-Fed, dan guncangan harga komoditas sebelum merambat ke IHSG."),
        ("Protokol Anti-Kebocoran:", "Menerapkan expanding walk-forward 3-fold dengan purging horizon H=5 hari bursa, menjamin estimasi out-of-fold murni tanpa kontaminasi masa depan."),
        ("Ensemble Ter-regularisasi:", "Menggabungkan Gradient Boosting (GBR 60%) untuk interaksi non-linier dan Ridge Regression (40%) untuk kestabilan estimasi ekstrim.")
    ]
    for b_title, b_desc in bullets_p2:
        p_t = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
        p_t.text = f"• {b_title}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_d = tf2.add_paragraph()
        p_d.text = b_desc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = SLATE_BODY
        p_d.space_after = Pt(10)

    p3_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(1.7), Inches(3.733), Inches(5.0))
    set_flat_style(p3_box, WHITE, BORDER_SUBTLE, 1)

    p3_tag = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(1.7), Inches(3.733), Inches(0.45))
    set_flat_style(p3_tag, NAVY_PRIMARY, border_color=None)
    tb3 = s2.shapes.add_textbox(Inches(8.95), Inches(1.78), Inches(3.4), Inches(0.3))
    p = tb3.text_frame.paragraphs[0]
    p.text = "HASIL KUNCI & BUKTI EMPIRIS"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = WHITE

    stats_c3 = [
        ("+19,5%", "Keunggulan Akurasi MAE", "Blend 60:40 (0,002401) melampaui baseline naif resmi rv_past5 (0,002981) dan unggul +10,2% vs persistensi."),
        ("0,00000", "Deviasi Uji Invariansi", "Mutasi noise acak data masa depan menghasilkan deviasi nol mutlak pada prediksi hari t (100% Zero Leakage)."),
        ("100% XAI", "Transparansi Faktor SHAP", "Setiap lonjakan volatilitas didekomposisi ke kontribusi fitur marjinal, memenuhi standar tata kelola komite risiko.")
    ]
    for s_idx, (s_val, s_lbl, s_sub) in enumerate(stats_c3):
        top_s = Inches(2.3) + (s_idx * Inches(1.48))
        s_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.95), top_s, Inches(3.433), Inches(1.35))
        set_flat_style(s_box, TEAL_TINT if s_idx == 0 else CANVAS_BG, border_color=BORDER_SUBTLE, border_width=1)
        
        tb_s = s2.shapes.add_textbox(Inches(9.1), top_s + Inches(0.08), Inches(3.133), Inches(1.2))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        
        p_val = tf_s.paragraphs[0]
        p_val.text = s_val
        p_val.font.size = Pt(16)
        p_val.font.bold = True
        p_val.font.color.rgb = TEAL_DARK if s_idx == 0 else NAVY_PRIMARY
        
        p_lbl = tf_s.add_paragraph()
        p_lbl.text = s_lbl
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = SLATE_DARK
        
        p_sub = tf_s.add_paragraph()
        p_sub.text = s_sub
        p_sub.font.size = Pt(8.0)
        p_sub.font.color.rgb = SLATE_BODY

    # =========================================================================
    # SLIDE 3: DATASET & TARGET VOLATILITAS 5 HARI FORWARD
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s3, "02 / Arsitektur Data Multivariat",
                         "Struktur Dataset Finansial & Horizon Target 5-Hari Forward",
                         "Pemisahan tegas antara 3.887 hari historis berlabel (2010–2024) dan 359 hari uji kompetisi murni out-of-sample (2025–2026).")
    add_editorial_footer(s3, 3)

    s3_left_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(5.0))
    set_flat_style(s3_left_box, WHITE, BORDER_SUBTLE, 1)

    tb_s3l = s3.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.6))
    tf_s3l = tb_s3l.text_frame
    tf_s3l.word_wrap = True

    p = tf_s3l.paragraphs[0]
    p.text = "1. Spesifikasi Deret Waktu Finansial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    bullets_s3_1 = [
        "Cakupan Total: 4.266 baris perdagangan bursa harian (Senin–Jumat, 2010 s/d 2026).",
        "Partisi Historis: 3.887 hari berlabel aktif (2010–2024) pasca pembersihan warm-up 20 hari.",
        "Partisi Uji Kompetisi: Tepat 359 hari bursa (2 Jan 2025 s/d 22 Mei 2026) dengan target NaN.",
        "10 Prediktor Makro: Kurs USD/IDR, S&P 500, CBOE VIX, Minyak WTI, Emas Spot, IHSG, CPI (Inflasi), BI Rate, US Fed Funds Rate."
    ]
    for b in bullets_s3_1:
        p = tf_s3l.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9.0)
        p.font.color.rgb = SLATE_BODY
        p.space_after = Pt(4)

    p_div = tf_s3l.add_paragraph()
    p_div.text = "2. Formulasi Target: Target_Volatilitas_Y"
    p_div.font.size = Pt(12)
    p_div.font.bold = True
    p_div.font.color.rgb = NAVY_PRIMARY
    p_div.space_before = Pt(10)

    bullets_s3_2 = [
        "Definisi Matematis: Realized Volatility harian IHSG untuk horizon 5 hari bursa ke depan [t+1 s/d t+5].",
        "Karakteristik Finansial: Bersifat forward-looking murni; tidak boleh disentuh selama ekstraksi fitur pada hari t.",
        "Status Data Uji 2025–2026: Merupakan data inferensi tanpa label, bukan data validasi berlabel yang telah diketahui akurasinya.",
        "Mandat Bebas Bocor: Sistem dibangun untuk mengantisipasi dinamika pasar tanpa pernah melihat data masa depan."
    ]
    for b in bullets_s3_2:
        p = tf_s3l.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9.0)
        p.font.color.rgb = SLATE_BODY
        p.space_after = Pt(4)

    add_framed_image(s3, 'outputs/eda/fig_03_timeseries_macro.png', Inches(6.0), Inches(1.7), Inches(6.533), Inches(5.0),
                     caption="Gambar 3.1: Ko-pergerakan Deret Waktu Finansial & Makroekonomi Historis (2010–2024)")

    # =========================================================================
    # SLIDE 4: EDA: FAT TAILS, VOLATILITY CLUSTERING, & REZIM PASAR
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s4, "03 / Analisis Data Eksploratif",
                         "Distribusi Leptokurtik, Ekor Tebal, & Fenomena Volatility Clustering",
                         "Pasar didominasi periode tenang (95%), namun rentan lonjakan krisis leptokurtik ekstrem (5%).")
    add_editorial_footer(s4, 4)

    # Top Metric Ribbon - Verified against notebook/EDA.ipynb (3.887 labeled days)
    ribbon_metrics = [
        ("MEAN TARGET (HISTORIS)", "0,00834", "Rata-rata volatilitas 5-hari historis"),
        ("MEDIAN TARGET (HISTORIS)", "0,00705", "Titik tengah distribusi target"),
        ("SKEWNESS", "+2,636", "Kemencengan positif (>1 right-skewed)"),
        ("EXCESS KURTOSIS", "+12,213", "Distribusi leptokurtik ekor sangat tebal")
    ]
    m_w = Inches(2.78)
    for idx, (m_l, m_v, m_s) in enumerate(ribbon_metrics):
        m_left = Inches(0.8) + (idx * Inches(2.98))
        m_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_left, Inches(1.65), m_w, Inches(1.05))
        set_flat_style(m_box, WHITE, BORDER_SUBTLE, 1)
        
        tb = s4.shapes.add_textbox(m_left + Inches(0.12), Inches(1.72), m_w - Inches(0.24), Inches(0.9))
        tf = tb.text_frame
        p_l = tf.paragraphs[0]
        p_l.text = m_l
        p_l.font.size = Pt(8.0)
        p_l.font.bold = True
        p_l.font.color.rgb = TEAL_PRIMARY
        
        p_v = tf.add_paragraph()
        p_v.text = m_v
        p_v.font.size = Pt(14)
        p_v.font.bold = True
        p_v.font.color.rgb = NAVY_PRIMARY
        
        p_s = tf.add_paragraph()
        p_s.text = m_s
        p_s.font.size = Pt(8.0)
        p_s.font.color.rgb = SLATE_MUTED

    s4_left = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.85), Inches(4.8), Inches(3.95))
    set_flat_style(s4_left, WHITE, BORDER_SUBTLE, 1)

    tb_s4 = s4.shapes.add_textbox(Inches(0.95), Inches(2.95), Inches(4.5), Inches(3.7))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True

    p = tf_s4.paragraphs[0]
    p.text = "Temuan Kuantitatif Karakteristik Risiko"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    eda_points = [
        ("Fat Tails & Asumsi Non-Gaussian:", "Excess kurtosis sebesar 12,213 membuktikan bahwa guncangan ekstrem (Covid-19 2020 puncak 0,05850, Taper Tantrum 2013) terjadi jauh lebih sering daripada kurva normal standar."),
        ("Ambang Batas Rezim Ekstrem (OOF):", "Pada 772 hari validasi OOF (2022–2024), persentil ke-95 target berada tepat pada ambang batas Y = 0,012650 (N=39 hari bursa krisis)."),
        ("Fenomena Volatility Clustering:", "Autokorelasi return absolut meluruh sangat lambat (long memory). Hari bursa berfluktuasi tinggi cenderung diikuti oleh hari bursa berfluktuasi tinggi lanjutan."),
        ("Implikasi Terhadap Pemodelan:", "Ekor tebal menuntut fungsi loss L1 (MAE) yang tahan outlier serta membenarkan prediktor persistensi (rv_past20) sebagai jangkar prediksi utama.")
    ]
    for ep_title, ep_desc in eda_points:
        p_t = tf_s4.add_paragraph()
        p_t.text = f"• {ep_title}"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_t.space_before = Pt(4)
        p_d = tf_s4.add_paragraph()
        p_d.text = ep_desc
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY

    add_framed_image(s4, 'outputs/eda/fig_08_volatility_clustering.png', Inches(5.8), Inches(2.85), Inches(6.733), Inches(3.95),
                     caption="Gambar 4.1: Autokorelasi (ACF) Return Absolut & Pembuktian Volatility Clustering IHSG")

    # =========================================================================
    # SLIDE 5: FEATURE ENGINEERING: X1, X2, X3 & FINANCIAL RATIONALE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s5, "04 / Task 1: Rekayasa Fitur Inovatif",
                         "Tiga Sinyal Finansial Orisinal: Formulasi & Rasionalitas Pasar",
                         "Menangkap transmisi sentimen global, disparitas suku bunga, dan guncangan riil sebelum merambat ke IHSG.")
    add_editorial_footer(s5, 5)

    s5_headers = ["SINYAL & NAMA FITUR", "FORMULASI MATEMATIS HARIAN (EOD t)", "TRANSMISI EKONOMI & RASIONALITAS FINANSIAL", "PERAN MODEL"]
    s5_rows = [
        [
            "X1: Fear-Liquidity Composite",
            "VIX_t × ((USDIDR_t - MA20_t) / MA20_t)",
            "Menangkap interaksi pelarian modal asing (capital outflow) saat kepanikan global (VIX) menekan kurs rupiah melampaui rata-rata 20 hari.",
            "Peringkat 4 MDI GBR (9,92%)\nKoefisien Linier Terbesar"
        ],
        [
            "X2: Rate Differential Pressure",
            "|BI_Rate_t - US_Rate_t| × |Ret5d(USDIDR)_t|",
            "Mengukur kerapuhan carry trade. Penyempitan spread bunga BI vs The Fed yang disertai fluktuasi kurs memicu tekanan likuidasi ekuitas.",
            "Sensor Siklus The Fed &\nStabilitas Moneter BI"
        ],
        [
            "X3: Commodity Macro Shock",
            "sqrt(Ret5(OIL)² + Ret5(GOLD)² + Ret5(SP500)²)",
            "Norma L2 multivariat bebas bias arah yang mengukur magnitudo guncangan simultan harga energi, aset safe haven, dan bursa Wall Street.",
            "Detektor Guncangan Riil\nStagflasi & Geopolitik"
        ]
    ]
    s5_widths = [Inches(2.5), Inches(3.0), Inches(4.3), Inches(1.933)]
    add_table_styled(s5, Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.2), s5_headers, s5_rows, s5_widths)

    s5_bot = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.65))
    set_flat_style(s5_bot, TEAL_TINT, border_color=TEAL_PRIMARY, border_width=1)

    tb_bot = s5.shapes.add_textbox(Inches(1.0), Inches(5.25), Inches(11.333), Inches(1.45))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "Rasionalitas Finansial & Kemandirian Sinyal terhadap Multikolinearitas"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    syn_bullets = [
        "Sifat Non-Redundan: Matriks korelasi membuktikan korelasi antar fitur baru berada pada rentang rendah hingga moderat (|r| < 0,35), memastikan penambahan fitur tidak memicu distorsi multikolinearitas parah.",
        "Mekanisme Early Warning: Volatilitas historis IHSG (rv_past5) bersifat reaktif karena baru melonjak setelah koreksi harga terjadi. Sebaliknya, kombinasi kurs dan sentimen eksternal (X1) bertindak sebagai sensor pendahulu.",
        "Kepatuhan Waktu: Seluruh data pendukung (kurs BI, VIX, komoditas) diekstraksi strictly pada penutupan hari t sebelum target hari t+1 terbentuk."
    ]
    for sb in syn_bullets:
        p = tf_b.add_paragraph()
        p.text = f"• {sb}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE_DARK
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 6: EMPIRICAL PROOF & NON-CAUSAL DISCIPLINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s6, "05 / Task 1: Bukti Empiris & Batasan",
                         "Validasi Empiris Fitur Baru & Batasan Disiplin Non-Kausal",
                         "Pembuktian peran fitur pada model linier dan non-linier serta penegasan batas etika statistik.")
    add_editorial_footer(s6, 6)

    s6_left = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(5.0))
    set_flat_style(s6_left, WHITE, BORDER_SUBTLE, 1)

    tb_s6 = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.6))
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True

    p = tf_s6.paragraphs[0]
    p.text = "1. Tiga Bukti Kuantitatif Peran Fitur Baru"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    proofs = [
        ("Dominasi Regresi Linier:", "Fitur X1 memegang koefisien positif terbesar pada model Ridge Tuned (alpha=1000), membuktikan peran utamanya dalam menangkap penularan kepanikan kurs secara linier."),
        ("Pohon Keputusan (MDI Importance):", "Pada model Gradient Boosting, X1 menduduki peringkat ke-4 fitur paling berpengaruh (9,92%), melampaui mayoritas prediktor makro individual."),
        ("Korelasi Dispersi Heteroskedastis:", "Lonjakan nilai X1 dan X3 berkoinsidensi erat dengan lonjakan varians residual pada model naif, mengonfirmasi sinyal efektif menangkap rezim turbulensi tinggi.")
    ]
    for pr_t, pr_d in proofs:
        p_t = tf_s6.add_paragraph()
        p_t.text = f"• {pr_t}"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_t.space_before = Pt(4)
        p_d = tf_s6.add_paragraph()
        p_d.text = pr_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY

    p_eth = tf_s6.add_paragraph()
    p_eth.text = "2. Penegasan Batas Disiplin Non-Kausal"
    p_eth.font.size = Pt(12)
    p_eth.font.bold = True
    p_eth.font.color.rgb = AMBER_ACCENT
    p_eth.space_before = Pt(10)

    ethics = [
        "Atribusi Prediktif vs Kausalitas:",
        "Penting ditekankan bahwa koefisien regresi, nilai MDI, dan SHAP mengukur kontribusi prediktif bersyarat (predictive association), BUKAN bukti kausalitas hukum alam atau hubungan sebab-akibat langsung.",
        "Implikasi Etika Portofolio:",
        "Penurunan matematis nilai X1 tidak serta-merta meredakan volatilitas jika faktor struktural lain tidak berubah. Model bertindak sebagai instrumen peringatan dini (early warning), bukan alat intervensi pasar."
    ]
    for idx, e in enumerate(ethics):
        p = tf_s6.add_paragraph()
        p.text = e
        p.font.size = Pt(9.0 if idx % 2 == 0 else 8.5)
        p.font.bold = True if idx % 2 == 0 else False
        p.font.color.rgb = SLATE_DARK if idx % 2 == 0 else SLATE_BODY
        p.space_after = Pt(2)

    add_framed_image(s6, 'outputs/models/fig_mod_03_feature_importance.png', Inches(6.0), Inches(1.7), Inches(6.533), Inches(5.0),
                     caption="Gambar 6.1: Mean Decrease in Impurity (MDI) Feature Importance Model Tree Baseline")

    # =========================================================================
    # SLIDE 7: TIME-SERIES VALIDATION & ANTI-LEAKAGE PROTOCOL
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s7, "06 / Task 2: Protokol Anti-Leakage",
                         "Arsitektur Validasi Temporal Bebas Bocor & Uji Invariansi",
                         "Menjamin integritas pengujian tanpa ada rembesan informasi masa depan ke masa lalu.")
    add_editorial_footer(s7, 7)

    steps = [
        ("TAHAP 01", "Expanding Walk-Forward", "3 Fold kronologis realistis: Fold 1 (2022, N=260/247), Fold 2 (2023, N=260/246), Fold 3 (2024 Pseudo-Holdout, N=252/279). Total 772 hari OOF."),
        ("TAHAP 02", "Purging Horizon H=5", "Mengeliminasi 5 hari perdagangan terakhir pada data latih tiap fold untuk memutus tumpang tindih horizon target [t+1, t+5]."),
        ("TAHAP 03", "Isolasi StandardScaler", "Parameter skala (mean dan varians) dihitung murni pada partisi latih, lalu diterapkan ke data validasi dan data uji kompetisi."),
        ("TAHAP 04", "Uji Invariansi Nol", "Menginjeksikan noise acak pada data masa depan menghasilkan deviasi prediksi hari t sebesar 0,000000000000 (Terbukti Bebas Bocor).")
    ]
    step_w = Inches(2.78)
    for idx, (s_num, s_title, s_desc) in enumerate(steps):
        s_left = Inches(0.8) + (idx * Inches(2.98))
        s_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_left, Inches(1.65), step_w, Inches(1.75))
        set_flat_style(s_box, WHITE, BORDER_SUBTLE, 1)

        tag_b = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, s_left, Inches(1.65), step_w, Inches(0.35))
        set_flat_style(tag_b, TEAL_DARK if idx == 3 else NAVY_PRIMARY, border_color=None)
        tb_tag = s7.shapes.add_textbox(s_left + Inches(0.1), Inches(1.7), step_w - Inches(0.2), Inches(0.25))
        p = tb_tag.text_frame.paragraphs[0]
        p.text = s_num
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

        tb = s7.shapes.add_textbox(s_left + Inches(0.12), Inches(2.05), step_w - Inches(0.24), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = s_title
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        
        p_d = tf.add_paragraph()
        p_d.text = s_desc
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = SLATE_BODY
        p_d.space_before = Pt(3)

    add_framed_image(s7, 'outputs/validation/fig_val_01_timeline_split.png', Inches(0.8), Inches(3.55), Inches(11.733), Inches(3.25),
                     caption="Gambar 7.1: Partisi Temporal Expanding Walk-Forward Cross-Validation & Purging Gap H=5")

    # =========================================================================
    # SLIDE 8: BASELINES & MODEL CANDIDATES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s8, "07 / Task 3: Arsitektur Pemodelan",
                         "Hierarki Pemodelan: Tolok Ukur Historis vs Kandidat Machine Learning",
                         "Membandingkan estimator varians statis/lagging dengan algoritma prediktif ter-regularisasi.")
    add_editorial_footer(s8, 8)

    p_base = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0))
    set_flat_style(p_base, WHITE, BORDER_SUBTLE, 1)

    tag_base = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(0.45))
    set_flat_style(tag_base, SLATE_DARK, border_color=None)
    tb_b = s8.shapes.add_textbox(Inches(0.95), Inches(1.78), Inches(5.4), Inches(0.3))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "KELOMPOK A — TOLOK UKUR HISTORIS (BASELINES)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_b_txt = s8.shapes.add_textbox(Inches(1.0), Inches(2.25), Inches(5.3), Inches(4.3))
    tf_b = tb_b_txt.text_frame
    tf_b.word_wrap = True

    base_items = [
        ("Constant Median (MAE 0,003299, RMSE 0,004454):", "Mengasumsikan volatilitas selalu berada pada nilai median historis. Berfungsi sebagai batas bawah efisiensi pemodelan tanpa memori waktu."),
        ("Baseline Naif Resmi rv_past5 (MAE 0,002981, RMSE 0,004088):", "Mengasumsikan volatilitas 5 hari ke depan sama persis dengan 5 hari terakhir. Merupakan acuan tolok ukur resmi kompetisi INCEPTION 2026."),
        ("Baseline Persistensi rv_past20 (MAE 0,002675, RMSE 0,003540):", "Menggunakan realized volatility 20 hari perdagangan (bulanan). Bertindak sebagai jangkar memori volatilitas jangka menengah."),
        ("Kelemahan Struktural Model Historis:", "Bersifat reaktif murni; baru melonjak setelah koreksi pasar terjadi dan lambat pulih saat kepanikan mereda, mengakibatkan over-ekstrapolasi tajam.")
    ]
    for b_t, b_d in base_items:
        p_t = tf_b.add_paragraph() if tf_b.paragraphs[0].text else tf_b.paragraphs[0]
        p_t.text = f"• {b_t}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_d = tf_b.add_paragraph()
        p_d.text = b_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY
        p_d.space_after = Pt(8)

    p_ml = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.7), Inches(5.7), Inches(5.0))
    set_flat_style(p_ml, WHITE, BORDER_SUBTLE, 1)

    tag_ml = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.7), Inches(5.7), Inches(0.45))
    set_flat_style(tag_ml, TEAL_DARK, border_color=None)
    tb_m = s8.shapes.add_textbox(Inches(7.0), Inches(1.78), Inches(5.4), Inches(0.3))
    p = tb_m.text_frame.paragraphs[0]
    p.text = "KELOMPOK B — ARSITEKTUR MACHINE LEARNING PREDIKTIF"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_m_txt = s8.shapes.add_textbox(Inches(7.0), Inches(2.25), Inches(5.3), Inches(4.3))
    tf_m = tb_m_txt.text_frame
    tf_m.word_wrap = True

    ml_items = [
        ("Ridge Tuned (Alpha 1000, MAE 0,002471, RMSE 0,003287):", "Regresi linier ter-regularisasi L2 kuat yang menekan varians koefisien makro berkorelasi, stabil mengestimasi tren umum pasar."),
        ("GBR Tuned (Champion Tunggal, MAE 0,002462, RMSE 0,003178):", "Gradient Boosting dengan fungsi loss L1 dan pohon dangkal (depth 2), unggul menangkap interaksi non-linier antar sinyal."),
        ("Blend 60:40 (Ensemble Champion, MAE 0,002401, RMSE 0,003152):", "Kombinasi terbobot GBR (60%) dan Ridge (40%). Sinergi optimal yang memadukan fleksibilitas non-linier dan stabilitas linier."),
        ("Blend 50:30:20 (Heuristik, MAE 0,002377, RMSE 0,003144):", "Memadukan GBR, Ridge, dan rv_past20. Meskipun MAE pooled sedikit lebih rendah, model ini terbukti kurang stabil pada evaluasi Fold 2024.")
    ]
    for m_t, m_d in ml_items:
        p_t = tf_m.add_paragraph() if tf_m.paragraphs[0].text else tf_m.paragraphs[0]
        p_t.text = f"• {m_t}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_d = tf_m.add_paragraph()
        p_d.text = m_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY
        p_d.space_after = Pt(8)

    # =========================================================================
    # SLIDE 9: HYPERPARAMETER TUNING & ARCHITECTURE SELECTION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s9, "08 / Task 3: Seleksi Arsitektur",
                         "Optimasi Hiperparameter: Fungsi Loss L1 & Kontrol Overfitting",
                         "Pemilihan parameter didasarkan pada karakteristik leptokurtik data finansial dan regularisasi ketat.")
    add_editorial_footer(s9, 9)

    s9_left = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(5.0))
    set_flat_style(s9_left, WHITE, BORDER_SUBTLE, 1)

    tb_s9 = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.6))
    tf_s9 = tb_s9.text_frame
    tf_s9.word_wrap = True

    p = tf_s9.paragraphs[0]
    p.text = "Rasionalitas Penyetelan Hiperparameter"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    tune_reasons = [
        ("Loss L1 (Mean Absolute Error):", "Mengestimasi conditional median yang kebal terhadap lonjakan ekstrem. Fungsi loss L2 (MSE) terbukti rapuh karena mengkuadratkan galat krisis sehingga model over-fitting pada noise."),
        ("Pohon Dangkal (Max Depth = 2):", "Pohon sengaja dibatasi hanya 2 split (maksimal 4 daun). Membatasi model agar hanya menangkap interaksi makro orde kedua dan mencegah penghafalan derau acak."),
        ("Shrinkage Rate Konservatif (0,03):", "Learning rate rendah menjamin pembaruan bobot secara bertahap melintasi 100 estimator, menghasilkan konvergensi kurva validasi yang stabil."),
        ("Penalti Kuat Ridge (Alpha = 1000):", "Penyusutan koefisien L2 yang agresif efektif menekan varians antar prediktor makro yang saling berkorelasi tinggi (USD/IDR, suku bunga, VIX).")
    ]
    for tr_t, tr_d in tune_reasons:
        p_t = tf_s9.add_paragraph()
        p_t.text = f"• {tr_t}"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_t.space_before = Pt(4)
        p_d = tf_s9.add_paragraph()
        p_d.text = tr_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY

    add_framed_image(s9, 'outputs/tuning/fig_tune_01_grid_search_curves.png', Inches(6.0), Inches(1.7), Inches(6.533), Inches(5.0),
                     caption="Gambar 9.1: Kurva Validasi Grid Search Hiperparameter GBR & Ridge Regression")

    # =========================================================================
    # SLIDE 10: MODEL EVALUATION & RECONCILED BENCHMARK
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s10, "09 / Task 3: Evaluasi Kuantitatif",
                         "Rekonsiliasi Evaluasi OOF 772 Hari: Keunggulan +19,5% vs Naif",
                         "Penyelarasan dokumentasi Checkpoint 6.3 pada ruang sampel validasi 2022–2024 yang identik.")
    add_editorial_footer(s10, 10)

    top_box = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.25))
    set_flat_style(top_box, TEAL_TINT, border_color=TEAL_PRIMARY, border_width=1)

    tb_t = s10.shapes.add_textbox(Inches(1.0), Inches(1.72), Inches(11.333), Inches(1.1))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "KEUNGGULAN +19,5% DI ATAS BASELINE NAIF RESMI (rv_past5)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Berdasarkan audit Checkpoint 6.3 pada 772 hari validasi OOF, Blend 60:40 mencatatkan MAE 0,002401 vs 0,002981 pada baseline naif resmi (unggul +19,5%) serta unggul +10,2% vs persistensi kuat (rv_past20 MAE 0,002675). Model juga tangguh meredam galat pada 39 hari rezim krisis ekstrem (MAE 0,007778)."
    p_sub.font.size = Pt(9.0)
    p_sub.font.color.rgb = SLATE_DARK
    p_sub.space_before = Pt(3)

    # Reconciled Table matching notebook/06_Reconciliation_Audit.ipynb Cell 8 & notebook/02 Cell 10
    s10_headers = ["ARSITEKTUR MODEL / KONFIGURASI", "POOLED MAE", "POOLED RMSE", "FOLD 2024 MAE", "MAE EKSTREM (Y>0,01265)", "STATUS / EVALUASI"]
    s10_rows = [
        ["Constant Median (Tanpa Dinamika Waktu)", "0,003299", "0,004454", "0,002640", "0,009618", "-10,7% (Batas Bawah)"],
        ["Baseline Naif Resmi (rv_past5)", "0,002981", "0,004088", "0,003348", "0,008914", "Acuan Dasar (0,0%)"],
        ["Baseline Persistensi Kuat (rv_past20)", "0,002675", "0,003540", "0,003232", "0,008310", "+10,2% vs Naif"],
        ["Ridge Tuned (Alpha 1000)", "0,002471", "0,003287", "0,002824", "0,007683", "+17,1% vs Naif"],
        ["GBR Tuned (Champion Tunggal)", "0,002462", "0,003178", "0,002646", "0,007882", "+17,4% vs Naif"],
        ["Blend 60:40 (Ensemble Champion)", "0,002401", "0,003152", "0,002654", "0,007778", "+19,5% (Pilihan Final)"]
    ]
    s10_widths = [Inches(3.733), Inches(1.5), Inches(1.5), Inches(1.6), Inches(1.9), Inches(1.5)]
    add_table_styled(s10, Inches(0.8), Inches(3.05), Inches(11.733), Inches(2.7), s10_headers, s10_rows, s10_widths, align_right_cols=[1, 2, 3, 4])

    tb_note = s10.shapes.add_textbox(Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.95))
    tf_n = tb_note.text_frame
    tf_n.word_wrap = True
    p = tf_n.paragraphs[0]
    p.text = "Catatan Kejujuran Metodologi (Methodological Honesty):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = SLATE_DARK
    notes = [
        "1. Periode 2022–2024 adalah evaluasi out-of-fold (OOF), namun Fold 2024 diakui sebagai pseudo-holdout karena sempat memengaruhi proses tuning hyperparameter.",
        "2. Seluruh metrik dihitung pada baris dan tanggal yang sama persis (772 hari bursa aktif) tanpa manipulasi data.",
        "3. Data kompetisi 2025–2026 adalah data inferensi tanpa label (Y=NaN), bukan data validasi berlabel yang telah terverifikasi akurasinya."
    ]
    for nt in notes:
        p = tf_n.add_paragraph()
        p.text = nt
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 11: GLOBAL XAI WITH SHAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s11, "10 / Task 3: Explainable AI Global",
                         "Dekomposisi SHAP Global: Hierarki Pengaruh & Transmisi Risiko",
                         "Transparansi faktor prediktif memenuhi regulasi anti-black box komite risiko institusional.")
    add_editorial_footer(s11, 11)

    s11_left = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(5.0))
    set_flat_style(s11_left, WHITE, BORDER_SUBTLE, 1)

    tb_s11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.6))
    tf_s11 = tb_s11.text_frame
    tf_s11.word_wrap = True

    p = tf_s11.paragraphs[0]
    p.text = "Peringkat Atribusi Fitur (Mean |SHAP|)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    shap_items = [
        ("1. rv_past20 (Mean |SHAP| 0,000466):", "Jangkar dasar volatilitas bulanan. Nilai masa lalu yang tinggi secara konsisten menggeser prediksi model ke rezim volatilitas tinggi."),
        ("2. mom_ihsg_10 (Mean |SHAP| 0,000294):", "Mencerminkan leverage effect asimetris: koreksi tajam indeks 10 hari memicu lonjakan volatilitas jauh lebih kuat dibandingkan apresiasi indeks."),
        ("3. US_rate (Mean |SHAP| 0,000231):", "Kenaikan suku bunga The Fed memperketat likuiditas global dan memicu aksi jual asing (outflow) di pasar modal Indonesia."),
        ("4. VIX (Mean |SHAP| 0,000188):", "Kepanikan global di Wall Street menular langsung ke bursa domestik, bertindak sebagai pemicu lonjakan volatilitas cepat."),
        ("5. X1_Fear_Liquidity (Mean |SHAP| 0,000142):", "Penguat sinyal bahaya saat depresiasi nilai tukar rupiah terjadi bersamaan dengan kepanikan bursa global.")
    ]
    for st, sd in shap_items:
        p_t = tf_s11.add_paragraph()
        p_t.text = st
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK
        p_t.space_before = Pt(3)
        p_d = tf_s11.add_paragraph()
        p_d.text = sd
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY

    p_w = tf_s11.add_paragraph()
    p_w.text = "Catatan Tata Kelola: SHAP mengukur kontribusi marjinal prediktif, BUKAN bukti hubungan kausalitas mekanistik."
    p_w.font.size = Pt(8.5)
    p_w.font.italic = True
    p_w.font.color.rgb = SLATE_MUTED
    p_w.space_before = Pt(8)

    add_framed_image(s11, 'outputs/xai/fig_xai_02_shap_summary_beeswarm.png', Inches(6.0), Inches(1.7), Inches(6.533), Inches(5.0),
                     caption="Gambar 11.1: SHAP Summary Beeswarm Plot Model GBR Tuned (Evaluasi OOF 772 Hari)")

    # =========================================================================
    # SLIDE 12: LOCAL XAI: CASE STUDY 11 MAY 2022 (VERIFIED FROM NB 07 CELL 6)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s12, "11 / Task 3: Explainable AI Lokal",
                         "Audit Forensik Krisis 11 Mei 2022: Deteksi Dini Puncak Volatilitas",
                         "Waterfall plot membongkar alasan sistem mengaktifkan Red Alert sebelum koreksi modal terjadi.")
    add_editorial_footer(s12, 12)

    s12_left = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(5.0))
    set_flat_style(s12_left, WHITE, BORDER_SUBTLE, 1)

    tb_s12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.6))
    tf_s12 = tb_s12.text_frame
    tf_s12.word_wrap = True

    p = tf_s12.paragraphs[0]
    p.text = "Kronologi Deteksi Krisis Pasca-Lebaran 2022"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    # Exact numbers from notebook/07_Model_Interpretation_XAI.ipynb Cell 6
    case_points = [
        ("Konteks Turbulensi Pasar:", "Tanggal 11 Mei 2022 merupakan pembukaan bursa pasca libur panjang Idul Fitri yang bertepatan dengan kenaikan Fed Rate 50 bps. IHSG terkoreksi tajam."),
        ("Peringatan Dini Sistem (Red Alert):", "Target aktual volatilitas melonjak ke Y = 0,019739. Model Blend 60:40 memproyeksikan lonjakan ke 0,012739 (GBR 0,012095, Ridge 0,013705). Red Alert aktif!"),
        ("Dekomposisi Faktor Pendorong SHAP:", ""),
        ("  • VIX Global 32,56 (+0,00160):", "Kepanikan Wall Street menembus batas krisis."),
        ("  • Koreksi IHSG 5-Hari -8,72% (+0,00123):", "Aksi jual asing agresif mengonfirmasi tekanan pasar."),
        ("  • Tren Momentum 10-Hari -6,85% (+0,00107):", "Ketiadaan likuiditas beli memperpanjang kepanikan."),
        ("  • Level IHSG 6.816 (-0,00028):", "Valuasi absolut meredam over-ekstrapolasi liar.")
    ]
    for cp_t, cp_d in case_points:
        p = tf_s12.add_paragraph()
        p.text = f"{cp_t} {cp_d}"
        p.font.size = Pt(8.5)
        p.font.bold = True if ("•" not in cp_t and "Kronologi" not in cp_t) else False
        p.font.color.rgb = SLATE_DARK
        p.space_after = Pt(2)

    p_imp = tf_s12.add_paragraph()
    p_imp.text = "Manfaat Manajerial: Manajer investasi memperoleh waktu 24–48 jam untuk melakukan de-risking portofolio sebelum penurunan NAB berlanjut."
    p_imp.font.size = Pt(8.5)
    p_imp.font.bold = True
    p_imp.font.color.rgb = TEAL_DARK
    p_imp.space_before = Pt(6)

    add_framed_image(s12, 'outputs/xai/fig_xai_03_local_explanations.png', Inches(6.0), Inches(1.7), Inches(6.533), Inches(5.0),
                     caption="Gambar 12.1: SHAP Waterfall Plot untuk Kasus Krisis Pasar 11 Mei 2022")

    # =========================================================================
    # SLIDE 13: ERROR ANALYSIS: BLACK MONDAY 2024 (VERIFIED CHECKPOINT 6.1)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s13, "12 / Task 3: Audit Kesalahan Prediksi",
                         "Analisis Galat Ekstrem: Forensik Black Monday Agustus 2024",
                         "Menguji batas kapabilitas model saat menghadapi kejutan eksogen likuidasi Yen Carry Trade.")
    add_editorial_footer(s13, 13)

    # Panel A: Underprediction 31 Juli 2024 (Verified Checkpoint 6.1)
    p_err1 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.7), Inches(2.65))
    set_flat_style(p_err1, WHITE, BORDER_SUBTLE, 1)

    tag_e1 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.7), Inches(0.35))
    set_flat_style(tag_e1, CRIMSON_ACCENT, border_color=None)
    tb_e1 = s13.shapes.add_textbox(Inches(0.95), Inches(1.7), Inches(5.4), Inches(0.25))
    p = tb_e1.text_frame.paragraphs[0]
    p.text = "KASUS 1: UNDERPREDICTION — 31 JULI 2024"
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_e1_txt = s13.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(5.4), Inches(2.2))
    tf_e1 = tb_e1_txt.text_frame
    tf_e1.word_wrap = True
    bullets_e1 = [
        ("Aktual Y = 0,019251 | Prediksi = 0,005825 | Residual = +0,013426:", "Model memproyeksikan volatilitas rendah karena seluruh prediktor harian EOD hari t (VIX 16,36, IHSG +0,19%) masih berada dalam kondisi tenang."),
        ("Akar Masalah (Kejutan Eksogen):", "Bank of Japan (BoJ) menaikkan suku bunga acuan pada 31 Juli siang. Efek likuidasi massal Yen Carry Trade global baru meledak di pasar pada t+3 (5 Agustus)."),
        ("Limitasi Inheren (No Prescience):", "Model bebas kebocoran tidak memiliki bola kristal untuk meramalkan guncangan eksogen yang belum tercermin pada data penutupan hari t.")
    ]
    for b_t, b_d in bullets_e1:
        p_t = tf_e1.add_paragraph() if tf_e1.paragraphs[0].text else tf_e1.paragraphs[0]
        p_t.text = f"• {b_t} {b_d}"
        p_t.font.size = Pt(8.5)
        p_t.font.color.rgb = SLATE_BODY
        p_t.space_after = Pt(2)

    # Panel B: Overprediction 5 Agustus 2024 (Verified Checkpoint 6.1)
    p_err2 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.65), Inches(5.7), Inches(2.65))
    set_flat_style(p_err2, WHITE, BORDER_SUBTLE, 1)

    tag_e2 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.65), Inches(5.7), Inches(0.35))
    set_flat_style(tag_e2, AMBER_ACCENT, border_color=None)
    tb_e2 = s13.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.4), Inches(0.25))
    p = tb_e2.text_frame.paragraphs[0]
    p.text = "KASUS 2: OVERPREDICTION — 5 AGUSTUS 2024"
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_e2_txt = s13.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.4), Inches(2.2))
    tf_e2 = tb_e2_txt.text_frame
    tf_e2.word_wrap = True
    bullets_e2 = [
        ("Aktual Y = 0,005503 | Prediksi = 0,012314 | Residual = -0,006811:", "Model memproyeksikan volatilitas tinggi lanjutan akibat lonjakan kepanikan ekstrem VIX ke level 38,57 pada Black Monday."),
        ("Akar Masalah (Reversi Cepat Kebijakan):", "Deputi Gubernur BoJ Uchida segera mengumumkan moratorium kenaikan suku bunga lanjutan dalam 48 jam, memicu pemulihan tajam pasar modal dunia."),
        ("Daya Tahan Model vs Baseline Naif:", "Galat absolut Blend 60:40 (0,006811) masih 38,7% lebih rendah dibandingkan baseline naif (0,011118, prediksi 0,016621) yang mengalami ekstrapolasi liar.")
    ]
    for b_t, b_d in bullets_e2:
        p_t = tf_e2.add_paragraph() if tf_e2.paragraphs[0].text else tf_e2.paragraphs[0]
        p_t.text = f"• {b_t} {b_d}"
        p_t.font.size = Pt(8.5)
        p_t.font.color.rgb = SLATE_BODY
        p_t.space_after = Pt(2)

    add_framed_image(s13, 'outputs/xai/error_analysis/fig_err_01_timeline_context.png', Inches(0.8), Inches(4.42), Inches(11.733), Inches(2.5),
                     caption="Gambar 13.1: Garis Waktu Krisis Black Monday 2024 — Pergerakan Aktual vs Proyeksi Model")

    # =========================================================================
    # SLIDE 14: PORTFOLIO IMPLICATIONS & RISK GOVERNANCE (POLICY PROPOSALS)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s14, "13 / Usulan Kebijakan Komite Risiko (Policy Proposals)",
                         "Tata Kelola Risiko Portofolio: Kerangka Kebijakan Dinamis Tiga Rezim",
                         "Usulan kebijakan alokasi aset dinamis berdasarkan sinyal model kuantitatif (bukan temuan empiris yang telah di-backtest).")
    add_editorial_footer(s14, 14)

    # Three Regime Allocation Cards explicitly labeled as Policy Proposals
    regimes = [
        ("USULAN REZIM TENANG", "Y < 0,0060", "Status Sinyal: HIJAU (Normal Operations)",
         "Usulan Ekuitas: 90% – 95%", "Instrumen Kas / SBN: 5% – 10%",
         "Kebijakan: Eksekusi strategi pertumbuhan penuh; pemantauan EOD standar; tidak diperlukan lindung nilai tambahan.",
         TEAL_DARK, TEAL_TINT),
        ("USULAN REZIM WASPADA", "0,0060 ≤ Y ≤ 0,0120", "Status Sinyal: KUNING (Hedging Alert)",
         "Usulan Ekuitas: 75% – 80%", "Instrumen Kas / SBN: 20% – 25%",
         "Kebijakan: Realokasi defensif ke saham ber-beta rendah; pembelian opsi put protektif pada sektor finansial.",
         AMBER_ACCENT, AMBER_TINT),
        ("USULAN REZIM KRISIS EKSTREM", "Y > 0,0120", "Status Sinyal: MERAH (Capital Preservation)",
         "Usulan Ekuitas: 50% – 60%", "Instrumen Kas / SBN: 40% – 50%",
         "Kebijakan: De-risking agresif; lindung nilai penuh portofolio; aktivasi pelaporan darurat ke Komite Investasi.",
         CRIMSON_ACCENT, CRIMSON_TINT)
    ]
    r_w = Inches(3.7)
    for idx, (r_title, r_thresh, r_status, r_eq, r_cash, r_pol, col_acc, col_tint) in enumerate(regimes):
        r_left = Inches(0.8) + (idx * Inches(4.0))
        r_box = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, r_left, Inches(1.7), r_w, Inches(2.95))
        set_flat_style(r_box, WHITE, BORDER_SUBTLE, 1)

        tag = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, r_left, Inches(1.7), r_w, Inches(0.42))
        set_flat_style(tag, col_acc, border_color=None)
        tb_t = s14.shapes.add_textbox(r_left + Inches(0.12), Inches(1.75), r_w - Inches(0.24), Inches(0.3))
        p = tb_t.text_frame.paragraphs[0]
        p.text = r_title
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

        tb_c = s14.shapes.add_textbox(r_left + Inches(0.15), Inches(2.2), r_w - Inches(0.3), Inches(2.4))
        tf = tb_c.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = r_thresh
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = r_status
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = col_acc
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = f"• {r_eq}"
        p3.font.size = Pt(8.5)
        p3.font.bold = True
        p3.font.color.rgb = SLATE_DARK

        p4 = tf.add_paragraph()
        p4.text = f"• {r_cash}"
        p4.font.size = Pt(8.5)
        p4.font.bold = True
        p4.font.color.rgb = SLATE_DARK

        p5 = tf.add_paragraph()
        p5.text = f"• {r_pol}"
        p5.font.size = Pt(8.0)
        p5.font.color.rgb = SLATE_BODY
        p5.space_before = Pt(4)

    bot_box = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.733), Inches(2.0))
    set_flat_style(bot_box, WHITE, BORDER_SUBTLE, 1)

    tb_bot = s14.shapes.add_textbox(Inches(1.0), Inches(4.9), Inches(11.333), Inches(1.8))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "Tiga Mandat Tata Kelola Risiko & Batasan Operasional Model"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    gov_mandates = [
        ("Sistem Peringatan Dua Kecepatan:", "Mengintegrasikan sinyal harian EOD dengan pemutus sirkuit intraday (circuit breaker). Jika VIX global melonjak > 30 secara intraday, komite risiko otomatis bersiap tanpa menunggu EOD."),
        ("Transparansi Komite & Faktur SHAP:", "Setiap aktivasi Sinyal Merah wajib disertai dokumen faktur SHAP yang membongkar faktor penyebab guncangan (misal: tekanan kurs vs suku bunga) guna menjamin akuntabilitas fidusia."),
        ("Batas Operasional & Integritas:", "Komite mengakui keterbatasan pseudo-holdout 2024 serta menegaskan bahwa 359 hari data 2025–2026 adalah inferensi murni tanpa label, sehingga memerlukan audit drift berkala.")
    ]
    for gm_t, gm_d in gov_mandates:
        p = tf_b.add_paragraph()
        p.text = f"• {gm_t} {gm_d}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE_BODY
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 15: CONCLUSION, TRACEABILITY, & SUBMISSION READINESS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_editorial_header(s15, "14 / Kesimpulan Eksekutif & Keterlacakan",
                         "Kesimpulan Akhir & Matriks Keterlacakan Komputasi Sumber",
                         "Sistem tervalidasi 100% patuh terhadap studi kasus dan siap mengawal portofolio PT Investion.")
    add_editorial_footer(s15, 15)

    s15_left = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(4.5), Inches(4.3))
    set_flat_style(s15_left, WHITE, BORDER_SUBTLE, 1)

    tb_s15l = s15.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(4.2), Inches(4.0))
    tf_s15l = tb_s15l.text_frame
    tf_s15l.word_wrap = True

    p = tf_s15l.paragraphs[0]
    p.text = "Tiga Pilar Kesiapan Sistem"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    pillars = [
        ("1. Keunggulan Prediktif Superior:", "Blend 60:40 membuktikan efisiensi MAE 0,002401 (+19,5% vs Naif resmi rv_past5) serta tangguh meredam galat di rezim krisis ekstrem."),
        ("2. Disiplin Metodologi Nir-Bocor:", "Protokol expanding walk-forward, purging gap H=5, dan isolasi StandardScaler terbukti menghasilkan deviasi nol mutlak (0,000000000000) pada uji invariansi masa depan."),
        ("3. Kepatuhan Tata Kelola & XAI:", "Setiap keputusan dapat dipertanggungjawabkan melalui SHAP Beeswarm dan Waterfall Plot, memenuhi mandat fidusia dan regulasi OJK.")
    ]
    for pil_t, pil_d in pillars:
        p_t = tf_s15l.add_paragraph()
        p_t.text = pil_t
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEAL_DARK
        p_t.space_before = Pt(4)
        p_d = tf_s15l.add_paragraph()
        p_d.text = pil_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = SLATE_BODY

    s15_headers = ["PARAMETER / METRIK KUNCI", "NILAI TERVERIFIKASI", "ARTEFAK SUMBER ASLI"]
    s15_rows = [
        ["Baseline Naif (rv_past5) vs Persistensi (rv_past20)", "MAE 0,002981 vs 0,002675", "02_Validation_Baseline.ipynb (Cell 10)"],
        ["Ensemble Champion Blend 60:40 (GBR + Ridge)", "MAE 0,002401 (+19,5% vs Naif)", "05_Robustness_Model_Selection.ipynb (Cell 6)"],
        ["Ambang Batas Rezim Ekstrem (Persentil Ke-95)", "Y_threshold = 0,012650 (N=39)", "06_Reconciliation_Audit.ipynb (Cell 8)"],
        ["Uji Invariansi Anti-Leakage Masa Depan", "Deviasi = 0,000000000000", "scripts/feature_engineering.py (Line 240–285)"],
        ["Berkas Prediksi Final Kompetisi 2025–2026", "Tepat 359 baris out-of-sample", "outputs/submission/submission_blend60_40.csv"]
    ]
    s15_widths = [Inches(3.3), Inches(1.9), Inches(1.833)]
    add_table_styled(s15, Inches(5.5), Inches(1.7), Inches(7.033), Inches(4.3), s15_headers, s15_rows, s15_widths)

    ready_bar = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.7))
    set_flat_style(ready_bar, NAVY_PRIMARY, border_color=None)
    
    tb_rb = s15.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.333), Inches(0.5))
    tf_rb = tb_rb.text_frame
    p_rb = tf_rb.paragraphs[0]
    p_rb.text = "STATUS SUBMISI: READY FOR SUBMISSION — 359 BARIS DATA UJI 2025–2026 TERPREDIKSI SECARA OUT-OF-SAMPLE MURNI"
    p_rb.font.size = Pt(10.5)
    p_rb.font.bold = True
    p_rb.font.color.rgb = TEAL_PRIMARY
    p_rb.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully built and saved to: {OUTPUT_PPTX}")
    print(f"File size: {os.path.getsize(OUTPUT_PPTX):,} bytes")
    print("=" * 70)

if __name__ == '__main__':
    build_audited_presentation()
