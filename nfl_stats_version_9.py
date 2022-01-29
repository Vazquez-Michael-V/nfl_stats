#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select

#Pandas and numpy for data tables.
import pandas as pd
import numpy as np

#Plotly and time imports for chart.
from plotly import offline
import time

import mods_nfl as nfl


PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
driver = webdriver.Chrome(service=serv)

#Navigate to the NFL website homepage.
WEBSITE = "https://www.nfl.com/"
driver.get(WEBSITE)
driver.maximize_window()
web_title = driver.title
print(web_title)

#Navigate to the stats page. Clear a dropdown if needed.
try:
    link_stats = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT,"Stats")))
    link_stats.click()

#Clear the slidedown.
except ElementClickInterceptedException:
    cancel_slidedownslidedown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onesignal-slidedown-cancel-button")))
    cancel_slidedownslidedown.click()
    link_stats = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT,"Stats")))
    link_stats.click()
    
time.sleep(5)

search_bar = driver.current_url
player_table = pd.read_html(search_bar)
df_2021 = pd.DataFrame(player_table[0])
print(df_2021)

print(f"Table pulled from '{search_bar}'.")

all_stat_years = []
#Find the currently selected year.
stat_year = nfl.selected_stat_year(driver)
print(f"Stat year is {stat_year}.")
all_stat_years.append(stat_year)
#Assign the number of top players, ie top 10 players.
top_num = 25

quarterbacks_2021 = list(df_2021['Player'])
#print(quarterbacks)
qb_tops_2021 = [quarterbacks_2021[i] for i in range(0,top_num)]
print(qb_tops_2021)

pass_yards_2021 = list(df_2021['Pass Yds'])
pass_yards_tops_2021 = [pass_yards_2021[i] for i in range(0, top_num)]
print(pass_yards_tops_2021)

#Click the dropdown menu.
main_content = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "main-content")))
drop_down = main_content.find_element(By.CLASS_NAME, "d3-o-dropdown")
drop_down.click()

option_tags = drop_down.find_elements(By.TAG_NAME, "option")

#Change the year to 2019.
nfl.year_to_click(option_tags, '2019')

#Find the currently selected year.
stat_year = nfl.selected_stat_year(driver)
print(f"Stat year is {stat_year}.")
all_stat_years.append(stat_year)

print("Printing 2019 data frame.")
search_bar = driver.current_url
player_table = pd.read_html(search_bar)
df_2019 = pd.DataFrame(player_table[0])
print(df_2019)

quarterbacks_2019 = list(df_2019['Player'])
#print(quarterbacks)
qb_tops_2019 = [quarterbacks_2019[i] for i in range(0,top_num)]
#print(qb_tops_2019)

pass_yards_2019 = list(df_2019['Pass Yds'])
pass_yards_tops_2019 = [pass_yards_2019[i] for i in range(0, top_num)]
#print(pass_yards_tops_2019)


#Want to find top qbs in 2021 and 2019.
df_21_merge_19 = df_2021.merge(df_2019, how="inner", on="Player")
all_stat_years.append('Compare 2021 to 2019')
df_21_merge_19 = df_21_merge_19.rename(columns={'Pass Yds_x': 'Pass Yds 2021', 'Pass Yds_y': 'Pass Yds 2019'})
#Create the plot lists for the merged DataFrame.
#(2021 yards - 2019 yards)/2019 yards
#df_21_merge_19['percent_change'] = ((df_21_merge_19['Pass Yds 2021'] - df_21_merge_19['Pass Yds 2019']) / df_21_merge_19['Pass Yds 2019'])*100
df_21_merge_19['percent_change'] = ((df_21_merge_19['Pass Yds 2021'] - df_21_merge_19['Pass Yds 2019']) / df_21_merge_19['Pass Yds 2019'])
merged_cols = df_21_merge_19.columns.tolist()
print(merged_cols)
print(len(merged_cols))

#Reorder the columns such that it is
# player, percent_change, Pass Yds 2021, Pass Yds 2019, then all other columns.

col1 = merged_cols[0:1] #Players column.
col2 = merged_cols[-1:] #percent_change column.
col3 = merged_cols[merged_cols.index('Pass Yds 2021') : merged_cols.index('Pass Yds 2021')+1]
col4 = merged_cols[merged_cols.index('Pass Yds 2019') : merged_cols.index('Pass Yds 2019')+1]

other_cols = []
for c in merged_cols:
    if c != 'Player' and c !='percent_change' and c !='Pass Yds 2021' and c!='Pass Yds 2019':
        other_cols.append(c)

reordered_cols = col1+col2+col3+col4+other_cols
print("Reorded cols")
print(len(reordered_cols))
df_21_merge_19 = df_21_merge_19[reordered_cols]

percent_change_21_19 = list(df_21_merge_19['percent_change'])
qbs_21_19 = list(df_21_merge_19['Player'])
print(qbs_21_19)

#Create excel files of the DataFrames.
filenames_dict = {'2021_merged_2019.xlsx':df_21_merge_19, 'df_2021.xlsx':df_2021,'df_2019.xlsx': df_2019}
for name, frame in filenames_dict.items():    
    with pd.ExcelWriter(name) as writer:       
        frame.to_excel(writer)

#Ask user which year to plot.
print("Available stat years are:")
for y in all_stat_years:    
    print(y)
year_to_plot = input("Select a year to plot. ")

df_colors = nfl.create_data_frame(quarterbacks_2021, pass_yards_2021, quarterbacks_2019, pass_yards_2019, qbs_21_19, percent_change_21_19, year_to_plot, 'darkslategrey', 'lightseagreen', 'blue')
print("")

nfl.barh_chart(df_colors, year_to_plot, 'darkslategrey', 'lightseagreen', 'blue')