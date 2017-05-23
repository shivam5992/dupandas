import pandas as pd 
from Levenshtein import ratio

class Cleaner:
	def __init__(self, data, clean_config):
		self.clean_config = clean_config
		self.columns = data['columns']
		self.df = data['inp_df']

		for col in self.columns:

			## check if column not in data frame 
			self.df["cln_"+col] = self.df[col].apply(lambda x : self._clean_tet(x)) 

	def _clean_text(self, txt):
		txt = str(txt)
		if self.clean_config['lower']:
			txt = txt.lower()
		if self.clean_config['punctuation']:
			txt = "".join([x for x in txt if x not in exclude])
		if self.clean_config['whitespace']:
			txt = "".join(txt.split()).strip()
		if self.clean_config['digits']:
			txt = "".join(x for x in txt if x not in "0987654321")
		return txt

		## stopwords, repeated, urls, mentions, hashtags , badchars, small words 
		## html entities, text encoding, split attached words, unstandardized words
		## slangs, appostrophes, normalization
		

## control - clean and match separate 
class Matcher:
	def __init__(self, config):

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

	def levenshtein_match(self, text1, text2):
		return ratio(text1, text2)

	def match_records(self, _row, colname):
		text1 = str(_row[colname])
		text2 = str(_row[colname+"_"])	
		
		conf = 0
		conf += self.levenshtein_match(text1, text2)
		## Add other matche algos here

		return conf 


	## Handle for multiple columns 
	def process(self, input_config):
		if 'colname' in input_config:
			colname = input_config['colname']
		else:
			print ("Terminating!, Key not found - 'colname'")

		if 'input_data' in input_config:
			inputDF = input_config['input_data']
		else:
			print ("Terminating!, Key not found - 'input_data'")

		if 'score_column_name' in input_config:
			scr_colname = input_config['score_column_name']
		else:
			print ('Key not found - "score_column_name", creating column "confidence_score"')
			scr_colname = 'confidence_score'

		## todo - check for multiple columns

		# Create another dataframe with same column
		tempDF = pd.DataFrame()
		tempDF[colname+"_"] = inputDF[colname]

		# Create Cartesian Products
		cartesian_index = '_i_n_d_e_x'
		inputDF[cartesian_index] = 0
		tempDF[cartesian_index] = 0
		cartesian_pairs = pd.merge(inputDF, tempDF, on=cartesian_index)

		# Matching Process
		cartesian_pairs[scr_colname] = cartesian_pairs.apply(lambda row: self.match_records(row, colname), axis=1)
		cartesian_pairs = cartesian_pairs.sort_values([scr_colname], ascending=[False])

		# Drop Temporary Index column
		drop = [cartesian_index]
		cartesian_pairs = cartesian_pairs.drop(drop, axis=1)

		return cartesian_pairs


