import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = r'z:\Projects\Inception'
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.feature_engineering import preprocess_usdidr, engineer_features
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import shap

print("Loading raw dataset and engineering features...")
df_raw = pd.read_csv(os.path.join(PROJECT_ROOT, 'Aset Lomba', 'dataset peserta.csv'))
df_clean, _ = preprocess_usdidr(df_raw)
df_feat = engineer_features(df_clean, use_cleaned_usdidr=True)

feature_cols = [c for c in df_feat.columns if c not in ['Date', 'Target_Volatilitas_Y', 'USDIDR_raw']]
labeled_df = df_feat[df_feat['Target_Volatilitas_Y'].notna()].dropna(subset=feature_cols).copy().reset_index(drop=True)
labeled_df['Date'] = pd.to_datetime(labeled_df['Date'])

# Fold 3 setup
train_fold3 = labeled_df[labeled_df['Date'] <= '2023-12-31'].iloc[:-5].copy()
val_fold3 = labeled_df[(labeled_df['Date'] >= '2024-01-01') & (labeled_df['Date'] <= '2024-12-17')].copy().reset_index(drop=True)

print(f"Fold 3 Train rows: {len(train_fold3)} | Val rows: {len(val_fold3)}")

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

# TreeSHAP for GBR
explainer = shap.TreeExplainer(gbr)
gbr_shap = explainer.shap_values(X_v)
gbr_base = explainer.expected_value
if isinstance(gbr_base, np.ndarray):
    gbr_base = float(gbr_base[0])

# Verify GBR additive property
gbr_recon = gbr_shap.sum(axis=1) + gbr_base
assert np.max(np.abs(gbr_recon - p_gbr)) < 1e-10
print(f"GBR base value: {gbr_base:.6f}")

# Fit Ridge Tuned
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_v_s = scaler.transform(X_v)

ridge = Ridge(alpha=1000.0, random_state=42)
ridge.fit(X_tr_s, y_tr)
p_ridge = ridge.predict(X_v_s)

ridge_shap = X_v_s * ridge.coef_
ridge_base = float(ridge.intercept_)

# Verify Ridge additive property
ridge_recon = ridge_shap.sum(axis=1) + ridge_base
assert np.max(np.abs(ridge_recon - p_ridge)) < 1e-10
print(f"Ridge base value: {ridge_base:.6f}")

# Blend 60:40
p_blend60 = 0.60 * p_gbr + 0.40 * p_ridge
blend60_shap = 0.60 * gbr_shap + 0.40 * ridge_shap
blend60_base = 0.60 * gbr_base + 0.40 * ridge_base
assert np.max(np.abs((blend60_shap.sum(axis=1) + blend60_base) - p_blend60)) < 1e-10

# Blend 50:30:20
rv20_idx = feature_cols.index('rv_past20')
p_rv20 = val_fold3['rv_past20'].values
mu_rv20 = float(train_fold3['rv_past20'].mean())
p_blend50 = 0.50 * p_gbr + 0.30 * p_ridge + 0.20 * p_rv20
blend50_shap = 0.50 * gbr_shap + 0.30 * ridge_shap
blend50_shap[:, rv20_idx] += 0.20 * (p_rv20 - mu_rv20)
blend50_base = 0.50 * gbr_base + 0.30 * ridge_base + 0.20 * mu_rv20
assert np.max(np.abs((blend50_shap.sum(axis=1) + blend50_base) - p_blend50)) < 1e-10

# Inspect target dates
target_dates = ['2024-07-31', '2024-08-05']
for td in target_dates:
    idx = val_fold3[val_fold3['Date'] == td].index[0]
    row = val_fold3.loc[idx]
    y_true = row['Target_Volatilitas_Y']
    
    print("\n" + "="*80)
    print(f"CASE DATE: {td} (Index {idx} in Fold 3)")
    print(f"Target Actual y_true: {y_true:.6f}")
    print(f"Predictions:")
    print(f"  GBR Tuned     : {p_gbr[idx]:.6f} | Residual: {y_true - p_gbr[idx]:+.6f} | AbsErr: {abs(y_true - p_gbr[idx]):.6f}")
    print(f"  Ridge Tuned   : {p_ridge[idx]:.6f} | Residual: {y_true - p_ridge[idx]:+.6f} | AbsErr: {abs(y_true - p_ridge[idx]):.6f}")
    print(f"  Blend 60:40   : {p_blend60[idx]:.6f} | Residual: {y_true - p_blend60[idx]:+.6f} | AbsErr: {abs(y_true - p_blend60[idx]):.6f}")
    print(f"  Blend 50:30:20: {p_blend50[idx]:.6f} | Residual: {y_true - p_blend50[idx]:+.6f} | AbsErr: {abs(y_true - p_blend50[idx]):.6f}")
    print(f"  rv_past20     : {p_rv20[idx]:.6f} | Residual: {y_true - p_rv20[idx]:+.6f} | AbsErr: {abs(y_true - p_rv20[idx]):.6f}")
    print(f"  rv_past5      : {row['rv_past5']:.6f} | Residual: {y_true - row['rv_past5']:+.6f} | AbsErr: {abs(y_true - row['rv_past5']):.6f}")
    
    print("\nKey Market Features at EOD:")
    print(f"  IHSG: {row['IHSG']:.2f} | ret: {row['IHSG_ret']:.4f} | mom5: {row['mom_ihsg_5']:.4f} | mom10: {row['mom_ihsg_10']:.4f}")
    print(f"  VIX: {row['VIX']:.2f} | vix_ratio_ma20: {row['vix_ratio_ma20']:.4f}")
    print(f"  USDIDR: {row['USDIDR']:.2f} | US_rate: {row['US_rate']:.2f}% | BI_rate: {row['BI_rate']:.2f}%")
    print(f"  rv_past5: {row['rv_past5']:.6f} | rv_past10: {row['rv_past10']:.6f} | rv_past20: {row['rv_past20']:.6f}")
    print(f"  X1_Fear_Robust: {row['X1_Fear_Liquidity_Robust']:.4f} | X2_Rate_Diff: {row['X2_Rate_Diff_Pressure_Abs']:.4f}")
    
    # SHAP decomposition for Blend 60:40
    df_shap_b = pd.DataFrame({
        'Feature': feature_cols,
        'Value': [row[c] for c in feature_cols],
        'SHAP_GBR': gbr_shap[idx],
        'SHAP_Ridge': ridge_shap[idx],
        'SHAP_Blend60': blend60_shap[idx],
        'Abs_Blend60': np.abs(blend60_shap[idx])
    }).sort_values('SHAP_Blend60', ascending=False)
    
    print(f"\nTop 5 Pushing UP Features (Blend 60:40, Base={blend60_base:.6f}):")
    for _, sr in df_shap_b.head(5).iterrows():
        print(f"  + {sr['Feature']:<25}: {sr['SHAP_Blend60']:+.6f} (val: {sr['Value']:.4f}, GBR: {sr['SHAP_GBR']:+.6f}, Ridge: {sr['SHAP_Ridge']:+.6f})")
        
    print(f"\nTop 5 Pushing DOWN Features (Blend 60:40):")
    for _, sr in df_shap_b.tail(5)[::-1].iterrows():
        print(f"  - {sr['Feature']:<25}: {sr['SHAP_Blend60']:+.6f} (val: {sr['Value']:.4f}, GBR: {sr['SHAP_GBR']:+.6f}, Ridge: {sr['SHAP_Ridge']:+.6f})")
