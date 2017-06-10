from dupandas import Cleaner

clean_config = {
	'lower' : True,
	'punctuation' : True,
	'whitespace' : True,
	'digit' : True,
}

clean = Cleaner(clean_config)
text1 = "new Delhi 3#! 34 "
print (clean.clean_text(text1))