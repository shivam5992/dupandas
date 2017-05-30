from dedupe import Dedupe
import pandas as pd 

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digits' : True
}

match_config = {
	'exact_math' : True,
	'levenshtein_ratio' : True,
	'soundex' : True,
	'metaphone' : True, 
	'jaro' : True,
}

dupe = Dedupe(clean_config = clean_config, match_config = match_config)

# unique pairs = True, False 
input_config = {
	'input_data' : pd.read_csv('data/test_data.csv'),
	'column' : 'city',
	'score_column' : 'score',
	'threshold' : 0.75,
	'_id' : 'id'
}

results = dupe.dedupe(input_config)
print results