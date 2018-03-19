# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 09:51:50 2018

@author: Alex
"""

#%% 
def make_one_df(id):
    edited_column_names = ['entry_id','peaks', 'trails', 'date_of_hike', 'parking_access', 'surface_conditions', 'equipment', 'water_crossings', 'trail_maintenance', 'dogs', 'bugs', 'lost_and_found', 'comments', 'name', 'email', 'date_submitted', 'link']
    result = get_html(id)
    result_list = [id] + html_to_df(result)
    df = pd.DataFrame(np.column_stack(result_list),columns = edited_column_names)
    return df

#%% 
def make_whole_df(start_ind,end_ind):
    
    # Make clean log file
    import os
    try:
        os.remove("download_and_parse_log.text")
    except:
        print('No log file')
    fh = open("download_and_parse_log.text","a")
    
    # Create empty dataframe 
    df = create_empty_df()
    df_list = []
    
    # Fill datafram
    #try: 
    frames = [make_one_df(i) for i in range(start_ind, end_ind+1) ]
    big_df = pd.concat(frames)
    #except:
     #   fh.write("\n"+str(test_id))
         
    
    
    
    #df.set_index('entry_id',inplace=True)
            
    #df.loc[start_ind:end_ind] = df_list
                
    fh.close()
    
    return big_df

#%% Time alternative approach 
timeit.timeit('df = make_whole_df(1,2)', number=1, setup="from __main__ import make_whole_df")
