# -*- coding: utf-8 -*-
"""
INCEPTION 2026 - PRESENTATION SLIDE DECK BUILDER
Target Output: outputs/final/DSC_GajahHitam_PPT.pptx
Format: 16:9 Widescreen (13.333 x 7.5 inches)
Slide Count: Exactly 15 slides
Design Standard: Professional Investment Banking / Quantitative Risk Management Executive Deck
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = r'z:\Projects\Inception'
OUTPUT_PPTX = os.path.join(PROJECT_ROOT, 'outputs', 'final', 'DSC_GajahHitam_PPT.pptx')

# Professional Color Palette
NAVY_DARK    = RGBColor(15, 23, 42)      # #0F172A Title / Deep Background
SLATE_DARK   = RGBColor(30, 41, 59)      # #1E293B Card Header
BLUE_PRIMARY = RGBColor(37, 99, 235)     # #2563EB Primary Brand Accent
BLUE_DARK    = RGBColor(29, 78, 216)     # #1D4ED8 Deep Cobalt
BLUE_LIGHT   = RGBColor(239, 246, 255)   # #EFF6FF Tint Background
GREY_BG      = RGBColor(248, 250, 252)   # #F8FAFC Slide Canvas
WHITE        = RGBColor(255, 255, 255)   # #FFFFFF Card Surface
BORDER_LIGHT = RGBColor(226, 232, 240)   # #E2E8F0 Subtle Border
TEXT_MAIN    = RGBColor(15, 23, 42)      # #0F172A Primary Text
TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B Secondary Text
EMERALD      = RGBColor(5, 150, 105)     # #059669 Outperformance / Pass
CRIMSON      = RGBColor(220, 38, 38)     # #DC2626 Risk / Error / Loss
AMBER        = RGBColor(217, 119, 6)     # #D97706 Warning / Alert
GOLD         = RGBColor(245, 158, 11)     # #F59E0B Highlight

def set_shape_flat(shape, fill_color, border_color=None, border_width=1):
    """Set flat fill and optional clean border on a shape."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()

def add_header(slide, category_tag, slide_title, subtitle_takeaway):
    """Adds a standard high-impact corporate slide header."""
    # Category Tracker Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.25))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_tag.upper()
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = BLUE_PRIMARY

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.45))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = slide_title
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_DARK

    # Subtitle / Key Takeaway
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.733), Inches(0.3))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_takeaway
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

def add_footer(slide, current_slide, total_slides=15):
    """Adds consistent corporate slide footer."""
    # Footer Left
    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.25))
    tf_l = foot_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "INCEPTION 2026 Data Science Competition | Tim GajahHitam — PT Investion Quantitative Risk Division"
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = TEXT_MUTED

    # Footer Right (Page Number)
    foot_right = slide.shapes.add_textbox(Inches(10.0), Inches(7.05), Inches(2.533), Inches(0.25))
    tf_r = foot_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} dari {total_slides}"
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = NAVY_DARK

