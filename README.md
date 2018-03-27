# Predicting trail conditions

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/view_from_pierce.JPG)
*Mt. Pierce has great views - but are the views from other peaks just as good?*

This is a summary of my side project.  The project is still a work in progress so please forgive me for parts that are incomplete - I'll be updating it throughout March and April 2018. 

## Table of Contents 
* [Motivation](#motivation)
* [Summary of approach](#summary-of-approach)
* [Results](#results)
* [My approach in more detail](#my-approach-in-more-detail)
	* [Data sources](#data-sources)
	* [Sampling](#sampling)
	* [Scraping](#scraping)
	* [Cleaning](#cleaning)
	* [Natural language processing?](#natural-language-processing)
	* [Classification](#classification)
* [What I learned](#what-i-learned)
* [Future directions](#future-directions) 
* [How to use this repository](#how-to-use-this-repository)
* [Project Organization](#project-organization)

## Motivation

Earlier this year I started leading winter hikes in the White Mountains and needed to answer these two questions:

>Which hike should I go on?
>What equipment do I need for that hike?  

I decided to start a side project so that I could gain quick answers to these questions without having to read many hike descriptions and check the weather every day.  

## Summary of approach

### Which hike should I go on?

For this part of the project, I decided to focus on determining which hikes have amazing views.  To do this, I scraped and cleaned data from online hike reports and used natural language processing techniques to parse the text data.  Specifically, I looked for instances adjectives like *amazing* or *wonderful* preceded the word *view*.  I now know which hikes have amazing views!

### What equipment do I need?

For this part of the project, I decided to focus on determining whether I'd need snowshoes for a hike.  For some hikes, snowshoes are absolutely necessary to prevent you sinking into the snow (commonly known as *postholing*).  But snowshoes are heavy, so it's good to avoid carrying them unnecessarily.  So it would be great to be able to accurately predict whether or not snowshoes are necessary for a hike.  

There are two situations where snowshoes are usually necessary:

1. For any hike after heavy snowfall 
2. For less-traveled hikes anytime in the winter - i.e. for hikes where there haven't been enough hikers to pack the snow down

And so, I plan to build a classifier with input variables such as *amount of recent snowfall* and *hike popularity* and outputs a probability for how likely it is that snowshoes are needed. 

So far, I’ve built some baseline classifiers that predict whether snowshoes are needed with reasonable accuracy.  Now I'm working on building the classifier described above to see if that is more accurate.  

## Results

### The top ten mountains for amazing views: 

1. Liberty
2. Pierce
3. Flume
4. Lafayette
5. Lincoln
6. Bondcliff
7. Washington
8. Bond
9. Bond West
10. Eisenhower

## My approach in more detail

### Data sources

*Reports data*
 
There are multiple websites hosting reports of trail conditions.  I decided to use data from the website [newenglandtrailconditions.com](http://newenglandtrailconditions.com/).  I like this website because the reports are separated into sections such as: surface conditions, recommended equipment, and water crossing notes.  This website also contains a lot of data, there are over 30,000 reports from almost 10 years! Here's an example report from the site: 

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/example_report.jpg)

 

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

### Cleaning 

### Natural language processing 

### Classification

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/prob_snowshoes_by_month.svg)

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/prob_snowshoes_by_peak.svg)

* Baseline 1: 0.636
* Baseline 2: 0.371
* Logistic regression: 0.368
* Random forest: 0.636

## What I learned 

*Big picture*

* You can learn a lot without doing any predictive modeling.
* Cleaning the text from free-form answers to questions is difficult - there are all kinds of idiosyncrasies that you have to deal with e.g. spelling mistakes, typos, people providing information with different levels of detail. 
* Write out what your model inputs and outputs will be before you even start cleaning data 
* It can be hard to beat a good baseline model

*Coding*

* Scraping data with Requests
* Parsing HTML with Beautiful Soup
* More fluent with pandas & regular expression




## Future directions
* Predicting whether river crossings are passable
* Incorporating reports from other websites


## How to use this repository
* I'll add info about how to run my code soon. 

## Project Organization

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
