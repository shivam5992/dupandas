from dupandas import Matcher

match_config = {
	'exact' : False,
	'levenshtein' : True,
	'soundex' : False,
	'nysiis' : False, 
}

match = Matcher(match_config)


text1 = "new delhi"
text2 = "newdeli"

print (match.match_elements(text1, text2))