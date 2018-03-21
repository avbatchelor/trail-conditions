
# Predicting trail conditions

The following document is a summary of my trail conditions side project. 

## Contents 
* [Motivation & project goals](#id-section1)
* Summary of approach
* The data
* Scraping the data
* Cleaning the data using NLP 
* Exploratory analysis and visualizations 
* Key discoveries 
* What I learned 
* Future directions 
* [How to use this repository](#id-section2)

<div id='id-section1'/>
## Motivation & Project Goals 
Earlier this year, I started leading hikes in the White Mountains with the awesome MIT Outing Club.  Part of what I love about winter hiking is that you may encounter a wide variety of conditions on the trails.  You might find yourself walking in three feet of powdered snow or you might find the snow to be tightly packed-down by previous hikers. These conditions require different equipment.  In powdered snow, you'll need snowshoes to stop yourself from post-holing but snowshoes are unnecessary (and tiring) on a packed-down trail.   

#insert picture of post-holing vs. packed trail 

#![alt text](https://github.com/avbatchelor/trail-conditions/blob/master/images/trail_example.JPG)

# The data

## Sampling 

* Bad conditions may be under-sampled 
* People that use this website are certain subset of hikers, might have different hiking habits e.g. prefer quieter trails 



```python
# some test code
for i in range(1,5):
    print(i)
```

    1
    2
    3
    4
    

## Scraping the data

## Water crossings 
* Mention 

## Future directions
* Incorporating reports from other websites

<div id='id-section2'/>
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
