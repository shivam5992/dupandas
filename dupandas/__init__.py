# Imports for Dedupe
import pandas as pd 

# Imports for Matcher 
import fuzzy
soundex = fuzzy.Soundex(4)

from Levenshtein import ratio

# Imports for Cleaner 
import string 
punctuations = string.punctuation

# Imports for Indexer 

class Matcher:
	"""
	python class for matching text records using different matching criterions. Currently, 
	exact matching, levenshtein match, soundex and nysiis are supported. 

	use: default configuration

	match = Matcher()
	score = match.match_elements(text1, text2)
	# returns the confidence score of exact match between two strings 

	use: custom configuration

	match_config = {
		'exact' : True, 'levenshtein' : True, 'soundex' : True, 'nysiis' : True
	}
	match = Matcher(match_config)
	score = match.match_elements(text1, text2)
	# returns the confidence score of flexible match between two strings using criterions mentioned
	"""

	def __init__(self, match_config = None):
		self.m_config = {
			'exact' : False, 
			'levenshtein' : False,
			'soundex' : False,
			'nysiis' : False, 
		}

		# Override match config and validation check
		if match_config != None:
			for key, value in match_config.iteritems():
				if key in self.m_config:
					if value not in [True, False,1,0]:
						print ("Invalid: Incorrect boolean value: "+str(value)+" for key: " + str(key))
					else:
						self.m_config[key] = value
				else:
					print ("Invalid: Matcher not recognized: " + str(key) + ", available Matchers: " +
																		 ", ".join(self.m_config.keys()))

		matcher_applied = [key for key in self.m_config if self.m_config[key]]
		if matcher_applied:
			print ("Applying Matchers: " + ", ".join(matcher_applied))
		else:
			self.m_config['exact'] = True
			print ("Warning: No matchers in config, applying default: exact match")
 	
	def match_elements(self, text1, text2):
		"""
		utility function to match two strings, makes use of 
		match config initiated in __init__ 

		returns the output as confidence score of flexible match
		"""

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


class Cleaner:
	"""
	python class to clean a text using different conditions - 
	uses clean config to perform cleaning on text 

	lower casing, punctuations, whitespace removal, digit removal, html removal etc. 
	"""

	def __init__(self, clean_config = None):
		self.cc = {
			'lower' : False,
			'punctuation' : False,
			'whitespace' : False,
			'digit' : False,
		}

		# Override clean config and validation check
		if clean_config != None:
			for key, value in clean_config.iteritems():
				if key in self.cc:
					if value not in [True, False,1,0]:
						print ("Invalid: Incorrect boolean value: "+str(value)+" for key: " + str(key))
					else:
						self.cc[key] = value
				else:
					print ("Invalid: Cleaner not recognized: " + str(key) + ", available Cleaners: " +
																	 ", ".join(self.cc.keys()))

		cleaners_applied = [key for key in self.cc if self.cc[key]]
		if cleaners_applied:
			print ("Applying Cleaners: " + ", ".join(cleaners_applied))
		else:
			print ("Warning: No cleaners in config")
 


	def clean_text(self, txt):
		"""
		function to clean a text on the basis of configurations mentioned in clean config.
		"""

		txt = str(txt)

		if self.cc['lower']:
			txt = txt.lower()

		if self.cc['punctuation']:
			txt = "".join([x for x in txt if x not in punctuations])

		if self.cc['whitespace']:
			txt = "".join(txt.split()).strip()

		if self.cc['digit']:
			txt = "".join(x for x in txt if x not in "0987654321")

		return txt


