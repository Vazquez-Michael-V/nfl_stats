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

#Option to export to csv file.
# filename = 'nfl_stats_version_2021.csv'
# df_2021.to_csv(filename, encoding='utf-8',index=False)

print(f"Table pulled from '{search_bar}'.")

all_stat_years = []
#Find the currently selected year.
stat_year = nfl.selected_stat_year(driver)
print(f"Stat year is {stat_year}.")
all_stat_years.append(stat_year)
#Assign the number of top players, ie top 10 players.
top_num = 10

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

#Ask user which year to plot.

print("Available stat years are:")
for y in all_stat_years:    
    print(y)
    
year_to_plot = input("Select a year to plot. ")
 
#Maybe create this dictionary in a for loop using a years list.
data_dict = {'2019':{'type': 'bar', 'orientation': 'h',
                     'x': pass_yards_tops_2019,
                     'y': qb_tops_2019
                     },
             '2021': {'type': 'bar', 'orientation': 'h',
                      'x': pass_yards_tops_2021,
                      'y': qb_tops_2021
                      }          
             }
try:     
    # Create the horizontal bar chart.
    nfl.barh_chart(data_dict, top_num, year_to_plot)

except KeyError:
    print(f"{year_to_plot} not an available stat year.")
    






