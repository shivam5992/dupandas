from dedupe import Dedupe
import pandas as pd 

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digits' : True
}

match_config = {
	'exact' : False,
	'levenshtein' : True,
	'soundex' : False,
	'nysiis' : False, 
}

dupe = Dedupe(clean_config = clean_config, match_config = match_config)

input_config = {
	'input_data' : pd.read_csv('data/sample_data.csv'),
	'column' : 'VillageName',
	'score_column' : 'score',
	'threshold' : 0.75,
	'_id' : 'id',
}

results = dupe.dedupe(input_config)
results.to_csv('data/results.csv')