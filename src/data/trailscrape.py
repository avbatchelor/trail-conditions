
# coding: utf-8

# # Download and parse data from newenglandtrailconditions.com

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#%% Download data 
def get_html(id):
    # Request webpage
    url = "http://www.newenglandtrailconditions.com/nh/viewreport.php?entryid=" + str(id)
    result = requests.get(url)

    # Check that it was received 
    if result.status_code == 200:
        return result
    else:
        print('Page ' + str(id) + ' not downloaded.')

#%% Parse html to list 
def html_to_df(result):

    # Parse html 
    soup = BeautifulSoup(result.text, 'html.parser')

    # Select the table containing hike report 
    table = soup.find_all('table')[2] 

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
    
    # Make clean log file
    import os
    os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\trail-conditions\\logs')
    try:
        os.remove("download_and_parse_log.text")
    except:
        print('No log file')
    fh = open("download_and_parse_log.text","a")
    
    # Create empty dataframe 
    df = create_empty_df()
    
    # Fill datafram
    for test_id in range(start_ind,end_ind+1):
        try: 
            result = get_html(test_id)
            result_list = html_to_df(result)
            df.loc[test_id] = result_list
        except:
            fh.write("\n"+str(test_id))

    fh.close()
    
    return df
