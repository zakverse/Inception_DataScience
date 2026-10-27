import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

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
    p_b40 = 0.40 * p_gbr + 0.60 * p_ridge
    p_b55 = 0.50 * p_gbr + 0.50 * p_ridge
    p_b70 = 0.70 * p_gbr + 0.30 * p_ridge
    
    val_sub['p_gbr'] = p_gbr
    val_sub['p_ridge'] = p_ridge
    val_sub['p_b60'] = p_b60
    val_sub['p_b50'] = p_b50
    val_sub['p_b40'] = p_b40
    val_sub['p_b55'] = p_b55
    val_sub['p_b70'] = p_b70
    oof_preds.append(val_sub)

all_oof = pd.concat(oof_preds, axis=0).reset_index(drop=True)
y_all = all_oof['Target_Volatilitas_Y'].values

# Check across various percentiles or subsets
for q in np.linspace(0.90, 0.98, 81):
    th = np.percentile(y_all, q*100)
    m = y_all > th
    mae_b60 = mean_absolute_error(y_all[m], all_oof['p_b60'][m])
    mae_b50 = mean_absolute_error(y_all[m], all_oof['p_b50'][m])
    if abs(mae_b60 - 0.007584) < 0.00005 or abs(mae_b50 - 0.007604) < 0.00005:
        print(f"Match found at q={q:.4f}, th={th:.6f}, N={np.sum(m)}: b60={mae_b60:.6f}, b50={mae_b50:.6f}")

# What about per fold top 5%?
mae_b60_folds = []
mae_b50_folds = []
for sub in oof_preds:
    y_sub = sub['Target_Volatilitas_Y'].values
    th_sub = np.percentile(y_sub, 95)
    m_sub = y_sub > th_sub
    mae_b60_folds.append(mean_absolute_error(y_sub[m_sub], sub['p_b60'][m_sub]))
    mae_b50_folds.append(mean_absolute_error(y_sub[m_sub], sub['p_b50'][m_sub]))
print(f"Mean across fold top 5%: b60={np.mean(mae_b60_folds):.6f}, b50={np.mean(mae_b50_folds):.6f}")

# What about quantile method with interpolation='nearest' or similar?
for method in ['linear', 'lower', 'higher', 'midpoint', 'nearest']:
    th_m = np.percentile(y_all, 95, method=method)
    m = y_all > th_m
    print(f"method={method}: th={th_m:.6f}, N={np.sum(m)}: b60={mean_absolute_error(y_all[m], all_oof['p_b60'][m]):.6f}")
