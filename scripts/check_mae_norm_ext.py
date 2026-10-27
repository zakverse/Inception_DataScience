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
    
    val_sub['p_gbr'] = p_gbr
    val_sub['p_ridge'] = p_ridge
    val_sub['p_rv20'] = val_sub['rv_past20'].values
    oof_preds.append(val_sub)

all_oof = pd.concat(oof_preds, axis=0).reset_index(drop=True)
y_all = all_oof['Target_Volatilitas_Y'].values

pct95 = np.percentile(y_all, 95)
norm_mask = y_all <= pct95
ext_mask = y_all > pct95

b_models = {
    'Blend 50:30:20': 0.50 * all_oof['p_gbr'] + 0.30 * all_oof['p_ridge'] + 0.20 * all_oof['p_rv20'],
    'Blend 40:60': 0.40 * all_oof['p_gbr'] + 0.60 * all_oof['p_ridge'],
    'Blend 50:50': 0.50 * all_oof['p_gbr'] + 0.50 * all_oof['p_ridge'],
    'Blend 60:40': 0.60 * all_oof['p_gbr'] + 0.40 * all_oof['p_ridge'],
    'Blend 70:30': 0.70 * all_oof['p_gbr'] + 0.30 * all_oof['p_ridge'],
    'GBR 100%': all_oof['p_gbr'],
    'Ridge 100%': all_oof['p_ridge'],
}

for name, p in b_models.items():
    m_norm = mean_absolute_error(y_all[norm_mask], p[norm_mask])
    m_ext = mean_absolute_error(y_all[ext_mask], p[ext_mask])
    print(f"{name:<15}: MAE Normal={m_norm:.6f} | MAE Ekstrem={m_ext:.6f}")
