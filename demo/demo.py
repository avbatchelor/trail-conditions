'''
Functions used in the demo of my trail conditions project 

AVB 04/11/2018

'''


# coding: utf-8

# # Download and parse data from newenglandtrailconditions.com

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

#%% Make dataframe
def make_df(start_ind,end_ind):
    
    # Create empty dataframe 
    df = create_empty_df()
    
    # Fill datafram
    for test_id in range(start_ind,end_ind+1):
        result = get_html(test_id)
        result_list = html_to_df(result)
        df.loc[test_id] = result_list
    
    return df

#%% Function for cleaning peak column 
def clean_peaks(df):
    text_field = 'peaks'
    df[text_field] = df[text_field].str.replace(r"Mt. ", "")
    df[text_field] = df[text_field].str.replace(r"Mt ", "")
    df[text_field] = df[text_field].str.replace(r" Mountain", "")
    df[text_field] = df[text_field].str.replace(r"Mount ", "")
    # Remove state
    df[text_field] = df[text_field].str.replace("NH|ME|VT|MA|RI|CT", "")
    # Remove text in brackets 
    df[text_field] = df[text_field].str.replace("\(.+\)","")
    # Replace and with a comma
    df[text_field] = df[text_field].str.replace(" and ",",")
    # lowercase
    df[text_field] = df[text_field].str.lower()
    # Replace apostophes 
    df[text_field] = df[text_field].str.replace("\'", "")
    #Remove all irrelevant characters such as any non alphanumeric characters
    df[text_field] = df[text_field].str.replace("[^a-z\s\,]", " ")
    # Remove trailing commas
    df[text_field] = df[text_field].str.replace("\,(?!\s+\S)", "")
    # remove multiple whitespaces 
    df[text_field] = df[text_field].str.replace("\s+", " ")
    # Remove trailing whitespace 
    df[text_field] = df[text_field].str.replace("\s+(?!\S)", "")
    # Remove preceding whitespace 
    df[text_field] = df[text_field].str.replace("(?<!\S)\s+", "")
    return df

def apply_plot_settings():
    plt.xlabel('Month',fontsize=12)
    plt.ylabel('Probability of needing snowshoes',fontsize=12)
    plt.title('Probability of needing snowshoes for each month',fontsize=20)
    plt.legend('')
    fig = plt.gcf()
    fig.set_size_inches(10, 5, forward=True)
    plt.ylim((0,1))
    plt.tight_layout()
    


def prep_for_model(df):
    
    # Drop datetime column
    #df.drop(columns = ['datetime'],inplace=True)
    
    # Separate out snowshoes var 
    snowshoes = df.snowshoes.copy()
    
    # One hot encoding 
    dummy_df = df.copy()
    dummy_df.drop(columns='snowshoes',inplace=True)
    dummy_df["month"] = dummy_df["month"].astype('category')
    dummy_df = pd.get_dummies(dummy_df)
    
    # Split test and training data 
    # Code adpated from: https://blog.myyellowroad.com/using-categorical-data-in-machine-learning-with-python-from-dummy-variables-to-deep-category-66041f734512
    msk = np.random.rand(len(df)) < 0.8
    x_train = dummy_df[msk].iloc[:,:]
    x_test = dummy_df[~msk].iloc[:,:]
    y_train = snowshoes[msk]
    y_test = snowshoes[~msk]
    
    return x_train, x_test, y_train, y_test, msk

#%% Plot weights 
def plot_weights(l,x_test):
    weights = np.squeeze(l.coef_)
    weights = weights.tolist()
    weight_df = pd.DataFrame(weights,columns =['weight'])
    weight_df['input_var'] = list(x_test)
    weight_df.set_index('input_var',inplace=True)
    weight_df.sort_values(by=['weight'],inplace=True)
    weight_df.plot.bar()
    plt.xticks(rotation='vertical')
    fig = plt.gcf()
    fig.set_size_inches(20, 5, forward=True)
    plt.ylabel('weight')

#%% Convert probabilities to class
def get_class(y_pred):
    # Select probability and round
    if y_pred.ndim == 2:
        y_class = np.round(y_pred[:,1])
    else:
        y_class = np.round(y_pred)
    
    return y_class