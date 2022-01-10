from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from plotly import offline

def year_to_click(option_tags, year):
    """Function that takes a list and clicks on a year in that list.
       option_tags is a list of WebElements.
       year is a string.
       """
    for y in option_tags[:]: 
        f"Selecting year {y.text}"
        #print(y.text)    
        if y.text == year:        
            y.click()
            break
        
        
def selected_stat_year(driver):
    """Returns the currently selected drop down menu year."""
    drop_down_select = Select(driver.find_element(By.CLASS_NAME, "d3-o-dropdown"))
    stat_year = drop_down_select.first_selected_option
    #print(f"Stat year is {stat_year.text}.")
    return stat_year.text

def barh_chart(pass_yards_tops, qb_tops, top_num, stat_year):
    #today = time.strftime("%m.%d.%y")
    chart_title = f"Top {top_num} Quarterbacks by Yards in {stat_year}"
    #print(f"Selected year is {stat_year}.")

    data = [{
        'type': 'bar',
        'orientation': 'h',
        'x': pass_yards_tops,
        'y': qb_tops
        }]

    layout = {
        'title': {'text': chart_title, 'x': 0.5, 'y': 0.9, 'xanchor':'center', 'yanchor': 'top'},
        'xaxis': {'title':'Yards'},
        'yaxis': {'title': 'QBs', 'autorange': 'reversed'}        
        }

    fig = {'data': data, 'layout': layout}
    offline.plot(fig, filename='qbs_yds_top_5.html')