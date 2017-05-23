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
	def __init__(self):

		## Handle for multiple columns 
		## Add cleaning code 
		## Add Multiple Matching Algos - 
		## todos 

		self.clean_config = {
			'lower' : True,
			'punctuation' : True,
			'whitespace' : True,
			'digits' : True
		}

		self.match_config = {
			'exact_math' : True,
			'levenshtein_ratio' : True,
			'soundex' : True,
			'metaphone' : True, 
			'Jaro' : True,
		}

	def clean_records():
		pass

	def match_records():
		text1 = str(_row[colname])
		text2 = str(_row[colname+"_"])	
		
		conf = 0
		conf += ratio(text1, text2)
		
		return conf 

	def process_records(self, _row, colname):
		cleaned = clean_records() 
		matched = match_records()
 
	def dedupe(self, input_config):
		if 'column' in input_config:
			colname = input_config['column']
		else:
			print ("Terminating!, Key not found - 'colname'")
			exit (0)

		if '_id' in input_config:
			_id = input_config['_id']
		else:
			print ("Terminating!, Key not found - '_id'")
			exit (0)

		if 'input_data' in input_config:
			input_df = input_config['input_data']
		else:
			print ("Terminating!, Key not found - 'input_data'")
			exit (0)

		if 'score_column' in input_config:
			scr_colname = input_config['score_column']
		else:
			print ('Key not found - "score_column", creating column "_score"')
			scr_colname = '_score'

		if 'threshold' in input_config:
			threshold = input_config['threshold']
		else:
			threshold = 0.0

		# Create another dataframe with same column
		temp_df = pd.DataFrame()
		temp_df[_id+"_"] = input_df[_id]
		temp_df[colname+"_"] = input_df[colname]

		# Create Cartesian Products
		cartesian_index = '_i_n_d_e_x'
		input_df[cartesian_index] = 0
		temp_df[cartesian_index] = 0
		pairs = pd.merge(input_df, temp_df, on=cartesian_index)

		# Matching Process
		pairs[scr_colname] = pairs.apply(lambda row: self.process_records(row, colname), axis=1)
		pairs = pairs.sort_values([scr_colname], ascending=[False])
		pairs = pairs[pairs[scr_colname] >= threshold]
		pairs = pairs[pairs[_id] != pairs[_id+"_"]]

		# Create output data frame
		output = pd.DataFrame()
		output[_id] = pairs[_id]
		output[_id+"_"] = pairs[_id+"_"]
		return output