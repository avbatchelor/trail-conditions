# Predicting trail conditions

The following document is a summary of my trail conditions side project. 

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

## Motivation
Earlier this year, I started leading winter hikes in the White Mountains with the awesome MIT Outing Club.  While I was planning my hikes, I spent a lot of time on the internet trying to answer questions like these:

* Which hike should I go on?
	* Which hikes have good views?
	* Which hikes are suitably challenging?
* What will the trail conditions be?
	* Are water levels low enough to make river crossings doable? 
	* Is the snow packed down or do we need snow shoes?

* insert picture of post-holing vs. packed trail 

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/images/trail_example.JPG)

There's a lot of data out there to answer these questions, but that data isn't very organized.  So to get to an answer I'd need to look though lots of data from different sources.  To answer these questions, I might follow steps like these:

**Human algorithm 1: Which hikes have good views?**

	1. Find list of hikes 
	2. Randomly select a hike 
	3. Find description of that hike 
	4. See if the author mentions that there is a good view 

**Human algorithm 2: Are rivers passable?**

	1.  Find reports of trail conditions for the hike you want to go on. 
	2.  Check whether reports note any issues with river crossings? 
	2.  Check the weather forecast every day to see how much rain there has been between the last hike report and when you'll go on your hike. 
	3.  Check USGS data on river height to see if river height is low or high. 
	4.  Guess whether the river will be passable.

I decided to try and automate these algorithms so I could spend less time reading about hiking and more time hiking!
   
## Summary of approach

## The data

### Data sources

*Reports data*
 
There are multiple websites hosting reports of trail conditions.  I decided to use data from the website [newenglandtrailconditions.com](http://newenglandtrailconditions.com/).  I like this website because the reports are separated into sections such as: surface conditions, recommended equipment, and water crossing notes.  This website also contains a lot of data, there are over 30,000 reports from almost 10 years! Here's an example report from the site: 

![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/reports/figures/example_report.jpg)


*Water data*

 

### Sampling 

* Bad conditions may be under-sampled 
* People that use this website are certain subset of hikers, might have different hiking habits e.g. prefer quieter trails 



```python
some test code
for i in range(1,5):
    print(i)
```

    1
    2
    3
    4
    

### Scraping



## Which hikes have good views?

## Water crossings 
* Mention 

## What I learned 

*Coding*

* Scraping data with Requests
* Parsing HTML with Beautiful Soup
* 




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
