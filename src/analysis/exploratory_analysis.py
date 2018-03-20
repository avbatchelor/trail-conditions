# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 20:33:22 2018

@author: Alex
"""

#%% Import packages 
import pandas as pd 
import os
from nltk.tokenize import RegexpTokenizer
import os

#%% Read in large dataframe
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
reports = pd.read_pickle('cleaned_reports')

#%% Determine most popular peaks
all_words = [word for tokens in reports["peak_tokens"] for word in tokens]
VOCAB = sorted(list(set(all_words)))
print("%s words total, with a vocabulary size of %s" % (len(all_words), len(VOCAB)))

from collections import Counter
counts = Counter(all_words)
print(counts)

# Note: many of the unpopular peaks have names like blah - east peak.  I should consider removing the - east peak part during data cleaning for more accurate results.

##% Peaks with good views
import numpy as np
great_views = np.unique(reports['peaks'][reports.comments.str.contains('great view')>0])
