from dupandas import Dedupe
import pandas as pd 

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digit' : True,
}

match_config = {
	'exact' : False,
	'levenshtein' : True,
	'soundex' : False,
	'nysiis' : False, 
}

dupe = Dedupe(clean_config = clean_config, match_config = match_config)

input_config = {
	'input_data' : pd.read_csv('examples/data/sample1.csv'),
	'column' : 'city',
	'score_column' : 'score',
	'threshold' : 0.75,
	'_id' : 'id',
	'unique_pairs' : True,
	'indexing' : False
}

results = dupe.dedupe(input_config)
results.to_csv('examples/data/results.csv')