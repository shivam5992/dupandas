# **dupandas:** data deduplication of text records in a pandas dataframe


[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](https://github.com/shivam5992/dupandas) [![Twitter Follow](https://img.shields.io/twitter/follow/shields_io.svg?style=social&label=Follow&maxAge=2592000)](https://twitter.com/shivamshaz)

dupandas is a python package to perform data deduplication on columns of a pandas dataframe using flexible text matching. It is compatible with both versions of python (2.x and 3.x). dupandas can find duplicate any kinds of text records in the pandas data. It comprises of sophisticated Matchers that can handle spelling differences and phonetics. It also comprises of several Cleaners, which can be used to clean up the noise present in the text data such as punctuations, digits, casing etc.

The good part of dupandas is that it's Matchers and Cleaner functions can be used as standalone packages while working with different problems of text data.


## Installation
Following python modules are required to use dupandas: **pandas, fuzzy, python-levenshtein** . These modules can be installed using pip command:

```python
    pip install dupandas pandas fuzzy python-levenshtein
```
**OR** if dependencies are already installed:

```
    pip install dupandas
```
    
## Usage : dupandas
dupandas using default Matchers and Cleaners, Default Matcher and Cleaners are Exact Match and No Cleaning respectively.

``` python
    from dupandas import Dedupe
    dupe = Dedupe()
    
    input_config = {
        'input_data' : pandas_dataframe,
        'column' : 'column_name_to_deduplicate',
        '_id' : 'unique_id_column_of_dataset',
        }
    results = dupe.dedupe(input_config)
```

dupandas using custom Cleaner and Matcher configs

```  python
    from dupandas import Dedupe

    clean_config = { 'lower' : True, 'punctuation' : True, 'whitespace' : True, 'digit' : True }
    match_config = { 'exact' : False, 'levenshtein' : True, 'soundex' : False, 'nysiis' : False}
    dupe = Dedupe(clean_config = clean_config, match_config = match_config)

    input_config = {
        'input_data' : pandas_dataframe,
        'column' : 'column_name_to_deduplicate',
        '_id' : 'unique_id_column_of_dataset',
        }
    results = dupe.dedupe(input_config)
```

Other options in input_config 

```python
    input_config = {
        'input_data' : pandas_dataframe,
        'column' : 'column_name_to_deduplicate',
        '_id' : 'unique_id_column_of_dataset',
        'score_column' : 'name_of_the_column_for_confidence_score',
        'threshold' : 0.75, # float value of threshold
        'unique_pairs' : True # boolean to get unique (A=B) or duplicate (A=B and B=A) results
        }
```

## Usage : standalone Cleaner class

```python
    from dupandas import Cleaner
    clean_config = { 'lower' : True, 'punctuation' : True, 'whitespace' : True, 'digit' : True }
    clean = Cleaner(clean_config)
    clean.clean_text("new Delhi 3#! 34 ")
```

## Usage: standalone Matcher class

```python
    from dupandas import Matcher
    match_config = { 'exact' : False, 'levenshtein' : True, 'soundex' : False, 'nysiis' : False}
    match = Matcher(match_config)
    match.match_elements("new delhi", "newdeli")
```

## Issues

Thanks for checking this work, Yes ofcourse there is a scope of improvement, Feel free to submit issues and enhancement requests.

## Contributing
#### ToDos

1. [ ]  V2: Add Support for multi column match
2. [ ]  V2: Add More Matchers
3. [ ]  V2: Add More Cleaners
4. [ ]  V2: Improve Speed
5. [ ]  V3: Add Support for multi column match

#### Steps 
 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** 