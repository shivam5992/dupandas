from _process import cleanup, matcher
import pandas as pd 

inp_df = pd.DataFrame()
columns = ['a','b']

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digits' : True
}

match_config = {
	'exact' : True,
	'levenshtein' : True,
	'soundex' : True
}

data = {
	'inp_df' : inp_df,
	'columns' : columns,
	'clean_config' : clean_config
}
clean = cleanup(data)