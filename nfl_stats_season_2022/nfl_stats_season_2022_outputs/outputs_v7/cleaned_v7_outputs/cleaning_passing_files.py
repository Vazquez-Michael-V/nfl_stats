
# Clean and prep the combined csvs output by nfl_stats_7.py
import pandas as pd
import numpy as np


dirty_files_input_path = r'some_directory'
cleaned_files_output_path = r'some_directory'

# All 11 categories have different columns. Will have to clean one at a time.
df_passing = pd.read_csv(f'{dirty_files_input_path}df_passing_2021_2022.csv',
                         # Only interested in passing yards, touchdowns, and interceptions.
                         usecols=['Player', 'Pass Yds', 'TD', 'INT', 'season_year'])

# Clean up the passing column names.
passing_og_col_names = df_passing.columns.to_list()
passing_col_renames = [col_name.lower().replace(" ", "_") for col_name in passing_og_col_names]
passing_col_rename_dict = {k:v for k,v in zip(passing_og_col_names, passing_col_renames)}
df_passing.rename(columns=passing_col_rename_dict, inplace=True)

print(df_passing.dtypes)
print(df_passing.head(5))
print(df_passing.shape)

# TODO: Some things to do:
# 1. Get new df to summarize 2021 passing.
# 2. Get new df to summarize 2022 passing.
# 3. Inner join on player column.
# 4. Create yoy column.
# 5. Create yoy_% column.
# 6. Create a td to interceptions column.

# .copy() to avoid SettingWithCopyWarning.
df_passing_2021 = df_passing.loc[df_passing['season_year'] == 2021].copy()
print(df_passing_2021.shape)
# Rename the 2021 passing columns, suffix '_2021', except if the column name is 'player'.
og_passing_2021_cols = df_passing_2021.columns.to_list()
passing_2021_cols_rename = [f'{col_name}_2021' if col_name != 'player' else 'player' for col_name in og_passing_2021_cols ]
passing_2021_rename_dict = {k:v for k,v in zip(og_passing_2021_cols, passing_2021_cols_rename)}
df_passing_2021.rename(columns=passing_2021_rename_dict, inplace=True)
print(df_passing_2021['season_year_2021'].unique())
# Drop rows with no player name.
df_passing_2021.dropna(subset=['player'], inplace=True)
print(df_passing_2021.shape)


# .copy() to avoid SettingWithCopyWarning.
df_passing_2022 = df_passing.loc[df_passing['season_year'] == 2022].copy()
print(df_passing_2022.shape)
# Rename the 2022 passing columns, suffix '_2022', except if the column name is 'player'.
og_passing_2022_cols = df_passing_2022.columns.to_list()
passing_2022_cols_rename = [f'{col_name}_2022' if col_name != 'player' else 'player' for col_name in og_passing_2022_cols]
passing_2022_rename_dict = {k:v for k,v in zip(og_passing_2022_cols, passing_2022_cols_rename)}
df_passing_2022.rename(columns=passing_2022_rename_dict, inplace=True)
print(df_passing_2022['season_year_2022'].unique())
# Drop rows with no player name.
df_passing_2022.dropna(subset=['player'], inplace=True)
print(df_passing_2022.shape)


# print(df_passing.shape)
# print(df_passing_2021.shape[0] + df_passing_2022.shape[0])

# Don't include the season_year column.
df_passing_compare = pd.merge(df_passing_2021[['player', 'pass_yds_2021', 'td_2021', 'int_2021']],                              
                              df_passing_2022[['player', 'pass_yds_2022', 'td_2022', 'int_2022']],
                              how='inner',
                              on=['player'])

# Create the yoy columns.
df_passing_compare['pass_yds_yoy'] = df_passing_compare['pass_yds_2022'] - df_passing_compare['pass_yds_2021']
df_passing_compare['td_yoy'] = df_passing_compare['td_2022'] - df_passing_compare['td_2021']
df_passing_compare['int_yoy'] = df_passing_compare['int_2022'] - df_passing_compare['int_2021']

# Create increase and decrease evaluation columns for passing yards, touchdowns, and interceptions.
pass_yds_condlist = [df_passing_compare['pass_yds_yoy'] > 0,
                     df_passing_compare['pass_yds_yoy'] < 0]
pass_yds_choicelist = ['increase', 'decrease']
df_passing_compare['pass_yds_yoy_eval'] = np.select(pass_yds_condlist, pass_yds_choicelist, 'no change')


td_condlist = [df_passing_compare['td_yoy'] > 0,
               df_passing_compare['td_yoy'] < 0]
td_choicelist = ['increase', 'decrease']
df_passing_compare['td_yoy_eval'] = np.select(td_condlist, td_choicelist, 'no change')


int_condlist = [df_passing_compare['int_yoy'] > 0,
                df_passing_compare['int_yoy'] < 0]
int_choicelist = ['increase', 'decrease']
df_passing_compare['int_yoy_eval'] = np.select(int_condlist, int_choicelist, 'no change')


# Create the yoy_pct_change columns.
df_passing_compare['pass_yds_yoy_pct_change'] = df_passing_compare['pass_yds_yoy'] / df_passing_compare['pass_yds_2021']
df_passing_compare['td_yoy_pct_change'] = df_passing_compare['td_yoy'] / df_passing_compare['td_2021']
df_passing_compare['int_yoy_pct_change'] = df_passing_compare['int_yoy'] / df_passing_compare['int_2021']

# Create td int ratio columns.
df_passing_compare['td_int_ratio_2021'] = df_passing_compare['td_2021'] / df_passing_compare['int_2021']
df_passing_compare['td_int_ratio_2022'] = df_passing_compare['td_2022'] / df_passing_compare['int_2022']
df_passing_compare['td_int_ratio_yoy'] = df_passing_compare['td_int_ratio_2022'] - df_passing_compare['td_int_ratio_2021']
df_passing_compare['td_int_ratio_yoy_pct_change'] = df_passing_compare['td_int_ratio_yoy'] / df_passing_compare['td_int_ratio_2021']


# Replace infintity values with 0.
df_passing_compare.replace([np.inf, -np.inf], np.nan, inplace=True)
df_passing_compare.fillna(0, inplace=True)

print(df_passing_compare.shape)
print(df_passing_compare.dtypes)

with pd.ExcelWriter(f'{cleaned_files_output_path}df_passing_compare.xlsx') as writer:
    df_passing_compare.to_excel(writer, sheet_name='passing_stats_compare', index=False)





