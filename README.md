# Predicting trail conditions

This is a summary of my side project.  The project is still a work in progress so please forgive me for parts that are incomplete - I'll be updating it throughout March and April 2018. 

## Table of Contents 
* [Motivation](#motivation)
* [Summary of approach](#summary-of-approach)
* [The data](#the-data)
	* [Sampling](#sampling)
	* [Scraping](#scraping)
	* [Cleaning](#cleaning)
* [Which hikes have good views?](#which-hikes-have-good-views)
* [Which rivers are passable?]()
	* [Word embeddings]()
	* [Logistic regression]()
* [What I learned](#what-i-learned)
* [Future directions](#future-directions) 
* [How to use this repository](#how-to-use-this-repository)
* [Project Organization](#project-organization)

## Motivation

Earlier this year I started leading winter hikes in the White Mountains and needed to answer these two questions:

>Which hike should I go on?
>And what equipment do I need for that hike?  

I decided to start a side project so that I could gain quick answers to these questions without having to read many hike descriptions and check the weather every day.  

## Summary of approach

*Which hike should I go on?* 

For this part of the project I decided to focus on determining which hikes have amazing views.  To do this, I scraped and cleaned data from online hike reports and used natural language processing techniques to parse the text data.  Specifically, I looked for instances where the word *view* was followed adjectives like *amazing* or *wonderful*.  I now know which hikes have amazing views!

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/view_from_pierce.JPG)
*I know Mt. Pierce has great views - but are the views from other peaks just as good?*

*What equipment do I need?* 

The next challenge is to determine what equipment I need.  For example, in the winter, especially if it has snowed recently, I’m likely to need snowshoes.  So far, I’ve fit a logistic regression model that takes the month of the year and the trail name (one-hot-encoded) as inputs and predicts whether snowshoes are needed with reasonable accuracy.  Next, I plan to improve the classifier by incorporating weather data.  

## Results



## My approach in more detail

### Data sources

*Reports data*
 
There are multiple websites hosting reports of trail conditions.  I decided to use data from the website [newenglandtrailconditions.com](http://newenglandtrailconditions.com/).  I like this website because the reports are separated into sections such as: surface conditions, recommended equipment, and water crossing notes.  This website also contains a lot of data, there are over 30,000 reports from almost 10 years! Here's an example report from the site: 

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/example_report.jpg)


*Water data*

 

### Sampling 

* Selection of 4000 footers 
* Bad conditions may be under-sampled 
* People that use this website are certain subset of hikers, might have different hiking habits e.g. prefer quieter trails 




    

### Scraping

Scraping data and parsing html turns out to be pretty easy when using request and beautiful soup.  Here's a simplified example of the code I used to scrape and parse trail reports: 

```python
import requests
from bs4 import BeautifulSoup

id = 1
url = "http://www.newenglandtrailconditions.com/nh/viewreport.php?entryid=" + str(id)
result = requests.get(url)

# Parse html 
soup = BeautifulSoup(result.text, 'html.parser')

# Select the table containing hike report 
table = soup.find_all('table')[2] 

```
Fortunately, the urls for the trail reports only differ by an id number  at the end of the url that increments by 1 for each new report.  So I was able to loop through the urls to get each report.  

Once I got the table, I had to loop through the html tags for rows and columns to extract the data I needed. 

## Which hikes have good views?

Which hikes have good views?**

	1. Find list of hikes 
	2. Randomly select a hike 
	3. Find description of that hike 
	4. See if the author mentions that there is a good view 

## Snowshoes

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/prob_snowshoes_by_peak.png)

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/prob_snowshoes_by_peak.svg)

* Baseline 1: 0.636
* Baseline 2: 0.371
* Logistic regression: 0.368
* Random forest: 0.636

## What I learned 

*Big picture*

* You can learn a lot without doing any predictive modeling.
* Cleaning the text from free-form answers to questions is difficult - there are all kinds of idiosyncrasies that you have to deal with e.g. spelling mistakes, typos, different levels of detail. 
* Write out what your model inputs and outputs will be before you even start cleaning data 
* It can be hard to beat a good baseline model

*Coding*

* Scraping data with Requests
* Parsing HTML with Beautiful Soup
* More fluent with pandas 




## Future directions
* Incorporating reports from other websites


## How to use this repository

## Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project organization based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
