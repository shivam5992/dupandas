from dedupe import Dedupe
import pandas as pd 

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digits' : True
}

match_config = {
	'exact' : True,
	'levenshtein' : True,
	'soundex' : True,
	'nysiis' : True, 
}

dupe = Dedupe(clean_config = clean_config, match_config = match_config)

#### todos 
# unique pairs = True, False 
# logs = True / False 
# normalize confidence score (0 to 100)
# comented code 

# Add Support for Multi Column Match
# Add other matching algos - jaro, metaphone
# Add More Cleaning Functions 

input_config = {
	'input_data' : pd.read_csv('data/test_data.csv'),
	'column' : 'city',
	'score_column' : 'score',
	'threshold' : 0.75,
	'_id' : 'id',
}

results = dupe.dedupe(input_config)
print results