class Dedupe:
	"""
	python class to deduplicate columns of a pandas data frame, 
	currently it supports single coulmn deduplication only. 

	makes use of Cleaner and Matcher class for text cleaning and matching purposes
	"""

	def __init__(self, clean_config = None, match_config = None):
		self.clean = Cleaner(clean_config)
		self.match = Matcher(match_config)


	def match_records(self, _row_data, colname):
		""" 
		function to obtain column values from two columns and apply matching functions
		"""
		
		text1 = str(_row_data[colname])
		text2 = str(_row_data[colname+"_"])	
		match_score = self.match.match_elements(text1, text2)
		return match_score 

	def clean_records(self, _row_data, colname):
		""" 
		function to obtain column value from relevant column and apply cleaning functions
		"""

		cleaned = self.clean.clean_text(_row_data[colname])
		return cleaned

	def validate_config(self, input_config):
		"""
		function to validate the input_config provided while calling deduplication process

		validation checks: 

		mandatory fields: colname, _id, input_data
		datatype checks: input_data should be pandas dataframe, 
						 threshold should be float,
						 every other value should be str
		availability checks: _id and colname should exist in input_data
		"""

		invalid_input = False

		# Mandatory Key Check 	
		mandates = ['column', '_id', 'input_data']
		for mandate in mandates:
			if mandate not in input_config:
				print ("Key not found - '"+mandate+"'")
				invalid_input = True
			else:
				input_df = input_config['input_data']

		## Terminate if validation is failed
		if invalid_input:
			print ("Terminating !!!")
			exit(0)

		# Defaults
		threshold = 0.0
		unique_pairs = True
		indexing = False
		
		# Datatype Check 
		for each in input_config:
			if each == 'threshold':
				if 'float' not in  str(type(input_config[each])):
					print ("Invalid: Type: " + str(type(input_config[each])) + " not recognized for " +
										 str(each) + " need float, setting default: 0.0")
				else:
					threshold = input_config[each]
			elif each == 'input_data':
				if 'pandas.core.frame.DataFrame' not in str(type(input_config[each])):
					invalid_input = True
					print ("Invalid: Type " + str(type(input_config[each])) + " not recognized for " + 
													str(each) + " need Pandas_Data_Frame")
			elif each == 'unique_pairs':
				if input_config[each] not in [True, False, 0, 1]:
					print ("Invalid: Type " + str(type(input_config[each])) + " not recognized for " + 
													str(each) + " need Boolean, setting default: True")
				else:
					unique_pairs = input_config['unique_pairs']

			elif each == 'indexing':
				if input_config[each] not in [True, False, 0, 1]:
					print ("Invalid: Type " + str(type(input_config[each])) + " not recognized for " + 
													str(each) + " need Boolean, setting default: False")
				else:
					indexing = input_config['indexing']

			elif each in ['column', '_id', 'score_column']:
				if 'str' not in str(type(input_config[each])):
					print ("Invalid: Type " + str(type(input_config[each])) + ", for " + str(each) + " need str")
					invalid_input = True

			else:
				print ("Warning: Key not recognized - " + str(each))
					

		## Terminate if validation is failed
		if invalid_input:
			print ("Terminating !!!")
			exit(0)

		## Availability Check
		keys = ['_id', 'column']
		for key in keys:
			if input_config[key] not in input_config['input_data']:
				print ("Invalid: column - " + str(key) + " not present in dataframe")
				invalid_input = True

		## Terminate if validation is failed
		if invalid_input:
			print ("Terminating !!!")
			exit(0)

		scr_colname = '_score'
		if 'score_column' in input_config:
			scr_colname = input_config['score_column']

		## Create final validated input configuration
		config = {
			'scr_colname' : scr_colname,
			'_id' : input_config['_id'],
			'colname' : input_config['column'],
			'input_data' : input_config['input_data'],
			'threshold' : threshold,
			'unique_pairs' : unique_pairs,
			'indexing' : indexing
		}
		return config
			
	def dedupe(self, input_config):
		""" 
		master function to perform deduplication on pandas column using flexible string matching
		uses Cleaner and Matcher class

		Flow: 
			- perform cleaning on the desired column
			- create duplicate cleaned column
			- create cartesian pairs of cleaned column and its duplicate
			- perform matching functions and return the score
			- create and return output dataframe
		"""

		config = self.validate_config(input_config)

		colname = config['colname']
		input_df = config['input_data']
		scr_colname = config['scr_colname']
		_id = config['_id']


		# Cleaning Process
		cln_col = "_cln_"+colname
		input_df[cln_col] = input_df.apply(lambda row: self.clean_records(row, colname), axis=1)
		
		# Create Cartesian Pairs
		print ("Applying Indexing: " + str(config["indexing"]))
		if config['indexing']:

			# Lazy Import : Any Suggestions to Improve ? 
			from Indexer import LuceneIndexer

			# cartesian pairs using indexing by lucene
			LI = LuceneIndexer()
			pairs = LI._create_pairs(input_df, cln_col, _id)
		else:
			# default cartesian pairs (slow)
			temp_df = pd.DataFrame()
			temp_df[_id+"_"] = input_df[_id]
			temp_df[cln_col+"_"] = input_df[cln_col]

			cartesian_index = '_i_n_d_e_x'
			input_df[cartesian_index] = 0
			temp_df[cartesian_index] = 0
			pairs = pd.merge(input_df, temp_df, on=cartesian_index)

		# Matching Process
		pairs[scr_colname] = pairs.apply(lambda row: self.match_records(row, cln_col), axis=1)
		pairs = pairs.sort_values([scr_colname], ascending=[False])
		pairs = pairs[pairs[scr_colname] >= config['threshold']]
		pairs = pairs[pairs[_id] != pairs[_id+"_"]]


		# Create output data frame
		output = pd.DataFrame()
		output[_id] = pairs[_id]
		output[_id+"_"] = pairs[_id+"_"]
		output[scr_colname] = pairs[scr_colname]


		# Remove Duplicate Pairs 
		if config['unique_pairs']:
			visited_hash = {}
			remove_indexes = []
			for index, row in output.iterrows():
				hash_index = "-".join(sorted([str(row[_id]), str(row[_id+"_"])]))
				if hash_index not in visited_hash:
					visited_hash[hash_index] = 1
				else:
					remove_indexes.append(index)
			output = output.drop(remove_indexes) 

		return output