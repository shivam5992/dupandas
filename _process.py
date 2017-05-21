from Levenshtein import ratio as lev_ratio
import pandas as pd 

class cleanup:
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
class matcher:
	def levenshtein_match(self, text1, text2):
		return lev_ratio(text1, text2)

	def match_records(self, _row, colname):
		text1 = str(_row[colname])
		text2 = str(_row[colname+"_"])	
		
		conf = 0
		conf += self.levenshtein_match(text1, text2)
		## Add other matche algos here

		return conf 


	## Handle for multiple columns 
	def process(self, colname, DF1):

		# Create another dataframe with same column
		# check for multiple columns
		DF2 = pd.DataFrame()
		DF2[colname+"_"] = DF1[colname]

		# Create Cartesian Products
		cartesian_index = '_i_n_d_e_x'
		DF1[cartesian_index] = 0
		DF2[cartesian_index] = 0
		cartesian_pairs = pd.merge(DF1, DF2, on=cartesian_index)

		# Matching Process
		cartesian_pairs['confidence_score'] = cartesian_pairs.apply(lambda row: self.match_records(row, colname), axis=1)
		cartesian_pairs = cartesian_pairs.sort_values(['confidence_score'], ascending=[False])

		drop = [cartesian_index]
		cartesian_pairs = cartesian_pairs.drop(drop, axis=1)

		return cartesian_pairs


if __name__ == '__main__':

	df1 = pd.read_csv('data/data1.csv')

	match = matcher()
	results = match.process('city', df1)
	results.to_csv('test.csv', index=False)
