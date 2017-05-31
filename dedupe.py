# Imports for Dedupe
import pandas as pd 

# Imports for Matcher 
import fuzzy
soundex = fuzzy.Soundex(4)

from Levenshtein import ratio

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
		self.m_config = {
			'exact' : False, 
			'levenshtein' : False,
			'soundex' : False,
			'nysiis' : False, 
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

	def match_records(self, _row_data, colname):
		text1 = str(_row_data[colname])
		text2 = str(_row_data[colname+"_"])	
		match_score = self.match.match_elements(text1, text2)
		return match_score 


	def clean_records(self, _row_data, colname):
		cleaned = self.clean.clean_element(_row_data[colname])
		return cleaned

	def validate_config(self, input_config):
		invalid_input = False

		# Mandatory Key Check 	
		mandates = ['column', '_id', 'input_data']
		for mandate in mandates:
			if mandate not in input_config:
				print ("Key not found - '"+mandate+"'")
				invalid_input = True
			else:
				input_df = input_config['input_data']
		
		# Datatype Check 
		for each in input_config:
			if each == 'threshold':
				if 'float' not in  str(type(input_config[each])):
					threshold = 0.0
					print ("Invalid Type: " + str(type(input_config[each])) + ", for " +
										 str(each) + " need float, setting default: 0.0")
				elif not (input_config[each] >= 0 and input_config[each] <= 1):
					threshold = 0.0
					print ("Key threshold should be between 0.0 and 1.0, setting default: 0.0")
				else:
					threshold = input_config[each]
			elif each == 'input_data':
				if 'pandas.core.frame.DataFrame' not in str(type(input_config[each])):
					invalid_input = True
					print ("Invalid type " + str(type(input_config[each])) + ", for " + 
													str(each) + " need Pandas_Data_Frame")
			elif 'str' not in str(type(input_config[each])):
				print ("Invalid type " + str(type(input_config[each])) + ", for " + str(each) + " need str")
				invalid_input = True


		## Availability Check
		keys = ['_id', 'column']
		for key in keys:
			if input_config[key] not in input_config['input_data']:
				print ("Column not present in dataframe: " + str(key))
				invalid_input = True


		if invalid_input:
			print ("Terminating !!!")
			exit(0)

		input_data = input_config['input_data']
		colname = input_config['column']
		_id = input_config['_id']
		
		scr_colname = '_score'
		if 'score_column' in input_config:
			scr_colname = input_config['score_column']

		config ={
			'scr_colname' : scr_colname,
			'_id' : _id,
			'colname' : colname,
			'input_data' : input_data,
			'threshold' : threshold

		}
		return config
			
	def dedupe(self, input_config):

		config = self.validate_config(input_config)

		colname = config['colname']
		input_df = config['input_data']
		threshold = config['threshold']
		_id = config['_id']
		scr_colname = config['scr_colname']


		# Cleaning Process
		cln_col = "_cln_"+colname
		input_df[cln_col] = input_df.apply(lambda row: self.clean_records(row, colname), axis=1)
		

		# Create another dataframe with same column
		temp_df = pd.DataFrame()
		temp_df[_id+"_"] = input_df[_id]
		temp_df[cln_col+"_"] = input_df[cln_col]


		# Create Cartesian Products
		cartesian_index = '_i_n_d_e_x'
		input_df[cartesian_index] = 0
		temp_df[cartesian_index] = 0
		pairs = pd.merge(input_df, temp_df, on=cartesian_index)

		
		# Matching Process
		pairs[scr_colname] = pairs.apply(lambda row: self.match_records(row, cln_col), axis=1)
		pairs = pairs.sort_values([scr_colname], ascending=[False])
		pairs = pairs[pairs[scr_colname] >= threshold]
		pairs = pairs[pairs[_id] != pairs[_id+"_"]]


		# Create output data frame
		output = pd.DataFrame()
		output[_id] = pairs[_id]
		output[_id+"_"] = pairs[_id+"_"]
		output[scr_colname] = pairs[scr_colname]
		return output		
