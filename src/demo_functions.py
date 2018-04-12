'''
Functions used in the demo of my trail conditions project 

AVB 04/11/2018

'''

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def html_to_df(table):

    # Code adapted from: http://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
    # 2018/02/10
    column_marker = 1
    result_list = []

    for row in table.find_all('tr'):

        # If the row contains 3 columns, add 1 to the number of rows 
        td_tags = row.find_all('td')
        if len(td_tags) == 3:
            text = td_tags[2].get_text()
            if text.find('Disclaimer') < 0:    
                result_list.append(td_tags[2].get_text())
                column_marker += 1

    return result_list

#%% Create empty data frame
def create_empty_df():

    edited_column_names = ['entry_id','peaks', 'trails', 'date_of_hike', 'parking_access', 'surface_conditions', 'equipment', 'water_crossings', 'trail_maintenance', 'dogs', 'bugs', 'lost_and_found', 'comments', 'name', 'email', 'date_submitted', 'link']
    df = pd.DataFrame(columns = edited_column_names)
    df.set_index('entry_id',inplace=True)
    return df

#%% 
def make_df(start_ind,end_ind):
    
    # Create empty dataframe 
    df = create_empty_df()
    
    # Fill dataframe
    result = get_html(test_id)
    result_list = html_to_df(result)
    df.loc[test_id] = result_list
    
    return df