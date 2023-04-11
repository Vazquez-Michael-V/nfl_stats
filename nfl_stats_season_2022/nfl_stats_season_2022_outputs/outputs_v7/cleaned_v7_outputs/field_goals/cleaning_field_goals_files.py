
# Clean and prep the combined field goals csvs output by nfl_stats_7.py
import pandas as pd
import numpy as np


dirty_files_input_path = r'C:\Users\plott\OneDrive\Desktop\python_work\nfl_stats_project\nfl_stats_project_2023\nfl_stats_outputs\nfl_player_stats_7_outputs\\'
field_goals_cleaned_output_path = r'C:\Users\plott\OneDrive\Desktop\python_work\nfl_stats_project\nfl_stats_project_2023\nfl_stats_outputs\nfl_player_stats_7_outputs\cleaned_v7_outputs\field_goals_outputs\\'

df_field_goals = pd.read_csv(f'{dirty_files_input_path}df_field_goals_2021_2022.csv')
df_field_goals.drop(columns=['Unnamed: 0', 'concat_index'], inplace=True)

# print(df_field_goals.info())
print(df_field_goals.shape)

# print(df_field_goals.head(10))

# print(df_field_goals['1-19 > A-M'].dtype)


# for col in df_field_goals.columns.to_list():
#     print(col)

# Create made / attempted columns.
# 1-19 > A-M --> DONE
# 20-29 > A-M
# 30-39 > A-M
# 40-49 > A-M
# 50-59 > A-M
# 60+ > A-M


made_attempt_cols = [col for col in df_field_goals.columns.to_list() if "> A-M" in col]
made_attempt_not_cols = [col for col in df_field_goals.columns.to_list() if not "> A-M" in col]
# print(made_attempt_cols)
# print(len(made_attempt_cols))

# print(made_attempt_not_cols)
# print(len(made_attempt_not_cols))



a_to_b_attmpt_made_list = []
for i in made_attempt_cols:
    if i[0] == '1':
        # print(i[0])
        a = i[0]
        # print(i[2:4])
        b = i[2:4]
        a_to_b_attmpt_made_list.append([f'{a}_to_{b}_made', f'{a}_to_{b}_attempted', f'{a}_to_{b}_ratio_made'])
    elif "+" in i:
        # print(i[0:3])
        b = i[0:3]
        a_to_b_attmpt_made_list.append([f'{b}_made', f'{b}_attempted', f'{b}_ratio_made'])
    else:
        # print(i[0:2])
        a = i[0:2]
        # print(i[3:5])
        b = i[3:5]
        a_to_b_attmpt_made_list.append([f'{a}_to_{b}_made', f'{a}_to_{b}_attempted', f'{a}_to_{b}_ratio_made'])

# 6 intervals, 3 columns for each interval --> 6*3 columns will be added to df_field_goals.
print(len(a_to_b_attmpt_made_list) * 3)

# I'm not typing this 6 times.
# df_field_goals[['1_to_19_attempted', '1_to_19_made']] = df_field_goals['1-19 > A-M'].str.split('/', expand=True).astype('int64')
# df_field_goals['1_to_19_ratio'] = (df_field_goals['1_to_19_made'] / df_field_goals['1_to_19_attempted']).fillna(0)

for og_cols, split_cols in zip(made_attempt_cols, a_to_b_attmpt_made_list):
    df_field_goals[split_cols[0:2]] = df_field_goals[og_cols].str.split('/', expand=True).astype('int64')
    # print(split_cols[0])
    # print(split_cols[1])
    # print(split_cols[2])
    df_field_goals[split_cols[2]] = df_field_goals[f'{split_cols[0]}'] / df_field_goals[f'{split_cols[1]}']

# Order the columns.
# print(a_to_b_attmpt_made_list[0])

unpacked_cols_list = []
for col_0 in a_to_b_attmpt_made_list:
    # print(col_0)
    for col_1 in col_0:
        # print(col_1)
        unpacked_cols_list.append(col_1)

# print(unpacked_cols_list)

# Not the most Pythony way to do it, but it works.
i = 0
for col in made_attempt_cols:
    unpacked_cols_list.insert(i, made_attempt_cols[made_attempt_cols.index(col)])
    i+=4

# print(unpacked_cols_list)
# print(len(unpacked_cols_list))

reorder_field_goals_cols_list = made_attempt_not_cols + unpacked_cols_list
df_field_goals = df_field_goals[reorder_field_goals_cols_list]

df_field_goals.fillna(0, inplace=True)

print(df_field_goals.shape)

# Start the yoy comparision process.
# DataFrame for 2022 and DataFrame for 2021.
df_fg_2022 = df_field_goals.loc[df_field_goals['season_year'] == 2022].copy()
print(df_fg_2022.shape)
df_fg_2021 = df_field_goals.loc[df_field_goals['season_year'] == 2021].copy()
print(df_fg_2021.shape)
df_fg_compare = pd.merge(df_fg_2022, df_fg_2021, how='inner', on=['Player'], suffixes=("_2022", "_2021"))
print(df_fg_compare.shape)


# TODO: Create yoy field goal columns. Use cleaning_passing_files.py as a reference.
with pd.ExcelWriter(f'{field_goals_cleaned_output_path}field_goals_2022_2021.xlsx') as writer:
    df_field_goals.to_excel(writer, sheet_name='field_goals')
    df_fg_compare.to_excel(writer, sheet_name='field_goals_compare')


