"""
Script to generate rigorous, publication-grade XAI Error Analysis visualizations
for Checkpoint 6.1 (Underprediction on 2024-07-31 and Overprediction on 2024-08-05).
Output directory: outputs/xai/error_analysis/
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

PROJECT_ROOT = r'z:\Projects\Inception'
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.feature_engineering import preprocess_usdidr, engineer_features
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import shap

# Visualization Styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9.5
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 13

C_BLUE   = '#2563EB'
C_RED    = '#DC2626'
C_GREEN  = '#16A34A'
C_ORANGE = '#D97706'
C_PURPLE = '#7C3AED'
C_GRAY   = '#6B7280'
C_DARK   = '#1F2937'

OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'outputs', 'xai', 'error_analysis')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset and running feature pipeline...")
df_raw = pd.read_csv(os.path.join(PROJECT_ROOT, 'Aset Lomba', 'dataset peserta.csv'))
df_clean, _ = preprocess_usdidr(df_raw)
df_feat = engineer_features(df_clean, use_cleaned_usdidr=True)

feature_cols = [c for c in df_feat.columns if c not in ['Date', 'Target_Volatilitas_Y', 'USDIDR_raw']]
labeled_df = df_feat[df_feat['Target_Volatilitas_Y'].notna()].dropna(subset=feature_cols).copy().reset_index(drop=True)
labeled_df['Date'] = pd.to_datetime(labeled_df['Date'])

# Fold 3 Setup
train_fold3 = labeled_df[labeled_df['Date'] <= '2023-12-31'].iloc[:-5].copy()
val_fold3 = labeled_df[(labeled_df['Date'] >= '2024-01-01') & (labeled_df['Date'] <= '2024-12-17')].copy().reset_index(drop=True)

X_tr = train_fold3[feature_cols].values
y_tr = train_fold3['Target_Volatilitas_Y'].values

X_v = val_fold3[feature_cols].values
y_v = val_fold3['Target_Volatilitas_Y'].values

# Fit GBR Tuned
gbr = GradientBoostingRegressor(
    loss='absolute_error',
    learning_rate=0.03,
    max_depth=2,
    n_estimators=100,
    min_samples_leaf=1,
    random_state=42
)
gbr.fit(X_tr, y_tr)
p_gbr = gbr.predict(X_v)

explainer = shap.TreeExplainer(gbr)
gbr_shap = explainer.shap_values(X_v)
gbr_base = float(explainer.expected_value if not isinstance(explainer.expected_value, np.ndarray) else explainer.expected_value[0])

# Fit Ridge Tuned
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_v_s = scaler.transform(X_v)

ridge = Ridge(alpha=1000.0, random_state=42)
ridge.fit(X_tr_s, y_tr)
p_ridge = ridge.predict(X_v_s)

ridge_shap = X_v_s * ridge.coef_
ridge_base = float(ridge.intercept_)

# Blend 60:40
p_blend60 = 0.60 * p_gbr + 0.40 * p_ridge
blend60_shap = 0.60 * gbr_shap + 0.40 * ridge_shap
blend60_base = 0.60 * gbr_base + 0.40 * ridge_base

# Blend 50:30:20
rv20_idx = feature_cols.index('rv_past20')
p_rv20 = val_fold3['rv_past20'].values
mu_rv20 = float(train_fold3['rv_past20'].mean())
p_blend50 = 0.50 * p_gbr + 0.30 * p_ridge + 0.20 * p_rv20
blend50_shap = 0.50 * gbr_shap + 0.30 * ridge_shap
blend50_shap[:, rv20_idx] += 0.20 * (p_rv20 - mu_rv20)
blend50_base = 0.50 * gbr_base + 0.30 * ridge_base + 0.20 * mu_rv20

# Add predictions to val_fold3 dataframe for convenient plotting
val_fold3['p_gbr'] = p_gbr
val_fold3['p_ridge'] = p_ridge
val_fold3['p_blend60'] = p_blend60
val_fold3['p_blend50'] = p_blend50
val_fold3['err_blend60'] = val_fold3['Target_Volatilitas_Y'] - p_blend60
val_fold3['abs_err_blend60'] = np.abs(val_fold3['err_blend60'])

# =============================================================================
# FIGURE 1: TIMELINE CONTEXT (Black Monday July-August 2024 Dynamics)
# =============================================================================
print("Generating Figure 1: Timeline Context...")
fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True, gridspec_kw={'height_ratios': [1.2, 1, 1.3]})

# Filter timeline window: 2024-07-15 to 2024-08-30
window_df = val_fold3[(val_fold3['Date'] >= '2024-07-15') & (val_fold3['Date'] <= '2024-08-30')].copy()

# Panel 1: IHSG Index & Daily Return
ax1 = axes[0]
ax1_twin = ax1.twinx()
ax1.plot(window_df['Date'], window_df['IHSG'], color=C_DARK, linewidth=2, label='IHSG Index (Close)')
bar_colors = [C_GREEN if r >= 0 else C_RED for r in window_df['IHSG_ret']]
ax1_twin.bar(window_df['Date'], window_df['IHSG_ret'] * 100, color=bar_colors, alpha=0.35, width=0.6, label='Daily Return (%)')
ax1.set_ylabel('IHSG Level', fontweight='bold', color=C_DARK)
ax1_twin.set_ylabel('Daily Return (%)', fontweight='bold', color=C_GRAY)
ax1.set_title('A. Pergerakan IHSG & Kejutan "Black Monday" 5 Agustus 2024 (Kejatuhan -3.40%)', fontweight='bold', loc='left')

# Annotations for both cases
d_under = pd.to_datetime('2024-07-31')
d_crash = pd.to_datetime('2024-08-05')

ax1.axvline(d_under, color=C_BLUE, linestyle='--', linewidth=1.5, alpha=0.85)
ax1.annotate('KASUS 1: 31 Juli 2024\nEOD Tenang (IHSG 7.255, VIX 16.4)\nModel Prediksi Rendah', 
             xy=(d_under, 7255.76), xytext=(pd.to_datetime('2024-07-18'), 7350),
             arrowprops=dict(facecolor=C_BLUE, shrink=0.08, width=1.5, headwidth=6),
             fontweight='bold', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor=C_BLUE))

ax1.axvline(d_crash, color=C_RED, linestyle='--', linewidth=1.5, alpha=0.85)
ax1.annotate('KASUS 2: 5 Agustus 2024\nPuncak Crash (IHSG 7.059, VIX 38.6)\nModel Over-Extrapolasi', 
             xy=(d_crash, 7059.65), xytext=(pd.to_datetime('2024-08-08'), 6950),
             arrowprops=dict(facecolor=C_RED, shrink=0.08, width=1.5, headwidth=6),
             fontweight='bold', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor=C_RED))

# Panel 2: VIX & USD/IDR
ax2 = axes[1]
ax2_twin = ax2.twinx()
ax2.plot(window_df['Date'], window_df['VIX'], color=C_ORANGE, linewidth=2, label='CBOE VIX')
ax2_twin.plot(window_df['Date'], window_df['USDIDR'], color=C_PURPLE, linewidth=1.8, linestyle='-.', label='USD/IDR')
ax2.set_ylabel('VIX Index', fontweight='bold', color=C_ORANGE)
ax2_twin.set_ylabel('USD / IDR', fontweight='bold', color=C_PURPLE)
ax2.set_title('B. Eskalasi Sentimen Risiko Global: Lonjakan Ekstrem VIX ke 38.57', fontweight='bold', loc='left')
ax2.axvline(d_under, color=C_BLUE, linestyle='--', linewidth=1.2, alpha=0.6)
ax2.axvline(d_crash, color=C_RED, linestyle='--', linewidth=1.2, alpha=0.6)

# Panel 3: Actual Target vs Predictions
ax3 = axes[2]
ax3.plot(window_df['Date'], window_df['Target_Volatilitas_Y'], color='black', linewidth=2.5, marker='o', markersize=4, label='Target Aktual Y (Forward 5d Vol)')
ax3.plot(window_df['Date'], window_df['p_blend60'], color=C_BLUE, linewidth=2, linestyle='-', marker='s', markersize=3.5, label='Prediksi Blend 60:40')
ax3.plot(window_df['Date'], window_df['p_gbr'], color=C_PURPLE, linewidth=1.5, linestyle=':', label='Prediksi GBR Tuned')
ax3.plot(window_df['Date'], window_df['rv_past5'], color=C_ORANGE, linewidth=1.5, linestyle='--', label='Baseline Naif (rv_past5)')

# Highlight gaps
ax3.axvline(d_under, color=C_BLUE, linestyle='--', linewidth=1.5, alpha=0.85)
ax3.axvline(d_crash, color=C_RED, linestyle='--', linewidth=1.5, alpha=0.85)

ax3.annotate(f"Underprediction Gap:\nAktual: 0.01925\nPred: 0.00583\nError: +0.01343", 
             xy=(d_under, 0.01925), xytext=(pd.to_datetime('2024-07-20'), 0.015),
             arrowprops=dict(facecolor=C_BLUE, shrink=0.08, width=1.5, headwidth=6),
             fontweight='bold', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor=C_BLUE))

ax3.annotate(f"Overprediction Gap:\nAktual: 0.00550\nPred: 0.01231\nError: -0.00681", 
             xy=(d_crash, 0.01231), xytext=(pd.to_datetime('2024-08-09'), 0.015),
             arrowprops=dict(facecolor=C_RED, shrink=0.08, width=1.5, headwidth=6),
             fontweight='bold', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor=C_RED))

ax3.set_ylabel('Realized Volatility', fontweight='bold')
ax3.set_xlabel('Tanggal Prediksi (t)', fontweight='bold')
ax3.set_title('C. Target Aktual vs Model Prediksi: Kegagalan Antisipasi Shok Forward & Over-Reaksi Pasca-Shok', fontweight='bold', loc='left')
ax3.legend(loc='upper right', frameon=True, fontsize=8.5)

ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.xticks(rotation=20)
plt.tight_layout()
fig_path1 = os.path.join(OUTPUT_DIR, 'fig_err_01_timeline_context.png')
plt.savefig(fig_path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"[OK] Saved Figure 1: {fig_path1}")

# =============================================================================
# HELPER FOR WATERFALL PLOTS
# =============================================================================
def plot_xai_waterfall(case_date, case_title, case_type, output_filename):
    idx = val_fold3[val_fold3['Date'] == case_date].index[0]
    row = val_fold3.loc[idx]
    y_true = row['Target_Volatilitas_Y']
    y_pred_b = p_blend60[idx]
    y_pred_g = p_gbr[idx]
    y_pred_r = p_ridge[idx]
    
    sh_b = blend60_shap[idx]
    sh_g = gbr_shap[idx]
    sh_r = ridge_shap[idx]
    
    df_contr = pd.DataFrame({
        'Feature': feature_cols,
        'Value': [row[c] for c in feature_cols],
        'SHAP_Blend60': sh_b,
        'SHAP_GBR': sh_g,
        'SHAP_Ridge': sh_r,
        'Abs_Blend60': np.abs(sh_b)
    }).sort_values('Abs_Blend60', ascending=False)
    
    # Take top 8 most influential features
    top8 = df_contr.head(8).sort_values('SHAP_Blend60', ascending=True)
    
    fig, (ax_bar, ax_decomp) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [1.3, 1]})
    
    # Left subplot: Horizontal Contribution Bar Chart for Blend 60:40
    y_positions = np.arange(len(top8))
    colors = [C_RED if v > 0 else C_BLUE for v in top8['SHAP_Blend60']]
    
    bars = ax_bar.barh(y_positions, top8['SHAP_Blend60'], color=colors, edgecolor='black', alpha=0.85, height=0.6)
    ax_bar.set_yticks(y_positions)
    labels = [f"{r['Feature']}\n(val: {r['Value']:.2f})" if abs(r['Value']) > 10 else f"{r['Feature']}\n(val: {r['Value']:.4f})" for _, r in top8.iterrows()]
    ax_bar.set_yticklabels(labels, fontsize=9)
    ax_bar.axvline(0, color='black', linewidth=1, linestyle='--')
    ax_bar.set_xlabel('Atribusi Nilai Prediksi Blend 60:40 (Delta dari Base Value)', fontweight='bold')
    ax_bar.set_title(f'A. Top Kontributor Fitur Blend 60:40\n[Base Value = {blend60_base:.6f} | Pred = {y_pred_b:.6f}]', fontweight='bold', loc='left')
    
    # Add value annotations
    for bar, val in zip(bars, top8['SHAP_Blend60']):
        offset = 0.00003 if val >= 0 else -0.00003
        ha = 'left' if val >= 0 else 'right'
        ax_bar.text(val + offset, bar.get_y() + bar.get_height()/2, f"{val:+.6f}", 
                    va='center', ha=ha, fontsize=8.5, fontweight='bold',
                    color=C_RED if val > 0 else C_BLUE)
        
    # Right subplot: Model Bridge & Error Decomposition
    # Visualizing: Base Value -> Sum SHAP -> Predicted -> Actual -> Residual Gap
    bridge_labels = [
        'Base Value\n(E[Y])',
        'Model Pred\n(Blend 60:40)',
        'Model Pred\n(GBR Tuned)',
        'Model Pred\n(Ridge Tuned)',
        'Baseline\n(rv_past5)',
        'Target Aktual\n(y_true)'
    ]
    bridge_vals = [
        blend60_base,
        y_pred_b,
        y_pred_g,
        y_pred_r,
        row['rv_past5'],
        y_true
    ]
    b_colors = [C_GRAY, C_BLUE, C_PURPLE, C_ORANGE, '#9CA3AF', C_DARK]
    
    x_b = np.arange(len(bridge_labels))
    b_bars = ax_decomp.bar(x_b, bridge_vals, color=b_colors, edgecolor='black', alpha=0.85, width=0.55)
    ax_decomp.set_xticks(x_b)
    ax_decomp.set_xticklabels(bridge_labels, fontsize=8.5, fontweight='bold')
    ax_decomp.set_ylabel('Realized Volatility', fontweight='bold')
    ax_decomp.set_title(f'B. Komparasi Prediksi vs Target Aktual & Error Gap\n[Tanggal: {case_date}]', fontweight='bold', loc='left')
    
    for bar, val in zip(b_bars, bridge_vals):
        ax_decomp.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0003, f"{val:.5f}", 
                       ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    # Draw arrow representing residual error
    err_val = y_true - y_pred_b
    ax_decomp.annotate(f"Residual Gap\n({err_val:+.5f})", 
                       xy=(1, y_pred_b), xytext=(1.5, (y_pred_b + y_true)/2),
                       arrowprops=dict(arrowstyle="<->", color=C_RED if err_val > 0 else C_BLUE, lw=2),
                       fontweight='bold', fontsize=9, ha='center',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='red' if err_val > 0 else 'blue'))
    
    plt.suptitle(f"{case_title} — Analisis Dekomposisi XAI ({case_date})", fontsize=12, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved Waterfall/Decomposition Figure: {output_filename}")

# =============================================================================
# FIGURE 2: WATERFALL UNDERPREDICTION (2024-07-31)
# =============================================================================
print("Generating Figure 2: Waterfall Underprediction (2024-07-31)...")
fig_path2 = os.path.join(OUTPUT_DIR, 'fig_err_02_waterfall_underprediction_20240731.png')
plot_xai_waterfall(
    case_date='2024-07-31',
    case_title='KASUS 1: UNDERPREDICTION EKSTREM (Pra-Black Monday)',
    case_type='under',
    output_filename=fig_path2
)

# =============================================================================
# FIGURE 3: WATERFALL OVERPREDICTION (2024-08-05)
# =============================================================================
print("Generating Figure 3: Waterfall Overprediction (2024-08-05)...")
fig_path3 = os.path.join(OUTPUT_DIR, 'fig_err_03_waterfall_overprediction_20240805.png')
plot_xai_waterfall(
    case_date='2024-08-05',
    case_title='KASUS 2: OVERPREDICTION EKSTREM (Puncak Crash Black Monday)',
    case_type='over',
    output_filename=fig_path3
)

# =============================================================================
# FIGURE 4: COMPARATIVE RESIDUAL & CONTRIBUTIONS BREAKDOWN
# =============================================================================
print("Generating Figure 4: Comparative Residual & Contributions Breakdown...")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

cases = ['2024-07-31', '2024-08-05']
case_names = ['Kasus 1: Underprediction\n(31 Juli 2024)', 'Kasus 2: Overprediction\n(5 Agustus 2024)']

# Panel A: Absolute Errors across Candidates
models = ['Baseline (rv_past5)', 'rv_past20', 'Ridge Tuned', 'GBR Tuned', 'Blend 60:40', 'Blend 50:30:20']
m_keys = ['rv_past5', 'rv_past20', 'p_ridge', 'p_gbr', 'p_blend60', 'p_blend50']

case1_row = val_fold3[val_fold3['Date'] == '2024-07-31'].iloc[0]
case2_row = val_fold3[val_fold3['Date'] == '2024-08-05'].iloc[0]

y_true1 = case1_row['Target_Volatilitas_Y']
y_true2 = case2_row['Target_Volatilitas_Y']

abs_err1 = [abs(y_true1 - case1_row[k]) for k in m_keys]
abs_err2 = [abs(y_true2 - case2_row[k]) for k in m_keys]

x = np.arange(len(models))
width = 0.35

rects1 = axes[0].bar(x - width/2, abs_err1, width, label='31 Jul 2024 (Underprediction)', color=C_BLUE, edgecolor='black', alpha=0.85)
rects2 = axes[0].bar(x + width/2, abs_err2, width, label='5 Agu 2024 (Overprediction)', color=C_RED, edgecolor='black', alpha=0.85)

axes[0].set_ylabel('Absolute Error |y - y_hat|', fontweight='bold')
axes[0].set_title('A. Perbandingan Absolute Error Model vs Baseline', fontweight='bold', loc='left')
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, rotation=25, ha='right', fontsize=8.5, fontweight='bold')
axes[0].legend(frameon=True)

for r in rects1:
    axes[0].text(r.get_x() + r.get_width()/2, r.get_height() + 0.0002, f"{r.get_height():.4f}", ha='center', va='bottom', fontsize=7.5)
for r in rects2:
    axes[0].text(r.get_x() + r.get_width()/2, r.get_height() + 0.0002, f"{r.get_height():.4f}", ha='center', va='bottom', fontsize=7.5)

# Panel B: Residuals with Direction (y_true - y_hat)
res1 = [y_true1 - case1_row[k] for k in m_keys]
res2 = [y_true2 - case2_row[k] for k in m_keys]

rects3 = axes[1].bar(x - width/2, res1, width, label='31 Jul (Positif = Underpredicted)', color=C_BLUE, edgecolor='black', alpha=0.85)
rects4 = axes[1].bar(x + width/2, res2, width, label='5 Agu (Negatif = Overpredicted)', color=C_RED, edgecolor='black', alpha=0.85)

axes[1].axhline(0, color='black', linewidth=1, linestyle='--')
axes[1].set_ylabel('Residual Error (y_true - y_hat)', fontweight='bold')
axes[1].set_title('B. Arah Residual Error: Asimetri Shok Tak Terduga vs Reversi Cepat', fontweight='bold', loc='left')
axes[1].set_xticks(x)
axes[1].set_xticklabels(models, rotation=25, ha='right', fontsize=8.5, fontweight='bold')
axes[1].legend(frameon=True)

for r in rects3:
    axes[1].text(r.get_x() + r.get_width()/2, r.get_height() + 0.0002, f"{r.get_height():+.4f}", ha='center', va='bottom', fontsize=7.5)
for r in rects4:
    axes[1].text(r.get_x() + r.get_width()/2, r.get_height() - 0.0008, f"{r.get_height():+.4f}", ha='center', va='top', fontsize=7.5)

plt.suptitle("Evaluasi Residual Error Model Kandidat pada Dua Kasus Ekstrem 2024", fontsize=12, fontweight='bold')
plt.tight_layout()
fig_path4 = os.path.join(OUTPUT_DIR, 'fig_err_04_comparative_model_residual_breakdown.png')
plt.savefig(fig_path4, dpi=150, bbox_inches='tight')
plt.close()
print(f"[OK] Saved Comparative Residual Figure: {fig_path4}")

print("\nAll 4 XAI Error Analysis figures generated successfully!")