def add_card(slide, left, top, width, height, fill_color=WHITE, border_color=BORDER_LIGHT, border_width=1):
    """Creates a card container shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    set_shape_flat(shape, fill_color, border_color, border_width)
    return shape

def add_image_framed(slide, img_path, left, top, width, height, caption=None):
    """Adds an image safely with optional frame and caption."""
    abs_path = os.path.abspath(img_path)
    if os.path.exists(abs_path):
        # Background card frame
        card = add_card(slide, left, top, width, height, fill_color=WHITE, border_color=BORDER_LIGHT)
        # Inner image placement with margin
        margin = Inches(0.08)
        img_left = left + margin
        img_top = top + margin
        img_w = width - (margin * 2)
        img_h = height - (margin * 2) - (Inches(0.25) if caption else 0)
        slide.shapes.add_picture(abs_path, img_left, img_top, img_w, img_h)
        
        if caption:
            cap_box = slide.shapes.add_textbox(left, top + height - Inches(0.28), width, Inches(0.25))
            tf = cap_box.text_frame
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = caption
            p.font.size = Pt(8.5)
            p.font.color.rgb = TEXT_MUTED
            p.font.italic = True
    else:
        # Fallback card if image missing
        card = add_card(slide, left, top, width, height, fill_color=RGBColor(254, 242, 242), border_color=CRIMSON)
        tb = slide.shapes.add_textbox(left, top, width, height)
        p = tb.text_frame.paragraphs[0]
        p.text = f"[Grafik tidak ditemukan: {os.path.basename(img_path)}]"
        p.font.size = Pt(10)
        p.font.color.rgb = CRIMSON

def build_presentation():
    print("Initializing Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER & IDENTITAS KOMPETISI
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = add_card(s1, Inches(0), Inches(0), Inches(13.333), Inches(7.5), fill_color=NAVY_DARK, border_color=None)
    
    # Accent top border
    accent_bar = add_card(s1, Inches(0), Inches(0), Inches(13.333), Inches(0.12), fill_color=BLUE_PRIMARY, border_color=None)

    # Competition Tag Badge
    badge_shape = add_card(s1, Inches(1.0), Inches(1.2), Inches(5.2), Inches(0.4), fill_color=BLUE_DARK, border_color=None)
    tb_b = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(5.2), Inches(0.4))
    p_b = tb_b.text_frame.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "INCEPTION 2026 DATA SCIENCE COMPETITION"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = WHITE

    # Main Title
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.333), Inches(1.6))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "SISTEM PERINGATAN DINI REALIZED VOLATILITY IHSG"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Predictive Machine Learning & Explainable AI (XAI) Mengawal Portofolio Dana Kelolaan Triliunan Rupiah PT Investion di Tengah Turbulensi Pasar Finansial Global"
    p_t2.font.size = Pt(14)
    p_t2.font.color.rgb = RGBColor(148, 163, 184)
    p_t2.space_before = Pt(12)

    # 4 Meta Cards
    meta_info = [
        ("NAMA TIM", "GajahHitam", "Peserta Resmi Kompetisi"),
        ("PERAN ANALIS", "Sr. Quantitative Risk Analyst", "Divisi Manajemen Risiko PT Investion"),
        ("TARGET PREDIKSI", "Target_Volatilitas_Y", "Realized Volatility 5-Hari Forward"),
        ("STATUS AUDIT", "100% Complete & Reconciled", "Terverifikasi Bebas Leakage")
    ]
    card_w = Inches(2.65)
    for i, (m_label, m_val, m_sub) in enumerate(meta_info):
        c_left = Inches(1.0) + (i * Inches(2.9))
        c_shape = add_card(s1, c_left, Inches(4.6), card_w, Inches(1.8), fill_color=SLATE_DARK, border_color=RGBColor(51, 65, 85))
        
        tb_m = s1.shapes.add_textbox(c_left + Inches(0.15), Inches(4.75), card_w - Inches(0.3), Inches(1.5))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p1 = tf_m.paragraphs[0]
        p1.text = m_label
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_PRIMARY
        
        p2 = tf_m.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(4)
        
        p3 = tf_m.add_paragraph()
        p3.text = m_sub
        p3.font.size = Pt(9)
        p3.font.color.rgb = RGBColor(148, 163, 184)
        p3.space_before = Pt(4)

    # Bottom Date
    tb_date = s1.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.4))
    p_d = tb_date.text_frame.paragraphs[0]
    p_d.text = "Financial Time Series Track | Babak Penyisihan INCEPTION 2026 | Jakarta, Oktober 2026"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # SLIDE 2: LATAR BELAKANG & TUJUAN EARLY WARNING SYSTEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Konteks Bisnis & Manajemen Risiko Portofolio",
               "Mengawal Dana Triliunan PT Investion di Tengah Turbulensi Pasar",
               "Kelemahan pendekatan naif menuntut dibangunnya Sistem Peringatan Dini yang prediktif dan anti-black box.")
    add_footer(s2, 2)

    cards_s2 = [
        ("1. Profil Risiko Portofolio PT Investion", [
            "PT Investion mengelola portofolio ekuitas dan campuran bernilai triliunan rupiah dengan eksposur tinggi pada IHSG.",
            "Karakteristik pasar berkembang (emerging market) sangat rentan terhadap penularan risiko (contagion effect) eksternal.",
            "Guncangan makro global dapat memicu aksi jual asing (foreign outflow) masif dan menggerus NAB portofolio dalam hitungan hari."
        ], BLUE_PRIMARY),
        ("2. Kegagalan Pendekatan Naif Tradisional", [
            "Estimasi varians historis masa lalu bersifat lagging: baru melonjak setelah koreksi harga terjadi (drawdown modal).",
            "Gagal mengantisipasi fenomena volatility clustering di mana kepanikan kurs valas dan Wall Street mendahului volatilitas ekuitas.",
            "Manajer investasi tidak memiliki buffer waktu untuk melakukan rebalancing atau lindung nilai (hedging) defensif."
        ], CRIMSON),
        ("3. Mandat Fidusia & Regulasi Anti-Black Box", [
            "Dewan Direksi dan Komite Risiko melarang penggunaan model black-box untuk keputusan alokasi modal bernilai triliunan rupiah.",
            "Regulasi OJK & fidusia nasabah institusi menuntut transparansi faktor: mengapa sistem mendeteksi sinyal bahaya (Red Alert)?",
            "Solusi Kuantitatif: Model regresi prediktif 5-hari forward yang dipadukan dengan Explainable AI (SHAP) untuk akuntabilitas penuh."
        ], EMERALD)
    ]
    col_w = Inches(3.75)
    for i, (c_title, points, c_accent) in enumerate(cards_s2):
        c_left = Inches(0.8) + (i * Inches(4.0))
        card = add_card(s2, c_left, Inches(1.65), col_w, Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
        
        # Header banner inside card
        banner = add_card(s2, c_left, Inches(1.65), col_w, Inches(0.55), fill_color=c_accent, border_color=None)
        tb_b = s2.shapes.add_textbox(c_left + Inches(0.15), Inches(1.72), col_w - Inches(0.3), Inches(0.4))
        p_b = tb_b.text_frame.paragraphs[0]
        p_b.text = c_title
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = WHITE
        
        # Content box
        tb_c = s2.shapes.add_textbox(c_left + Inches(0.2), Inches(2.35), col_w - Inches(0.4), Inches(4.2))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        for j, pt in enumerate(points):
            p = tf_c.paragraphs[0] if j == 0 else tf_c.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: DATASET & TARGET FORMULATION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Dataset & Formulasi Target Prediksi",
               "Struktur Data Multivariat & Formulasi Realized Volatility 5-Hari Forward",
               "Pemisahan tegas antara 3.887 hari historis berlabel (2010–2024) dan 359 hari uji kompetisi (2025–2026).")
    add_footer(s3, 3)

    # Left: 2 Cards (Structure & Target)
    add_card(s3, Inches(0.8), Inches(1.65), Inches(5.7), Inches(2.55), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_d1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.3), Inches(2.3))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    p1 = tf_d1.paragraphs[0]
    p1.text = "1. Struktur Dataset Indonesia Financial Time Series"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_DARK
    
    bullets_d1 = [
        "Total Observasi: 4.266 baris perdagangan bursa harian (Senin–Jumat, 2010 s/d 2026).",
        "10 Prediktor Makro: USD/IDR, S&P 500, CBOE VIX, Minyak WTI, Emas Spot, IHSG, CPI (Inflasi), BI Policy Rate, US Fed Funds Rate.",
        "Segmentasi Partisi Data:",
        "  • Data Historis Berlabel: 2010–2024 (3.887 hari aktif pasca warm-up 20 hari).",
        "  • Data Uji Kompetisi (Test): Tepat 359 hari bursa (2 Jan 2025 s/d 22 Mei 2026)."
    ]
    for b in bullets_d1:
        p = tf_d1.add_paragraph()
        p.text = b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    add_card(s3, Inches(0.8), Inches(4.35), Inches(5.7), Inches(2.4), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_d2 = s3.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(5.3), Inches(2.1))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True
    p2 = tf_d2.paragraphs[0]
    p2.text = "2. Formulasi Target Prediksi: Target_Volatilitas_Y"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_DARK
    
    bullets_d2 = [
        "Definisi Target: Realized Volatility harian IHSG untuk jendela 5 hari bursa ke depan [t+1 s/d t+5].",
        "Karakteristik Finansial: Bersifat forward-looking murni; tidak boleh disentuh selama rekayasa fitur pada hari t.",
        "Status Data Uji: Seluruh 359 baris tahun 2025–2026 memiliki target NaN yang wajib diprediksi secara out-of-sample murni.",
        "Tantangan Analis: Membangun sistem bebas kebocoran waktu yang mampu mengantisipasi guncangan tanpa melihat masa depan."
    ]
    for b in bullets_d2:
        p = tf_d2.add_paragraph()
        p.text = b
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    # Right: Image fig_03_timeseries_macro.png
    add_image_framed(s3, 'outputs/eda/fig_03_timeseries_macro.png', Inches(6.75), Inches(1.65), Inches(5.78), Inches(5.1),
                     caption="Gambar 3.1: Ko-pergerakan Deret Waktu Multi-Aset Finansial Historis (2010–2024)")

    # =========================================================================
    # SLIDE 4: EDA & VOLATILITY CLUSTERING
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Exploratory Data Analysis (EDA)",
               "Distribusi Leptokurtik, Volatility Clustering, & Segmentasi Rezim Pasar",
               "Target memiliki ekor tebal krisis; pasar terbagi menjadi 95% rezim normal dan 5% rezim ekstrem.")
    add_footer(s4, 4)

    # Left: 3 Cards (Stats, Clustering, Regime)
    add_card(s4, Inches(0.8), Inches(1.65), Inches(5.5), Inches(1.6), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_s1 = s4.shapes.add_textbox(Inches(0.95), Inches(1.72), Inches(5.2), Inches(1.4))
    tf_s1 = tb_s1.text_frame
    tf_s1.word_wrap = True
    p = tf_s1.paragraphs[0]
    p.text = "1. Statistik Deskriptif Target (Target_Volatilitas_Y)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    stats_txt = [
        "Mean: 0,00793 | Median: 0,00698 | Std Dev: 0,00392 | Min: 0,00164 | Max: 0,04230",
        "Kemencengan Positif (Skewness > 2,4) & Ekor Tebal (Excess Kurtosis > 11,2).",
        "Menunjukkan distribusi leptokurtik khas finansial: tenang di mayoritas hari, namun rentan lonjakan krisis masif (Covid-19 2020 & Taper Tantrum 2013)."
    ]
    for st in stats_txt:
        p = tf_s1.add_paragraph()
        p.text = f"• {st}"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MAIN

    add_card(s4, Inches(0.8), Inches(3.38), Inches(5.5), Inches(1.6), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_s2 = s4.shapes.add_textbox(Inches(0.95), Inches(3.45), Inches(5.2), Inches(1.4))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    p = tf_s2.paragraphs[0]
    p.text = "2. Fenomena Volatility Clustering (Mandelbrot, 1963)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    clust_txt = [
        "Uji Autokorelasi (ACF) return absolut membuktikan dependensi temporal signifikan dan meluruh lambat (long memory).",
        "Hari-hari bergejolak cenderung diikuti oleh hari-hari bergejolak berikutnya.",
        "Implikasi Model: Model memori volatilitas adaptif mutlak diperlukan untuk menangkap pergeseran rezim varians."
    ]
    for cl in clust_txt:
        p = tf_s2.add_paragraph()
        p.text = f"• {cl}"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MAIN

    add_card(s4, Inches(0.8), Inches(5.1), Inches(5.5), Inches(1.65), fill_color=BLUE_LIGHT, border_color=BORDER_LIGHT)
    tb_s3 = s4.shapes.add_textbox(Inches(0.95), Inches(5.18), Inches(5.2), Inches(1.45))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    p = tf_s3.paragraphs[0]
    p.text = "3. Segmentasi Rezim Risiko (Threshold Persentil ke-95)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    reg_txt = [
        "Ambang Batas Terverifikasi Checkpoint 6.3: Y_threshold = 0,012650 (pada N=772 hari validasi OOF).",
        "Rezim Normal (Y <= 0,012650): 733 hari (94,95%) — fluktuasi stabil harian.",
        "Rezim Ekstrem (Y > 0,012650): 39 hari (5,05%) — turbulensi krisis pasar parah.",
        "Kunci Evaluasi: Model yang unggul di rezim normal wajib diuji ketahanannya pada rezim ekstrem."
    ]
    for rg in reg_txt:
        p = tf_s3.add_paragraph()
        p.text = f"• {rg}"
        p.font.size = Pt(9)
        p.font.color.rgb = NAVY_DARK

    # Right: Image fig_08_volatility_clustering.png
    add_image_framed(s4, 'outputs/eda/fig_08_volatility_clustering.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 4.1: Analisis Volatility Clustering & Autokorelasi Return Absolut IHSG")

    # =========================================================================
    # SLIDE 5: FEATURE ENGINEERING X1, X2, X3
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Task 1: Feature Engineering & Inovasi Sinyal",
               "Formulasi Tiga Fitur Turunan Inovatif Berbasis Makro & Finansial",
               "Menggabungkan kepanikan global, tekanan selisih suku bunga valas, dan guncangan komoditas dunia.")
    add_footer(s5, 5)

    feat_data = [
        ("X1: Fear Liquidity Composite",
         "X1_Fear_Liquidity_Robust",
         "VIX_t * ((USDIDR_t - MA20_t) / MA20_t)",
         "Kepanikan Ekuitas Global x Tekanan Depresiasi Kurs Valas",
         [
             "Rasionalitas: Saat VIX melonjak, investor global menarik dana (risk-off). Jika rupiah tertekan melebihi rata-rata 20 harinya, hal ini mengonfirmasi terjadinya pelarian modal valas (capital flight).",
             "Sifat Matematis: Rasio deviasi relatif menjaga skala fitur tetap stabil di tengah tren depresiasi struktural rupiah jangka panjang.",
             "Kinerja Model: Menembus Top-4 Feature Importance MDI pada model pohon Checkpoint 3A (bobot 9,92%)."
         ], BLUE_PRIMARY),
        ("X2: Rate Differential Pressure",
         "X2_Rate_Diff_Pressure_Abs",
         "|BI_rate_t - US_rate_t| * |ret5(USDIDR)_t|",
         "Selisih Suku Bunga Kebijakan x Momentum Kurs 5-Hari",
         [
             "Rasionalitas: Spread suku bunga adalah premi imbal hasil carry trade. Saat selisih menyempit bersamaan dengan lonjakan volatilitas kurs, posisi arbitrase dibongkar paksa (unwinding carry trade).",
             "Sifat Matematis: Nilai absolut mengukur intensitas stres moneter tanpa terganggu arah deviasi positif/negatif.",
             "Relevansi Pasar: Sangat sensitif terhadap siklus pengetatan moneter agresif The Fed (2022–2023)."
         ], EMERALD),
        ("X3: Commodity Macro Shock",
         "X3_Commodity_Shock_L2Norm",
         "sqrt(ret5(OIL)^2 + ret5(GOLD)^2 + ret5(SP500)^2)",
         "Norma Euclidean Guncangan Komoditas & Ekuitas Global",
         [
             "Rasionalitas: Minyak (energi/inflasi), Emas (safe haven), dan S&P 500 (pasar modal dunia) merefleksikan pergeseran rezim makroekonomi global simultan yang merambat ke IHSG.",
             "Sifat Matematis: Pengukuran vektor L2-norm mencegah pembatalan tanda (sign cancellation) antar aset.",
             "Ketahanan: Memberikan sinyal shock makro independen dari volatilitas lokal."
         ], AMBER)
    ]
    col_w5 = Inches(3.75)
    for i, (f_title, f_col, f_formula, f_sub, f_desc, f_accent) in enumerate(feat_data):
        c_left = Inches(0.8) + (i * Inches(4.0))
        add_card(s5, c_left, Inches(1.65), col_w5, Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
        
        # Header banner
        add_card(s5, c_left, Inches(1.65), col_w5, Inches(0.65), fill_color=f_accent, border_color=None)
        tb_h = s5.shapes.add_textbox(c_left + Inches(0.1), Inches(1.7), col_w5 - Inches(0.2), Inches(0.55))
        p = tb_h.text_frame.paragraphs[0]
        p.text = f_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p2 = tb_h.text_frame.add_paragraph()
        p2.text = f_col
        p2.font.size = Pt(9)
        p2.font.color.rgb = RGBColor(224, 231, 255)

        # Formula Card Box
        add_card(s5, c_left + Inches(0.15), Inches(2.4), col_w5 - Inches(0.3), Inches(0.65), fill_color=GREY_BG, border_color=BORDER_LIGHT)
        tb_f = s5.shapes.add_textbox(c_left + Inches(0.2), Inches(2.42), col_w5 - Inches(0.4), Inches(0.6))
        p_f = tb_f.text_frame.paragraphs[0]
        p_f.text = f_formula
        p_f.font.size = Pt(9.5)
        p_f.font.bold = True
        p_f.font.color.rgb = NAVY_DARK

        # Bullets
        tb_b = s5.shapes.add_textbox(c_left + Inches(0.15), Inches(3.15), col_w5 - Inches(0.3), Inches(3.4))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for j, pt in enumerate(f_desc):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p.text = f"•  {pt}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 6: HIPOTESIS EKONOMI & VALIDASI EMPIRIS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Task 1: Hipotesis Ekonomi & Validasi Empiris",
               "Transmisi Makroekonomi, Validasi Kuantitatif, & Batasan Kausalitas",
               "Fitur turunan terbukti berkontribusi signifikan; hubungan diposisikan sebagai sinyal prediktif murni.")
    add_footer(s6, 6)

    # Left: 3 Cards (Hypotheses, Feature Importance, Non-causal)
    add_card(s6, Inches(0.8), Inches(1.65), Inches(5.5), Inches(1.7), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_h1 = s6.shapes.add_textbox(Inches(0.95), Inches(1.72), Inches(5.2), Inches(1.5))
    tf_h1 = tb_h1.text_frame
    tf_h1.word_wrap = True
    p = tf_h1.paragraphs[0]
    p.text = "1. Hipotesis Transmisi Ekonomi ke Volatilitas IHSG"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    h_txt = [
        "Hipotesis X1: Risk-off sentimen global bertemu depresiasi rupiah memicu aksi jual asing (foreign outflow) pada saham LQ45, melipatgandakan varians IHSG.",
        "Hipotesis X2: Penyempitan spread suku bunga memicu penutupan carry trade, menekan likuiditas valas perbankan dan merambat ke pasar saham.",
        "Hipotesis X3: Guncangan energi & Wall Street menandai ketidakpastian premi risiko global yang direspons oleh repricing aset domestik."
    ]
    for h in h_txt:
        p = tf_h1.add_paragraph()
        p.text = f"• {h}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_card(s6, Inches(0.8), Inches(3.48), Inches(5.5), Inches(1.6), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_h2 = s6.shapes.add_textbox(Inches(0.95), Inches(3.55), Inches(5.2), Inches(1.4))
    tf_h2 = tb_h2.text_frame
    tf_h2.word_wrap = True
    p = tf_h2.paragraphs[0]
    p.text = "2. Uji Validitas Kuantitatif EDA & Bukti Model Nyata"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    val_txt = [
        "Korelasi Positif Kuat: Heatmap (fig_06) & ranking korelasi target (fig_07) mengonfirmasi keterikatan empiris signifikan terhadap Target_Volatilitas_Y.",
        "Scatter Heteroskedastisitas (fig_10): Lonjakan X1 dan X3 bertepatan dengan lonjakan varians target Y.",
        "Feature Importance Nyata: Pada model pohon Checkpoint 3A (fig_mod_03), X1 menempati peringkat ke-4 prediktor terkuat dengan kontribusi MDI 9,92%."
    ]
    for v in val_txt:
        p = tf_h2.add_paragraph()
        p.text = f"• {v}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_card(s6, Inches(0.8), Inches(5.2), Inches(5.5), Inches(1.55), fill_color=RGBColor(254, 242, 242), border_color=CRIMSON)
    tb_h3 = s6.shapes.add_textbox(Inches(0.95), Inches(5.28), Inches(5.2), Inches(1.35))
    tf_h3 = tb_h3.text_frame
    tf_h3.word_wrap = True
    p = tf_h3.paragraphs[0]
    p.text = "3. Integritas Ilmiah: Peringatan Anti-Klaim Kausalitas Palsu"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    nc_txt = [
        "Seluruh temuan korelasi dan feature importance mencerminkan kapasitas reduksi varians dan asosiasi prediktif statistik, BUKAN kausalitas hukum alam.",
        "Kenaikan X1 menyertai peningkatan risiko, tetapi menstabilkan X1 secara artifisial tidak otomatis meredam volatilitas IHSG.",
        "Pembedaan ini krusial agar Komite Risiko tidak salah mengartikan indikator peringatan dini sebagai tuas intervensi kebijakan."
    ]
    for nc in nc_txt:
        p = tf_h3.add_paragraph()
        p.text = f"• {nc}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = NAVY_DARK
        p.space_after = Pt(2)

    # Right: Image fig_mod_03_feature_importance.png
    add_image_framed(s6, 'outputs/models/fig_mod_03_feature_importance.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 6.1: Bukti Kontribusi MDI Feature Importance Model Pohon (Checkpoint 3A)")

    # =========================================================================
    # SLIDE 7: PROTOKOL VALIDASI TIME-SERIES & ANTI-LEAKAGE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Task 2: Protokol Validasi & Disiplin Anti-Leakage",
               "Pemisahan Kronologis Murni, Purging Horizon H=5, & Uji Invariansi Bebas Bocor",
               "Dilarang keras random split; integritas zero future information dibuktikan lewat automated unit test.")
    add_footer(s7, 7)

    # Left: 4 Cards
    add_card(s7, Inches(0.8), Inches(1.65), Inches(5.5), Inches(1.2), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_v1 = s7.shapes.add_textbox(Inches(0.95), Inches(1.7), Inches(5.2), Inches(1.05))
    tf_v1 = tb_v1.text_frame
    tf_v1.word_wrap = True
    p = tf_v1.paragraphs[0]
    p.text = "1. Expanding Walk-Forward Cross-Validation 3-Lipatan"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for b in [
        "Fold 1: Train 2010–2021 | Val 2022 (N=247 hari) — Era pengetatan moneter agresif.",
        "Fold 2: Train 2010–2022 | Val 2023 (N=246 hari) — Era suku bunga tinggi stabil.",
        "Fold 3: Train 2010–2023 | Val 2024 (N=279 hari) — Era All-Time High & Black Monday."
    ]:
        p = tf_v1.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    add_card(s7, Inches(0.8), Inches(2.95), Inches(5.5), Inches(1.25), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_v2 = s7.shapes.add_textbox(Inches(0.95), Inches(3.0), Inches(5.2), Inches(1.1))
    tf_v2 = tb_v2.text_frame
    tf_v2.word_wrap = True
    p = tf_v2.paragraphs[0]
    p.text = "2. Mekanisme Purging H=5 & Warm-Up Handling"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for b in [
        "Purging Horizon 5-Hari: 5 hari terakhir data train dieliminasi (train.iloc[:-5]) untuk mencegah overlap label target [t+1..t+5] dengan awal periode validasi.",
        "Warm-Up Window 20-Hari: Baris awal Januari 2010 dibersihkan menggunakan dropna() agar seluruh model menerima input matriks seragam (N=3.887)."
    ]:
        p = tf_v2.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    add_card(s7, Inches(0.8), Inches(4.3), Inches(5.5), Inches(1.35), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_v3 = s7.shapes.add_textbox(Inches(0.95), Inches(4.35), Inches(5.2), Inches(1.2))
    tf_v3 = tb_v3.text_frame
    tf_v3.word_wrap = True
    p = tf_v3.paragraphs[0]
    p.text = "3. Pipeline StandardScaler & Unit Test Invariance Bebas Bocor"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for b in [
        "Penskalaan Bersih: StandardScaler dibungkus Pipeline dan hanya di-fit pada X_train tiap fold; partisi validasi/test hanya menerima transform().",
        "Automated Invariance Unit Test (test_5_anti_leakage_invariance): Mutasi data masa depan (t+1..t+5) sebesar +1000% menghasilkan deviasi tepat 0,000000000000 pada fitur hari t."
    ]:
        p = tf_v3.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    add_card(s7, Inches(0.8), Inches(5.75), Inches(5.5), Inches(1.0), fill_color=BLUE_LIGHT, border_color=BORDER_LIGHT)
    tb_v4 = s7.shapes.add_textbox(Inches(0.95), Inches(5.8), Inches(5.2), Inches(0.85))
    tf_v4 = tb_v4.text_frame
    tf_v4.word_wrap = True
    p = tf_v4.paragraphs[0]
    p.text = "4. Transparansi Metodologis: Pseudo-Holdout 2024 & Isolasi Test"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    for b in [
        "Data 2024 diakui sebagai Pseudo-Holdout karena memengaruhi tuning model.",
        "Data uji 2025–2026 (359 baris) diisolasi 100% tanpa pernah dihitung performanya."
    ]:
        p = tf_v4.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = NAVY_DARK

    # Right: Image fig_val_01_timeline_split.png
    add_image_framed(s7, 'outputs/validation/fig_val_01_timeline_split.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 7.1: Skema Kronologis Expanding Walk-Forward Temporal Split & Purging H=5")

    # =========================================================================
    # SLIDE 8: BASELINE & MODEL CANDIDATES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Task 3: Baseline Benchmark & Kandidat Model",
               "Hierarki Model Pembanding & Algoritma Machine Learning",
               "Membangun benchmark yang tangguh untuk membuktikan nilai tambah riil machine learning.")
    add_footer(s8, 8)

    # 2 Big Cards
    col_w8 = Inches(5.7)
    
    # Left Card: Baselines
    add_card(s8, Inches(0.8), Inches(1.65), col_w8, Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    add_card(s8, Inches(0.8), Inches(1.65), col_w8, Inches(0.55), fill_color=SLATE_DARK, border_color=None)
    tb_bh = s8.shapes.add_textbox(Inches(1.0), Inches(1.72), col_w8 - Inches(0.4), Inches(0.4))
    p = tb_bh.text_frame.paragraphs[0]
    p.text = "A. HIERARKI MODEL BASELINE PEMBANDING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = WHITE

    base_items = [
        ("1. Baseline Naif Resmi Kompetisi (rv_past5)",
         "Formula: Rata-rata volatilitas 5 hari historis terakhir [t-4 s/d t].",
         "Kelemahan: Sangat reaktif dan rentan over-ekstrapolasi saat pasar mengalami flash crash sesaat.",
         "Performa: Pooled MAE = 0,002981 | Pooled RMSE = 0,004088 (Acuan Dasar Evaluasi)."),
        ("2. Baseline Persistensi Kuat (rv_past20)",
         "Formula: Rata-rata volatilitas 20 hari historis terakhir (1 bulan bursa).",
         "Karakteristik: Baseline yang jauh lebih kuat dan stabil, menjadi jangkar utama model time-series.",
         "Performa: Pooled MAE = 0,002675 | Pooled RMSE = 0,003540 (+10,3% vs naif)."),
        ("3. Baseline Constant Median",
         "Formula: Memprediksi nilai median tetap dari seluruh data latih.",
         "Kelemahan: Mengabaikan dinamika temporal; gagal mendeteksi lonjakan risiko.",
         "Performa: Pooled MAE = 0,003299 | Pooled RMSE = 0,004456 (-10,7% vs naif).")
    ]
    tb_bc = s8.shapes.add_textbox(Inches(1.0), Inches(2.35), col_w8 - Inches(0.4), Inches(4.2))
    tf_bc = tb_bc.text_frame
    tf_bc.word_wrap = True
    for title, fml, weak, perf in base_items:
        p = tf_bc.paragraphs[0] if tf_bc.paragraphs[0].text == "" else tf_bc.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = BLUE_DARK
        p.space_before = Pt(6)
        
        for desc in [fml, weak, perf]:
            p_sub = tf_bc.add_paragraph()
            p_sub.text = f"  • {desc}"
            p_sub.font.size = Pt(8.5)
            p_sub.font.color.rgb = TEXT_MAIN

    # Right Card: ML Candidates
    add_card(s8, Inches(6.8), Inches(1.65), col_w8, Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    add_card(s8, Inches(6.8), Inches(1.65), col_w8, Inches(0.55), fill_color=BLUE_PRIMARY, border_color=None)
    tb_mh = s8.shapes.add_textbox(Inches(7.0), Inches(1.72), col_w8 - Inches(0.4), Inches(0.4))
    p = tb_mh.text_frame.paragraphs[0]
    p.text = "B. KANDIDAT ALGORITMA MACHINE LEARNING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = WHITE

    ml_items = [
        ("1. Ridge Tuned (Linier Teratur L2)",
         "Pipeline: StandardScaler + Ridge(alpha=1000.0, random_state=42).",
         "Peran: Meredam multikolinearitas makro dan bertindak sebagai penstabil linier.",
         "Performa: Pooled MAE = 0,002476 (+16,9% vs naif) | Paling tahan guncangan ekstrem."),
        ("2. GBR Tuned (Single Champion Utama)",
         "Konfigurasi: loss='absolute_error', lr=0.03, max_depth=2, n_estimators=100.",
         "Peran: Menangkap interaksi non-linier orde kedua dan mengoptimalkan metrik MAE.",
         "Performa: Pooled MAE = 0,002462 (+17,4% vs naif) | Model tunggal terbaik."),
        ("3. Blend 60:40 (Ensemble Champion Utama)",
         "Komposisi: 60% GBR Tuned + 40% Ridge Tuned.",
         "Peran: Mengawinkan kepekaan pohon non-linier dengan ketahanan peredam Ridge.",
         "Performa: Pooled MAE = 0,002401 (+19,5% vs naif) | Rekomendasi Utama Tim."),
        ("4. Blend 50:30:20 (Hibrida Heuristik)",
         "Komposisi: 50% GBR + 30% Ridge + 20% rv_past20.",
         "Kelemahan: Terdistorsi pembobotan berlebih fitur naif saat pasar All-Time High.",
         "Performa: Pooled MAE 0,002377, namun tertinggal di Fold 2024 (0,002692 vs 0,002654).")
    ]
    tb_mc = s8.shapes.add_textbox(Inches(7.0), Inches(2.35), col_w8 - Inches(0.4), Inches(4.2))
    tf_mc = tb_mc.text_frame
    tf_mc.word_wrap = True
    for title, cfg, role, perf in ml_items:
        p = tf_mc.paragraphs[0] if tf_mc.paragraphs[0].text == "" else tf_mc.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = BLUE_DARK
        p.space_before = Pt(4)
        
        for desc in [cfg, role, perf]:
            p_sub = tf_mc.add_paragraph()
            p_sub.text = f"  • {desc}"
            p_sub.font.size = Pt(8.5)
            p_sub.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 9: HYPERPARAMETER TUNING & MODEL SELECTION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Task 3: Hyperparameter Tuning & Seleksi Model",
               "Pencarian Parameter Terkendali & Alasan Pemilihan Arsitektur",
               "Fungsi kerugian L1 dan pohon dangkal memberikan generalisasi optimal tanpa menghafal derau.")
    add_footer(s9, 9)

    # Left: 3 Cards (Grid, Technical Rationale, Ensemble Synergy)
    add_card(s9, Inches(0.8), Inches(1.65), Inches(5.5), Inches(1.5), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_t1 = s9.shapes.add_textbox(Inches(0.95), Inches(1.72), Inches(5.2), Inches(1.35))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "1. Ruang Pencarian Grid Search (Data Train/Val)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for pt in [
        "GBR Regressor: learning_rate in [0.01..0.10], max_depth in [2, 3, 4], loss in ['absolute_error', 'squared_error', 'huber'].",
        "Ridge Regressor: alpha in log-grid [10^-3, 10^-2, 10^-1, 1, 10, 100, 1000].",
        "Validasi: Evaluasi walk-forward temporal tanpa menyentuh data test kompetisi."
    ]:
        p = tf_t1.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_card(s9, Inches(0.8), Inches(3.28), Inches(5.5), Inches(1.85), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_t2 = s9.shapes.add_textbox(Inches(0.95), Inches(3.35), Inches(5.2), Inches(1.7))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]
    p.text = "2. Alasan Teknis Penetapan GBR Tuned (Single Champion)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for pt in [
        "Loss L1 (absolute_error): Secara matematis mengestimasi median bersyarat, langsung meminimalkan metrik MAE kompetisi dan kebal terhadap outlier lonjakan krisis 2020.",
        "Pohon Dangkal (max_depth=2): Membatasi kapasitas interaksi hanya hingga orde ke-2, mencegah penghafalan derau (noise memorization) pada data finansial.",
        "Learning Rate Konservatif (0.03): Menghasilkan kurva konvergensi paling halus pada 100 estimator tanpa risiko overfitting."
    ]:
        p = tf_t2.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    add_card(s9, Inches(0.8), Inches(5.25), Inches(5.5), Inches(1.5), fill_color=BLUE_LIGHT, border_color=BORDER_LIGHT)
    tb_t3 = s9.shapes.add_textbox(Inches(0.95), Inches(5.32), Inches(5.2), Inches(1.35))
    tf_t3 = tb_t3.text_frame
    tf_t3.word_wrap = True
    p = tf_t3.paragraphs[0]
    p.text = "3. Sinergi Arsitektur Blend 60:40 (GBR + Ridge)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    for pt in [
        "Pilar Ridge alpha=1000.0 menekan multikolinearitas prediktor makro dan bertindak sebagai penstabil (anchor) yang meredam over-reaksi pohon saat pasar panik.",
        "Kombinasi 60:40 mempertahankan akurasi tinggi di kondisi normal dan ketahanan superior saat krisis ekstrem."
    ]:
        p = tf_t3.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = NAVY_DARK
        p.space_after = Pt(2)

    # Right: Image fig_tune_01_grid_search_curves.png
    add_image_framed(s9, 'outputs/tuning/fig_tune_01_grid_search_curves.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 9.1: Kurva Validasi Grid Search Hyperparameter GBR dan Ridge")

    # =========================================================================
    # SLIDE 10: PERBANDINGAN EVALUASI & METRIK TERVERIFIKASI
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Task 3: Hasil Evaluasi & Benchmark Akurasi",
               "Pembuktian Benchmark: Keunggulan +19,5% vs Baseline Naif",
               "Angka hasil rekonsiliasi terverifikasi Checkpoint 6.3 pada 772 hari validasi out-of-fold sebanding.")
    add_footer(s10, 10)

    # Table of Reconciled Metrics
    table_shape = s10.shapes.add_table(6, 7, Inches(0.8), Inches(1.65), Inches(11.733), Inches(2.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.733) # Model
    table.columns[1].width = Inches(1.4)   # Pooled MAE
    table.columns[2].width = Inches(1.4)   # Pooled RMSE
    table.columns[3].width = Inches(1.4)   # Fold 1
    table.columns[4].width = Inches(1.4)   # Fold 2
    table.columns[5].width = Inches(1.4)   # Fold 3
    table.columns[6].width = Inches(2.0)   # Keunggulan MAE vs rv_past5

    headers = ["Model / Konfigurasi", "Pooled MAE", "Pooled RMSE", "Fold 1 (2022)", "Fold 2 (2023)", "Fold 3 (2024)", "Keunggulan vs rv_past5"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    table_rows = [
        ("Baseline Naif Resmi (rv_past5)", "0,002981", "0,004088", "0,002956", "0,002636", "0,003348", "Acuan Dasar", WHITE, TEXT_MAIN),
        ("Baseline Persistensi (rv_past20)", "0,002675", "0,003540", "0,002599", "0,002210", "0,003232", "+10,3% (vs naif)", GREY_BG, TEXT_MAIN),
        ("GBR Tuned (Single Champion)", "0,002462", "0,003178", "0,002404", "0,002334", "0,002646", "+17,4% (Unggul)", WHITE, BLUE_DARK),
        ("Blend 60:40 (Ensemble Champion)", "0,002401", "0,003152", "0,002302", "0,002246", "0,002654", "+19,5% (Unggul Mutlak)", BLUE_LIGHT, EMERALD),
        ("Blend 50:30:20 (Hibrida Heuristik)", "0,002377", "0,003144", "0,002244", "0,002194", "0,002692", "+20,3% (Tertinggal F3)", GREY_BG, TEXT_MUTED)
    ]
    for row_idx, r_data in enumerate(table_rows, start=1):
        for col_idx in range(7):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = r_data[7]
            p = cell.text_frame.paragraphs[0]
            p.text = r_data[col_idx]
            p.font.size = Pt(9)
            p.font.color.rgb = r_data[8] if col_idx in [0, 1, 6] else TEXT_MAIN
            p.font.bold = True if col_idx in [0, 1, 6] or row_idx == 4 else False
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Bottom Split: Left Card (Extreme Regimes) + Right Card (Key Takeaways)
    add_card(s10, Inches(0.8), Inches(4.05), Inches(5.7), Inches(2.7), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_b1 = s10.shapes.add_textbox(Inches(1.0), Inches(4.15), Inches(5.3), Inches(2.5))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    p = tf_b1.paragraphs[0]
    p.text = "Ketahanan pada Rezim Pasar Ekstrem (Top 5% Teratas)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    ext_points = [
        "Definisi: Y > 0,012650 (N=39 hari bursa paling turbulen).",
        "Ridge Tuned: MAE Ekstrem = 0,007683 (Paling tahan guncangan).",
        "Blend 60:40: MAE Ekstrem = 0,007778 (Lebih tangguh dari GBR & Blend 50:30:20).",
        "Blend 50:30:20: MAE Ekstrem = 0,007858.",
        "GBR Tuned: MAE Ekstrem = 0,007882.",
        "Insight: Pilar Ridge terbukti meredam estimasi berlebih non-linier saat pasar panik."
    ]
    for ep in ext_points:
        p = tf_b1.add_paragraph()
        p.text = f"• {ep}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    add_card(s10, Inches(6.8), Inches(4.05), Inches(5.733), Inches(2.7), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_b2 = s10.shapes.add_textbox(Inches(7.0), Inches(4.15), Inches(5.3), Inches(2.5))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "Analisis Keputusan Champion (Blend 60:40 vs 50:30:20)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    takeaways = [
        "Validasi Adil & Sah: Seluruh metrik dihitung pada tepat 772 hari validasi out-of-fold yang persis sebanding.",
        "Keunggulan Sah: Blend 60:40 unggul +19,5% vs rv_past5 dan +10,2% vs rv_past20.",
        "Mengapa Blend 60:40 Dipilih?:",
        "  • Pada Fold 2024 (IHSG All-Time High), kinerja Blend 50:30:20 anjlok (MAE 0,002692) akibat pembobotan berlebih fitur naif rv20.",
        "  • Blend 60:40 lebih unggul di Fold 2024 (MAE 0,002654) dan lebih tahan guncangan ekstrem (0,007778 vs 0,007858).",
        "  • Mempertahankan dekomposisi Explainable AI murni tanpa bobot heuristik."
    ]
    for tk in takeaways:
        p = tf_b2.add_paragraph()
        p.text = f"• {tk}" if not tk.startswith("  •") else tk
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 11: GLOBAL XAI SHAP SUMMARY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Task 3: Explainable AI — Penjelasan Global (Global XAI)",
               "Dekomposisi SHAP Global: Membongkar Logika Internal Model",
               "Volatilitas historis, momentum indeks, suku bunga Fed, dan VIX mendominasi arah prediksi model.")
    add_footer(s11, 11)

    # Left: Ranking Card & Insights
    add_card(s11, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_g = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.1), Inches(4.8))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    p = tf_g.paragraphs[0]
    p.text = "Ranking Atribusi Fitur Global (mean |SHAP|)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    
    g_items = [
        ("1. rv_past20 (0,000466)", "Jangkar memori volatilitas historis lokal utama. Nilai tinggi mendorong prediksi naik."),
        ("2. mom_ihsg_10 (0,000294)", "Asymmetric Leverage Effect: Penurunan tajam indeks 10-hari mendorong lonjakan ekspektasi volatilitas."),
        ("3. US_rate (0,000231)", "Suku bunga The Fed tinggi memperlebar premi risiko dan membatasi likuiditas pasar berkembang."),
        ("4. VIX (0,000188)", "Kepanikan Wall Street mentransmisikan ketakutan langsung ke sentimen pelaku pasar domestik."),
        ("5. rv_past5 (0,000186)", "Volatilitas jangka pendek lokal."),
        ("6. X1_Fear_Liquidity (0,000142)", "Fitur turunan penguat guncangan saat VIX dan kurs tertekan.")
    ]
    for f_name, f_exp in g_items:
        p = tf_g.add_paragraph()
        p.text = f_name
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = BLUE_PRIMARY
        p.space_before = Pt(6)
        
        p2 = tf_g.add_paragraph()
        p2.text = f"  • {f_exp}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MAIN

    p_bot = tf_g.add_paragraph()
    p_bot.text = "Sifat Aditif Eksak Blend 60:40:"
    p_bot.font.size = Pt(9.5)
    p_bot.font.bold = True
    p_bot.font.color.rgb = NAVY_DARK
    p_bot.space_before = Pt(8)
    p_bot2 = tf_g.add_paragraph()
    p_bot2.text = "Superposisi linier antara TreeSHAP (GBR) dan koefisien linier terstandarisasi (Ridge) memiliki deviasi rekonstruksi < 10^-10 (sempurna)."
    p_bot2.font.size = Pt(8.5)
    p_bot2.font.color.rgb = TEXT_MUTED

    # Right: Image fig_xai_02_shap_summary_beeswarm.png
    add_image_framed(s11, 'outputs/xai/fig_xai_02_shap_summary_beeswarm.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 11.1: SHAP Summary Beeswarm Plot — Distribusi & Arah Dampak Fitur")

    # =========================================================================
    # SLIDE 12: LOCAL XAI KASUS 11 MEI 2022
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Task 3: Explainable AI — Penjelasan Lokal (Local XAI)",
               "Deteksi Dini Puncak Krisis 11 Mei 2022 & Penerjemahan Bahasa Bisnis",
               "Model sukses memancarkan sinyal bahaya risiko tinggi (0,012739 vs aktual 0,019739) pasca-Lebaran & kenaikan Fed Rate 50 bps.")
    add_footer(s12, 12)

    # Left: Context & Business Table
    add_card(s12, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_l = s12.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.1), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Studi Kasus: Puncak Turbulensi 11 Mei 2022"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    
    ctx_pts = [
        "Konteks: Pembukaan bursa pasca-libur panjang Idul Fitri 1443 H + The Fed menaikkan suku bunga 50 bps (tertinggi dalam 22 tahun).",
        "Target Riil: Melonjak ekstrem ke Y = 0,019739 (Persentil ke-99,5).",
        "Prediksi Model: Melonjak tajam dari base value 0,007949 ke 0,012739 (Blend 60:40) dan 0,012095 (GBR) — Red Alert Aktif!"
    ]
    for cp in ctx_pts:
        p = tf_l.add_paragraph()
        p.text = f"• {cp}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN

    p_tbl = tf_l.add_paragraph()
    p_tbl.text = "Penerjemahan Bahasa Bisnis untuk Direksi PT Investion:"
    p_tbl.font.size = Pt(10)
    p_tbl.font.bold = True
    p_tbl.font.color.rgb = NAVY_DARK
    p_tbl.space_before = Pt(8)

    bus_trans = [
        ("VIX = 32,56 (SHAP +0,001599)", "Premi Kepanikan Global: Wall Street menembus ambang batas krisis (>30), menulari aset berisiko."),
        ("mom_ihsg_5 = -8,72% (SHAP +0,001228)", "Aksi Jual Panik: IHSG anjlok bebas -8,7% sepekan memicu kepanikan likuiditas domestik."),
        ("mom_ihsg_10 = -6,85% (SHAP +0,001071)", "Pelemahan Tren: Kerusakan tren 2 pekan mengonfirmasi ketiadaan minat beli (no bids)."),
        ("IHSG = 6.816 (SHAP -0,000283)", "Faktor Penahan: Valuasi indeks yang terkoreksi memberikan sedikit bantalan valuasi.")
    ]
    for b_title, b_desc in bus_trans:
        p = tf_l.add_paragraph()
        p.text = f"▲ {b_title}" if not "Penahan" in b_desc else f"▼ {b_title}"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CRIMSON if not "Penahan" in b_desc else BLUE_DARK
        p.space_before = Pt(4)
        
        p2 = tf_l.add_paragraph()
        p2.text = f"   {b_desc}"
        p2.font.size = Pt(8)
        p2.font.color.rgb = TEXT_MAIN

    # Right: Image fig_xai_03_local_explanations.png
    add_image_framed(s12, 'outputs/xai/fig_xai_03_local_explanations.png', Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1),
                     caption="Gambar 12.1: Local Waterfall Plot Dekomposisi Atribusi SHAP (11 Mei 2022)")

    # =========================================================================
    # SLIDE 13: XAI ERROR ANALYSIS BLACK MONDAY 2024
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Task 3: Analisis Kesalahan Berbasis XAI (Error Analysis)",
               "Audit Forensik Kesalahan Prediksi: Studi Kasus Black Monday Agustus 2024",
               "Membedah underprediction 31 Juli 2024 (kejutan eksogen) dan overprediction 5 Agustus 2024 (reversi kilat 48 jam).")
    add_footer(s13, 13)

    c_w13 = Inches(5.7)
    
    # Left: Case 1
    add_card(s13, Inches(0.8), Inches(1.65), c_w13, Inches(2.65), fill_color=WHITE, border_color=BORDER_LIGHT)
    add_card(s13, Inches(0.8), Inches(1.65), c_w13, Inches(0.42), fill_color=CRIMSON, border_color=None)
    tb_c1h = s13.shapes.add_textbox(Inches(0.95), Inches(1.7), c_w13 - Inches(0.3), Inches(0.35))
    p = tb_c1h.text_frame.paragraphs[0]
    p.text = "KASUS 1: UNDERPREDICTION EKSTREM (31 JULI 2024)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_c1b = s13.shapes.add_textbox(Inches(0.95), Inches(2.15), c_w13 - Inches(0.3), Inches(2.1))
    tf_c1b = tb_c1b.text_frame
    tf_c1b.word_wrap = True
    c1_content = [
        "• Target Aktual vs Prediksi: Y = 0,019251 | Prediksi = 0,005825 (Residual +0,013426).",
        "• Konteks EOD 31 Juli: IHSG menguat +0,19% di 7.255; VIX tenang 16,36; varians 20-hari sangat rendah (0,0052).",
        "• Atribusi SHAP: rv_past20 (-0,000670), US_rate (-0,000473), IHSG (-0,000349) menarik prediksi ke bawah.",
        "• Akar Masalah & Batasan: Likuidasi Yen carry trade baru meledak pada t+3 (5 Agustus). Model time-series bebas bocor secara logis tidak dapat mendeteksi kejutan eksogen masa depan sebelum tercermin di harga."
    ]
    for idx, desc in enumerate(c1_content):
        p = tf_c1b.paragraphs[0] if idx == 0 else tf_c1b.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    # Right: Case 2
    add_card(s13, Inches(6.8), Inches(1.65), c_w13, Inches(2.65), fill_color=WHITE, border_color=BORDER_LIGHT)
    add_card(s13, Inches(6.8), Inches(1.65), c_w13, Inches(0.42), fill_color=AMBER, border_color=None)
    tb_c2h = s13.shapes.add_textbox(Inches(6.95), Inches(1.7), c_w13 - Inches(0.3), Inches(0.35))
    p = tb_c2h.text_frame.paragraphs[0]
    p.text = "KASUS 2: OVERPREDICTION EKSTREM (5 AGUSTUS 2024)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = WHITE

    tb_c2b = s13.shapes.add_textbox(Inches(6.95), Inches(2.15), c_w13 - Inches(0.3), Inches(2.1))
    tf_c2b = tb_c2b.text_frame
    tf_c2b.word_wrap = True
    c2_content = [
        "• Target Aktual vs Prediksi: Y = 0,005503 | Prediksi = 0,012314 (Residual -0,006811).",
        "• Konteks EOD 5 Agustus: Nikkei -12,4%, IHSG -3,40%, VIX meroket ke level krisis 38,57. Model memprediksi volatilitas 0,012314.",
        "• Atribusi SHAP: VIX (+0,001895) dan mom_ihsg_5 (+0,000977) mendominasi lonjakan prediksi (>65% deviasi).",
        "• Akar Masalah & Keunggulan ML: Over-ekstrapolasi memori krisis. Namun intervensi BoJ 7 Agustus meredakan kepanikan seketika (reversi 48 jam). Model ML memangkas error baseline naif (0,016621) sebesar 38,7%!"
    ]
    for idx, desc in enumerate(c2_content):
        p = tf_c2b.paragraphs[0] if idx == 0 else tf_c2b.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(2)

    # Bottom: Image fig_err_01_timeline_context.png
    add_image_framed(s13, 'outputs/xai/error_analysis/fig_err_01_timeline_context.png', Inches(0.8), Inches(4.42), Inches(11.733), Inches(2.5),
                     caption="Gambar 13.1: Konteks Kronologis Peristiwa Black Monday Agustus 2024 & Dinamika Koreksi Pasca-Intervensi BoJ")

    # =========================================================================
    # SLIDE 14: REKOMENDASI PORTOFOLIO & BATASAN MODEL
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Tata Kelola Etis & Rekomendasi Portofolio PT Investion",
               "Batasan Model, Kerangka Tiga Lapis, & Kebijakan Operasional Mitigasi Risiko",
               "Pemisahan fakta vs atribusi XAI vs interpretasi ekonomi untuk memandu keputusan alokasi triliunan rupiah.")
    add_footer(s14, 14)

    # Left: Governance & Limits
    add_card(s14, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_gov = s14.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.1), Inches(4.9))
    tf_gov = tb_gov.text_frame
    tf_gov.word_wrap = True
    p = tf_gov.paragraphs[0]
    p.text = "1. Tata Kelola Etis & Batasan Model Kuantitatif"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_DARK
    
    gov_pts = [
        ("Kerangka Evaluasi Tiga Lapis:", "Pemisahan disiplin antara Fakta Komputasi (data bursa & residual) vs Atribusi XAI (kontribusi marjinal fungsi) vs Interpretasi Finansial (mekanisme pasar)."),
        ("Asimetri Kejutan Eksogen (No Prescience):", "Model EOD tidak memiliki bola kristal untuk meramalkan keputusan bank sentral tengah malam sebelum tercermin di harga."),
        ("Risiko Alarm Berlebih pada Flash Crash:", "Sensitivitas tinggi terhadap VIX dapat memicu false alarm saat guncangan likuiditas mereda kilat."),
        ("Non-Causal Disclaimer:", "Nilai SHAP bukan dalil intervensi kausalitas kebijakan moneter."),
        ("Deklarasi Data Uji 2025–2026:", "Prediksi 359 hari dihasilkan out-of-sample murni tanpa klaim akurasi terkonfirmasi karena target dirahasiakan.")
    ]
    for title, desc in gov_pts:
        p = tf_gov.add_paragraph()
        p.text = title
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = BLUE_PRIMARY
        p.space_before = Pt(4)
        p2 = tf_gov.add_paragraph()
        p2.text = f"  • {desc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MAIN

    # Right: 3 Operational Recommendations
    add_card(s14, Inches(6.55), Inches(1.65), Inches(5.98), Inches(5.1), fill_color=WHITE, border_color=BORDER_LIGHT)
    tb_rec = s14.shapes.add_textbox(Inches(6.75), Inches(1.75), Inches(5.6), Inches(4.9))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True
    p = tf_rec.paragraphs[0]
    p.text = "2. Tiga Rekomendasi Kebijakan Komite Risiko PT Investion"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    
    recs = [
        ("A. Dual-Speed Early Warning Architecture",
         "• Kecepatan Rendah (Model EOD Harian): Prediksi Blend 60:40 memandu alokasi portofolio harian dan perhitungan Value at Risk (VaR) 5-hari forward.\n"
         "• Kecepatan Tinggi (Intraday Circuit Breaker): Jika VIX global melonjak >20% dalam satu sesi perdagangan saat BEI tutup, status Yellow Alert otomatis aktif."),
        ("B. Strategi Lindung Nilai Adaptif (Anti-Panic Fire-Sale)",
         "• Saat model memprediksi volatilitas ekstrem yang didorong lonjakan VIX sesaat (kasus 5 Agustus), dilarang likuidasi panik saham yang mengunci kerugian modal.\n"
         "• Terapkan instrumen derivatif lindung nilai sintetis (protective put/collar) atau naikkan instrumen pasar uang durasi pendek."),
        ("C. Dinamika Alokasi Aset Taktikal Tiga Koridor",
         "• Rezim Tenang (Y_pred < 0,0060): Ekuitas agresif 90–95% (fokus beta tinggi).\n"
         "• Rezim Waspada (0,0060 <= Y_pred <= 0,0120): Ekuitas netral 75–80% (defensif).\n"
         "• Rezim Krisis (Y_pred > 0,0120): Pangkas ekuitas ke 50–60%, maksimalkan kas/SBN.")
    ]
    for r_title, r_desc in recs:
        p = tf_rec.add_paragraph()
        p.text = r_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = BLUE_DARK
        p.space_before = Pt(6)
        p2 = tf_rec.add_paragraph()
        p2.text = r_desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 15: KESIMPULAN AKHIR & KETERLACAKAN ARTEFAK
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Kesimpulan Akhir & Matriks Keterlacakan Artefak",
               "Integritas Metodologis Sempurna, Keunggulan Prediktif Tervalidasi, & Siap Diuji",
               "Seluruh persyaratan Task 1, 2, 3 terpenuhi 100% dan terpetakan ke artefak komputasi sumber.")
    add_footer(s15, 15)

    # 3 Summary Cards across top
    sum_cards = [
        ("100% Kepatuhan Studi Kasus",
         "Seluruh 19 butir evaluasi Task 1, 2, dan 3 berstatus COMPLETE 100% dengan bukti nyata kode, visualisasi, dan laporan formal.",
         BLUE_PRIMARY),
        ("Keunggulan Prediktif Sah",
         "Blend 60:40 unggul +19,5% vs baseline naif resmi (rv_past5) dan +10,2% vs persistensi pada 772 hari validasi OOF sebanding.",
         EMERALD),
        ("Integritas Berkas Submisi",
         "Berkas submission 359-baris dan dataset 4.266-baris terverifikasi 100% bebas NaN, bebas inf, dan konsisten terhadap profil historis.",
         BLUE_DARK)
    ]
    c_w15 = Inches(3.75)
    for i, (sc_title, sc_desc, sc_color) in enumerate(sum_cards):
        c_left = Inches(0.8) + (i * Inches(4.0))
        add_card(s15, c_left, Inches(1.65), c_w15, Inches(1.6), fill_color=WHITE, border_color=BORDER_LIGHT)
        banner = add_card(s15, c_left, Inches(1.65), c_w15, Inches(0.4), fill_color=sc_color, border_color=None)
        tb = s15.shapes.add_textbox(c_left + Inches(0.1), Inches(1.7), c_w15 - Inches(0.2), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = sc_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        tb_d = s15.shapes.add_textbox(c_left + Inches(0.15), Inches(2.12), c_w15 - Inches(0.3), Inches(1.05))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = tf_d.margin_right = tf_d.margin_bottom = 0
        p_d = tf_d.paragraphs[0]
        p_d.text = sc_desc
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = TEXT_MAIN

    # Bottom: Traceability Matrix Table
    tb_head = s15.shapes.add_textbox(Inches(0.8), Inches(3.35), Inches(11.733), Inches(0.3))
    p = tb_head.text_frame.paragraphs[0]
    p.text = "MATRIKS KETERLACAKAN KOMPUTASI (COMPUTATIONAL TRACEABILITY MATRIX)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    t15_shape = s15.shapes.add_table(6, 4, Inches(0.8), Inches(3.7), Inches(11.733), Inches(2.95))
    t15 = t15_shape.table
    t15.columns[0].width = Inches(2.8)
    t15.columns[1].width = Inches(2.0)
    t15.columns[2].width = Inches(4.0)
    t15.columns[3].width = Inches(2.933)

    t15_headers = ["Parameter / Metrik Kunci", "Nilai Terverifikasi", "File Artefak Komputasi Sumber", "Rujukan Sel / Baris Kode"]
    for c_idx, h in enumerate(t15_headers):
        cell = t15.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER if c_idx == 1 else PP_ALIGN.LEFT

    t15_rows = [
        ("Baseline rv_past5 (Naif)", "MAE 0,002981 | RMSE 0,004088", "notebook/02_Validation_Baseline.ipynb", "Cell 10 (evaluate_baseline_models)"),
        ("Baseline rv_past20 (Persistensi)", "MAE 0,002675 | RMSE 0,003540", "notebook/02_Validation_Baseline.ipynb", "Cell 10 (evaluate_baseline_models)"),
        ("Blend 60:40 (Ensemble Champion)", "MAE 0,002401 (+19,5% vs naif)", "notebook/05_Robustness_Model_Selection.ipynb", "Cell 6 (blending_grid_evaluation)"),
        ("Threshold Rezim Ekstrem 95th", "Y_threshold = 0,012650 (N=39)", "notebook/06_Reconciliation_Audit.ipynb", "Cell 8 (pct95 = percentile(y, 95))"),
        ("Invariansi Anti-Leakage (Zero Diff)", "Deviasi = 0,000000000000", "scripts/feature_engineering.py", "Line 240-285 (test_5_anti_leakage)")
    ]
    for r_idx, r_data in enumerate(t15_rows, start=1):
        for c_idx in range(4):
            cell = t15.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else GREY_BG
            p = cell.text_frame.paragraphs[0]
            p.text = r_data[c_idx]
            p.font.size = Pt(8.5)
            p.font.color.rgb = BLUE_DARK if c_idx == 1 else TEXT_MAIN
            p.font.bold = True if c_idx in [0, 1] else False
            p.alignment = PP_ALIGN.CENTER if c_idx == 1 else PP_ALIGN.LEFT

    # Save Presentation
    print(f"Saving Presentation to {OUTPUT_PPTX}...")
    prs.save(OUTPUT_PPTX)
    size_kb = os.path.getsize(OUTPUT_PPTX) / 1024
    print(f"[SUCCESS] PowerPoint presentation generated successfully: {OUTPUT_PPTX} ({size_kb:.1f} KB)")
    return OUTPUT_PPTX

if __name__ == '__main__':
    build_presentation()
