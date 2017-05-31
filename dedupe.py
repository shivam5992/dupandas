# Imports for Dedupe
import pandas as pd 

# Imports for Matcher 
from Levenshtein import ratio
import fuzzy
soundex = fuzzy.Soundex(4)


# Imports for Cleaner 
import string 
punctuations = string.punctuation

class Cleaner:
	def __init__(self, clean_config = None):

		## stopwords, repeated, urls, mentions, hashtags , badchars, small words 
		## html entities, text encoding, split attached words, unstandardized words
		## slangs, appostrophes, normalization, text encodings 
		
		self.cc = {
			'lower' : True,
			'punctuation' : True,
			'whitespace' : True,
			'digits' : True,
			'html' : True
		}


	def clean_element(self, txt):
		txt = str(txt)

		if self.cc['lower']:
			txt = txt.lower()

		if self.cc['punctuation']:
			txt = "".join([x for x in txt if x not in punctuations])

		if self.cc['whitespace']:
			txt = "".join(txt.split()).strip()

		if self.cc['digits']:
			txt = "".join(x for x in txt if x not in "0987654321")

		# if self.cc['html']:
		# 	txt = txt.replace('','')

		return txt


class Matcher:
	def __init__(self, match_config = None):

		# normalize confidence score (0 to 100)

		## more matching configs 
		self.m_config = {
			'exact' : False, 
			'levenshtein' : False,
			'soundex' : False,
			'nysiis' : False, 

			'jaro' : False,
			'metaphone' : False
		}

		# Override match config 
		for key, value in match_config.iteritems():
			if key in self.m_config:
				if value not in [True, False,1,0]:
					print ("! Invalid Boolean: "+str(value)+", Matcher key: " + str(key))
				else:
					self.m_config[key] = value
			else:
				print ("! Matcher Not Recognized, " + str(key))
				print ("! Available Matchers: " + ", ".join(self.m_config.keys()))

		matcher_applied = [key for key in self.m_config if self.m_config[key]]
		if matcher_applied:
			print ("Applying Matchers: " + ", ".join(matcher_applied))
		else:
			self.m_config['exact'] = True
			print ("No Matchers in config, Applying Default Matcher: exact match")
 
	def match_elements(self, text1, text2):
		conf = 0

		if self.m_config['exact']:
			if text1 == text2:
				conf += 1

		if self.m_config['levenshtein']:
			conf += ratio(text1, text2)

		if self.m_config['soundex']:
			if soundex(text1) == soundex(text2):
				conf += 1 

		if self.m_config['nysiis']:
			if fuzzy.nysiis(text1) == fuzzy.nysiis(text2):
				conf += 1 

		return conf 
		

class Dedupe:
	def __init__(self, clean_config = None, match_config = None):
		self.clean = Cleaner(clean_config)
		self.match = Matcher(match_config)
		## Handle for multiple columns 


	def match_records(self, _row_data, colname):
		text1 = str(_row_data[colname])
		text2 = str(_row_data[colname+"_"])	
		match_score = self.match.match_elements(text1, text2)
		return match_score 


	def clean_records(self, _row_data, colname):
		cleaned = self.clean.clean_element(_row_data[colname])
		return cleaned
 

	def dedupe(self, input_config):

		# Conditional Validation Checks 
		if 'column' in input_config:
			colname = input_config['column']
		else:
			print ("! Terminating!, Key not found - 'colname'")
			exit (0)

		if '_id' in input_config:
			_id = input_config['_id']
		else:
			print ("! Terminating!, Key not found - '_id'")
			exit (0)

		if 'input_data' in input_config:
			input_df = input_config['input_data']
		else:
			print ("! Terminating!, Key not found - 'input_data'")
			exit (0)

		if 'score_column' in input_config:
			scr_colname = input_config['score_column']
		else:
			print ('! Key not found - "score_column", creating column "_score"')
			scr_colname = '_score'

		if 'threshold' in input_config:
			threshold = input_config['threshold']
		else:
			threshold = 0.0

		# Cleaning Process
		clean_colname = "_cln_"+colname
		input_df[clean_colname] = input_df.apply(lambda row_data: self.clean_records(row_data, colname), axis=1)
		

		# Create another dataframe with same column
		temp_df = pd.DataFrame()
		temp_df[_id+"_"] = input_df[_id]
		temp_df[clean_colname+"_"] = input_df[clean_colname]


		# Create Cartesian Products
		cartesian_index = '_i_n_d_e_x'
		input_df[cartesian_index] = 0
		temp_df[cartesian_index] = 0
		pairs = pd.merge(input_df, temp_df, on=cartesian_index)

		
		# Matching Process
		pairs[scr_colname] = pairs.apply(lambda row_data: self.match_records(row_data, clean_colname), axis=1)
		pairs = pairs.sort_values([scr_colname], ascending=[False])
		pairs = pairs[pairs[scr_colname] >= threshold]
		pairs = pairs[pairs[_id] != pairs[_id+"_"]]


		# Create output data frame
		output = pd.DataFrame()
		output[_id] = pairs[_id]
		output[_id+"_"] = pairs[_id+"_"]
		output[scr_colname] = pairs[scr_colname]
		return output