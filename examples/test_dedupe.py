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
	'input_data' : pd.read_csv('examples/data/example.csv'),
	'column' : 'City',
	'_id' : 'Id',

	'score_column' : 'score',
	'threshold' : 0.75,
	'unique_pairs' : True,
	'indexing' : True
}

results = dupe.dedupe(input_config)
results.to_csv('examples/data/results.csv', index = False)