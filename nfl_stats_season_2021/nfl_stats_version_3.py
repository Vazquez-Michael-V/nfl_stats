#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Pandas to get table data.
import pandas as pd

#Plotly and time imports for chart.
from plotly import offline
import time

PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
driver = webdriver.Chrome(service=serv)

#Navigate to the NFL website homepage.
WEBSITE = "https://www.nfl.com/"
driver.get(WEBSITE)
driver.maximize_window()
web_title = driver.title
print(web_title)

#Navigate to the stats page.
link_stats = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT,"Stats")))
link_stats.click()

time.sleep(5)

search_bar = driver.current_url
player_table = pd.read_html(search_bar)
df = pd.DataFrame(player_table[0])
print(df)

#Option to export to csv file.
filename = 'nfl_stats_version_3.csv'
df.to_csv(filename, encoding='utf-8',index=False)

print(f"Table pulled from '{search_bar}'.")

# header_row = list(df)
# print(header_row)

# View list indexes.
# for a, t in enumerate(list(df)):
#     print(f"col_{a} {t}")
    
quarterbacks = list(df['Player'])
#print(quarterbacks)
qb_top_5 = [quarterbacks[i] for i in range(0,10)]
print(qb_top_5)

pass_yards = list(df['Pass Yds'])
pass_yards_top_5 = [pass_yards[i] for i in range(0,10)]
print(pass_yards_top_5)

today = time.strftime("%m.%d.%y")
chart_title = f"Top Ten Quarterbacks by Yards as of {today}"

#Create the plot using Plotly.
data = [{
    'type': 'bar',
    'orientation': 'h',
    'x': pass_yards_top_5,
    'y': qb_top_5
    }]

layout = {
    'title': {'text': chart_title, 'x': 0.5, 'y': 0.9, 'xanchor':'center', 'yanchor': 'top'},
    'xaxis': {'title':'Yards'},
    'yaxis': {'title': 'QBs', 'autorange': 'reversed'}        
    }

fig = {'data': data, 'layout': layout}
offline.plot(fig, filename='qbs_yds_top_5.html')





















