from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

import pandas as pd

import plotly.graph_objs as go
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

def assign_colors(quarterbacks_2021, quarterbacks_2019, qbs_21_19, percent_change_21_19, year_to_plot, color_default, color_2021, color_2019):
    """Returns color dictionary for 2021 and 2019."""    
    # color_default = 'darkslategrey'
    # color_2021 = 'lightseagreen'
    # color_2019 = 'blue'
    
    colors_dict_2021 = {qb: color_default for qb in quarterbacks_2021}
    for qb in quarterbacks_2021:
        if qb in qbs_21_19:
            colors_dict_2021[qb]= color_2021  
            
    colors_dict_2019 = {qb: color_default for qb in quarterbacks_2019}
    for qb in quarterbacks_2019:
        if qb in qbs_21_19:
            colors_dict_2019[qb]= color_2019
    
    if year_to_plot == '2021':
        return colors_dict_2021
    elif year_to_plot == '2019':
        return colors_dict_2019
    elif year_to_plot == 'Compare 2021 to 2019':
        colors_21_19 = ['gold']*(len(qbs_21_19))
        return colors_21_19

def number_yaxis(y_axis_list):
    """Returns an enumerated a list."""
    y_num_list = []
    for n, y in enumerate(y_axis_list, 1):
        r = f"{n}. {y}"
        y_num_list.append(r)
    return y_num_list

def create_data_frame(quarterbacks_2021,pass_yards_2021, quarterbacks_2019, pass_yards_2019, qbs_21_19, percent_change_21_19, year_to_plot, color_default, color_2021, color_2019):
    """Create a DataFrame with columns qb, yards, bar color."""
    colors_dict = assign_colors(quarterbacks_2021, quarterbacks_2019, qbs_21_19, percent_change_21_19, year_to_plot, color_default, color_2021, color_2019)
    bar_color = []
    if year_to_plot == '2021':        
        for qb in quarterbacks_2021:
            bar_color.append(colors_dict[qb])
        dict_df = {'Players': number_yaxis(quarterbacks_2021), 'Yards': pass_yards_2021, 'Bar Color': bar_color}
        df_colors = pd.DataFrame(dict_df)    
            
    elif year_to_plot == '2019':        
        for qb in quarterbacks_2019:
            bar_color.append(colors_dict[qb])
        dict_df = {'Players': number_yaxis(quarterbacks_2019), 'Yards': pass_yards_2019, 'Bar Color': bar_color}
        df_colors = pd.DataFrame(dict_df)
            
    elif year_to_plot == 'Compare 2021 to 2019':        
        dict_df = {'Players': number_yaxis(qbs_21_19), 'Percent Change': percent_change_21_19}
        df_colors = pd.DataFrame(dict_df)
        df_colors['Bar Color']='gold'           

    df_colors['Year'] = year_to_plot
    print(df_colors)
    return df_colors


def barh_chart(df_colors, year_to_plot, color_default, color_2021, color_2019):
    """Takes the colors DataFrame and creates charts."""   
    
    fig = go.Figure()
    
    if year_to_plot == '2021':
        df_default = df_colors.loc[df_colors['Bar Color']==color_default]
        df_not_default = df_colors.loc[df_colors['Bar Color']==color_2021]
        print(df_default)
        print(df_not_default)
        
        fig.add_trace(go.Bar(
            x = list(df_not_default['Yards']),
            y = list(df_not_default['Players']),
            name = '2021 and 2019',
            orientation='h',
            marker_color = color_2021
            ))              
        
        fig.add_trace(go.Bar(
            x = list(df_default['Yards']),
            y = list(df_default['Players']),
            name = '2021',
            orientation='h',
            marker_color = color_default
            ))
        
        fig.update_yaxes(categoryorder='array', categoryarray = list(df_colors['Players']))   
    
        fig.update_yaxes(
            autorange='reversed'
                        )
        
        chart_title = f"Top QBs in {year_to_plot}"
        
    elif year_to_plot == '2019':
        df_default = df_colors.loc[df_colors['Bar Color']==color_default]
        df_not_default = df_colors.loc[df_colors['Bar Color']==color_2019]
        print(df_default)
        print(df_not_default)
        
        fig.add_trace(go.Bar(
            x = list(df_not_default['Yards']),
            y = list(df_not_default['Players']),
            name = '2021 and 2019',
            orientation='h',
            marker_color = color_2021
            ))              
        
        fig.add_trace(go.Bar(
            x = list(df_default['Yards']),
            y = list(df_default['Players']),
            name = '2019',
            orientation='h',
            marker_color = color_default
            ))
        
        fig.update_yaxes(categoryorder='array', categoryarray = list(df_colors['Players']))   
    
        fig.update_yaxes(
            autorange='reversed'
                        )
        
        chart_title = f"Top QBs in {year_to_plot}"
    
    elif year_to_plot == 'Compare 2021 to 2019':
        print(df_colors)
        fig.add_trace(go.Bar(
            x = list(df_colors['Percent Change']),
            y = list(df_colors['Players']),
            orientation='h',
            marker_color = 'gold'           
            ))
        
        fig.update_xaxes(
            tickformat='.2%'
            )       
    
        fig.update_yaxes(categoryorder='array', categoryarray = list(df_colors['Players']))   
    
        fig.update_yaxes(
            autorange='reversed'
                        )    
        chart_title = "Top QBs Percent Change in Yards from 2019 to 2021"
        
        
    fig.update_layout(
        title = {'text': chart_title, 'x': 0.5, 'y': 0.92, 'xanchor':'center', 'yanchor': 'top'},
        xaxis_title="Yards",
        yaxis_title="QBs"
        )
     
    offline.plot(fig, filename='qbs_yds_top_10.html')