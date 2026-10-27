import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = r'z:\Projects\Inception'
df_raw = pd.read_csv(os.path.join(PROJECT_ROOT, 'Aset Lomba', 'dataset peserta.csv'))
df_raw['Date'] = pd.to_datetime(df_raw['Date'])
df_raw = df_raw.sort_values('Date').reset_index(drop=True)

# Look at window around late July and August 2024
sub = df_raw[(df_raw['Date'] >= '2024-07-25') & (df_raw['Date'] <= '2024-08-16')].copy()
sub['IHSG_ret'] = sub['IHSG'].pct_change()
print(sub[['Date', 'IHSG', 'IHSG_ret', 'VIX', 'USDIDR', 'Target_Volatilitas_Y']].to_string(index=False))
