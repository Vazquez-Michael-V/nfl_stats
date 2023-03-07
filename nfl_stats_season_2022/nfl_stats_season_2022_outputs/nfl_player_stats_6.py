#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

#Pandas and numpy for data tables.
import pandas as pd
import numpy as np

# Date and time imports.
import time
from datetime import datetime
import pytz

import json


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
chrome_options.add_argument('--incognito')


PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
driver = webdriver.Chrome(service=serv, options=chrome_options)

WEBSITE = "https://www.nfl.com/stats/player-stats/"
driver.get(WEBSITE)
driver.maximize_window()
web_title = driver.title
print(WEBSITE)
print(web_title)

time.sleep(2)
print(driver.current_url)

def dropdown_year(driver, year):
    """Select the year from the NFL stats dropdown menu."""
    ### Start of dropdown_year(driver, year) function.
    # TODO: Year selection needs to be done before the table scraping.
    # NFL stats website defaults to the current year.
    year_dropdown = driver.find_element(By.CLASS_NAME, 'd3-o-dropdown')
    select_obj_years = Select(year_dropdown)
    selected_year_list = select_obj_years.all_selected_options
    print(selected_year_list)
    print(type(selected_year_list))
    for y in selected_year_list:
        print(y.text)
    
    default_selected_year = selected_year_list[0]
    if default_selected_year != year:
        year_dropdown.click()
        select_obj_years.select_by_visible_text(str(year))
    else:
        pass
    # select_options_years_list = select_obj_years.options
    # print(type(select_options_years_list))
    # for sy in select_options_years_list:
    #     print(sy.text)
    
    return None
    ### End of dropdown_year function.


def get_stats_dict(driver, year):
    ### Start of get_stats_dict(driver) function.
    # TODO: Need to add keys for the year. ie 2022 DataFrame and 2021 DataFrame.
    # TODO: Find the selected year again and add it to the dictionary.
    # Obtain the urls for stats categories.
    stats_categories = driver.find_element(By.CLASS_NAME, 'nfl-o-tabs-bar__stage')
    print(stats_categories.text)
    print(type(stats_categories))
    
    # {passing: {'dataframe': df, 'url': url}}        
    stats_dict = {}
    year = str(year)
    stats_dict[year] = {}
    print("\nFinding categories links.")
    stats_categories_li = stats_categories.find_elements(By.TAG_NAME, 'li')
    for li_class in stats_categories_li:
        key = li_class.text
        print(key)
        li_class_a = li_class.find_element(By.TAG_NAME, 'a')
        li_class_url_str = li_class_a.get_attribute('href')
        value = li_class_url_str
        print(value)
        stats_dict[year][key] = {}
        stats_dict[year][key]['dataframe'] = None
        stats_dict[year][key]['url'] = value
    
    
    for k,v in stats_dict.items():
        print(k)
        print(f'\t{v}\n')


    return stats_dict
    ### End of get_stats_dict function.


def scrape_nfl_tables(driver, stats_dict_year, year):
    ### Start of scrape_nfl_tables(driver, stats_dict) function. 
    # Loop over the categories, Passing Rushing, ..., Punt Returns.
    # On each page, need to:
        # 1. Scrape the stats table.
        # 2. Check for next page button.
    year = str(year)
    for category in list(stats_dict_year[year].keys()):
        print(f'Scraping {category} data...')
        print(stats_dict_year[year][category]['url'])
        category_tables_list = []
        driver.get(stats_dict_year[year][category]['url'])
        # Give the page 10 seconds to load.
        # TODO: Use EC waits to be sure the page loads.
        # time.sleep(10)
        # Replace a static sleep time with a web element check.
        # This should wait at <= 10 seconds, which should reduce script run time, compared to a set sleep time of 10 seconds.
        print("Searching for table on page...")
        # No error handling here. If the script fails here then the rest of the script makes no sense, so let this TimeoutException stop the script.
        # There is only one table per page on these NFL stats urls.
        table_on_page_1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, 'table'))
            )
        print("Table found on page.")
        
        while True:
            # Scrape the stats table on the current page.
            table_on_page_list = pd.read_html(driver.current_url)
            category_tables_list.append(table_on_page_list[0])
            print(table_on_page_list[0].shape)
            try:
                # next_page_button_class = driver.find_element(By.CLASS_NAME, 'nfl-o-table-pagination__buttons')
                next_page_button_class = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'nfl-o-table-pagination__buttons'))
                    )
                print("Clicking next page button.")
                next_page_button_class.click()
                # time.sleep(10)
                # TODO: Changing set sleep time of 10 seconds to a web element check of <= 10 seconds.
            # except NoSuchElementException:
            # WebDriverWait will return a TimeoutException, not a NoSuchElementException.
            except TimeoutException:
                print(f'Timed out searching for next page button. No more {category} pages found here.')
                break
        # Concat the DataFrames for this category in the loop.
        df_category_temp = pd.concat(category_tables_list)
        stats_dict_year[year][category]['dataframe'] = [df_category_temp]   
        time.sleep(5)
    print("Scrape completed.")
    
    return stats_dict_year
    ### End of scrape_nfl_tables function.


def create_nfl_csvs(updated_stats_dict_year, year):
    ### Start of create_nfl_csvs(stats_dict) function.
    year = str(year)
    timezone_est = pytz.timezone('EST')
    scrape_completed_datetime = datetime.now(timezone_est).strftime('%Y%m%d')
    # Notice that not all categories have the same number of columns. --> Will need seperate file for each category.
    for category in list(updated_stats_dict_year[year].keys()):
        category_under_scores = category.replace(" ", "_")
        print(f'Writing csv for category {category}.')
        df_category = updated_stats_dict_year[year][category]['dataframe'][0]
        # Questionably lengthly filename.
        df_category.to_csv(f'df_{category_under_scores.lower()}_nfl_season_{year}_as_of_{scrape_completed_datetime}.csv')
    ### End of create_nfl_csvs(stats_dict) function.


# Set the dropdown menu to year 2021.
dropdown_year(driver, 2021)
# Obtain a dictionary to hold 2021 data.
stats_dict_2021 = get_stats_dict(driver, 2021)
print(stats_dict_2021)
# Scrape the tables and update the input dictionary.
updated_stats_dict_2021 = scrape_nfl_tables(driver, stats_dict_2021, 2021)
create_nfl_csvs(updated_stats_dict_2021, 2021)
# print(list(stats_dict.keys()))
# print(stats_dict['Punting']['url'])
# print(stats_dict_2021['2021'].keys())

time.sleep(10)

# Set the dropdown menu to year 2022.
dropdown_year(driver, 2022)
# Obtain a dictionary to hold 2022 data.
stats_dict_2022 = get_stats_dict(driver, 2022)
print(stats_dict_2022)
# Scrape the tables and update the input dictionary.
updated_stats_dict_2022 = scrape_nfl_tables(driver, stats_dict_2022, 2022)
create_nfl_csvs(updated_stats_dict_2022, 2022)

# TODO: Maybe need to merge 2021 and 2022 dictionaries?



# df_passing = pd.concat(passing_tables_list)
# df_passing.reset_index(inplace=True, drop=False, names='concat_index')
# df_passing.dropna(inplace=True, subset=['Player'])
# print(df_passing.head())
# print(df_passing.shape)

