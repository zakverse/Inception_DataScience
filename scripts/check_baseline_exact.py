import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = r'z:\Projects\Inception'
sys.path.insert(0, PROJECT_ROOT)

from scripts.feature_engineering import preprocess_usdidr, engineer_features

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

val_rows = []
for f_name, t_end, v_start, v_end in folds:
    sub = labeled_df[(labeled_df['Date'] >= v_start) & (labeled_df['Date'] <= v_end)].copy()
    val_rows.append(sub)

all_val = pd.concat(val_rows, axis=0).reset_index(drop=True)
print(f"Total OOF validation rows: {len(all_val)}")

for col in ['rv_past5', 'rv_past10', 'rv_past20']:
    mae = np.mean(np.abs(all_val['Target_Volatilitas_Y'] - all_val[col]))
    rmse = np.sqrt(np.mean((all_val['Target_Volatilitas_Y'] - all_val[col])**2))
    print(f"Pooled across all 772 rows for {col}: MAE = {mae:.6f} | RMSE = {rmse:.6f}")

for f_name, t_end, v_start, v_end in folds:
    sub = labeled_df[(labeled_df['Date'] >= v_start) & (labeled_df['Date'] <= v_end)].copy()
    mae_5 = np.mean(np.abs(sub['Target_Volatilitas_Y'] - sub['rv_past5']))
    rmse_5 = np.sqrt(np.mean((sub['Target_Volatilitas_Y'] - sub['rv_past5'])**2))
    mae_20 = np.mean(np.abs(sub['Target_Volatilitas_Y'] - sub['rv_past20']))
    rmse_20 = np.sqrt(np.mean((sub['Target_Volatilitas_Y'] - sub['rv_past20'])**2))
    print(f"{f_name} (N={len(sub)}): rv_past5 MAE={mae_5:.6f}, RMSE={rmse_5:.6f} | rv_past20 MAE={mae_20:.6f}, RMSE={rmse_20:.6f}")
