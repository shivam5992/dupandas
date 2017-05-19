from Levenshtein import ratio as lev_ratio

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
	def levenshtein_match(text1, text2):
		return lev_ratio(text1, text2)

	def match_records(x):
		t1 = str(x['cln_col1'])
		t2 = str(x['cln_col2'])	
		
		s1 = levenshtein_match(t1, t2)
		c['confidence'] = s1

		## Add other matche algos here 

	## Handle for multiple columns 
	def process():
		cartesian_pairs = pd.merge(DF1, DF2, on = [col])

		cartesian_pairs.apply(lambda x: match_records(x, 'halka'), axis=1)

		## sort and return the id pairs 

if __name__ == '__main__':
	matcher()


