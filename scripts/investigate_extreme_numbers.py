import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = r'z:\Projects\Inception'
sys.path.insert(0, PROJECT_ROOT)

from scripts.feature_engineering import preprocess_usdidr, engineer_features
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

df_raw = pd.read_csv(os.path.join(PROJECT_ROOT, 'Aset Lomba', 'dataset peserta.csv'))
df_clean, _ = preprocess_usdidr(df_raw)
df_feat = engineer_features(df_clean, use_cleaned_usdidr=True)

feature_cols = [c for c in df_feat.columns if c not in ['Date', 'Target_Volatilitas_Y', 'USDIDR_raw']]
labeled_df = df_feat[df_feat['Target_Volatilitas_Y'].notna()].dropna(subset=feature_cols).copy().reset_index(drop=True)
labeled_df['Date'] = pd.to_datetime(labeled_df['Date'])

folds = [
    ('Fold 1 (2022)', '2021-12-31', '2022-01-01', '2022-12-31'),
    ('Fold 2 (2023)', '2022-12-31', '2023-01-01', '2023-12-31'),
    ('Fold 3 (2024)', '2023-12-31', '2024-01-01', '2024-12-17'),
]

PURGE_H = 5
oof_preds = []

for f_name, t_end, v_start, v_end in folds:
    train_sub = labeled_df[labeled_df['Date'] <= t_end].iloc[:-PURGE_H]
    val_sub = labeled_df[(labeled_df['Date'] >= v_start) & (labeled_df['Date'] <= v_end)].copy()
    
    gbr = GradientBoostingRegressor(loss='absolute_error', learning_rate=0.03, max_depth=2, n_estimators=100, min_samples_leaf=1, random_state=42)
    gbr.fit(train_sub[feature_cols].values, train_sub['Target_Volatilitas_Y'].values)
    
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(train_sub[feature_cols].values)
    X_v_s = scaler.transform(val_sub[feature_cols].values)
    ridge = Ridge(alpha=1000.0, random_state=42)
    ridge.fit(X_tr_s, train_sub['Target_Volatilitas_Y'].values)
    
    p_gbr = gbr.predict(val_sub[feature_cols].values)
    p_ridge = ridge.predict(X_v_s)
    p_b60 = 0.60 * p_gbr + 0.40 * p_ridge
    p_b50 = 0.50 * p_gbr + 0.30 * p_ridge + 0.20 * val_sub['rv_past20'].values
    
    val_sub['p_gbr'] = p_gbr
    val_sub['p_ridge'] = p_ridge
    val_sub['p_b60'] = p_b60
    val_sub['p_b50'] = p_b50
    oof_preds.append(val_sub)

all_oof = pd.concat(oof_preds, axis=0).reset_index(drop=True)

# Test top 5% threshold
q95 = all_oof['Target_Volatilitas_Y'].quantile(0.95)
top5 = all_oof[all_oof['Target_Volatilitas_Y'] >= q95]
print(f"Top 5% by target (threshold {q95:.6f}, N={len(top5)}):")
print(f"  GBR: {np.mean(np.abs(top5['Target_Volatilitas_Y'] - top5['p_gbr'])):.6f}")
print(f"  Ridge: {np.mean(np.abs(top5['Target_Volatilitas_Y'] - top5['p_ridge'])):.6f}")
print(f"  Blend 60:40: {np.mean(np.abs(top5['Target_Volatilitas_Y'] - top5['p_b60'])):.6f}")
print(f"  Blend 50:30:20: {np.mean(np.abs(top5['Target_Volatilitas_Y'] - top5['p_b50'])):.6f}")

# Where does 0.007584 or 0.007604 come from? Check different percentiles or train threshold
q95_tr = labeled_df[labeled_df['Date'] <= '2021-12-31']['Target_Volatilitas_Y'].quantile(0.95)
top5_tr = all_oof[all_oof['Target_Volatilitas_Y'] >= q95_tr]
print(f"Top by train threshold {q95_tr:.6f} (N={len(top5_tr)}):")
print(f"  Blend 60:40: {np.mean(np.abs(top5_tr['Target_Volatilitas_Y'] - top5_tr['p_b60'])):.6f}")
print(f"  Blend 50:30:20: {np.mean(np.abs(top5_tr['Target_Volatilitas_Y'] - top5_tr['p_b50'])):.6f}")
