#-*- coding: utf-8 -*- 
import csv
import re
from nltk.corpus import stopwords
import nltk, string
from appos import appos
from slangs import slangs
from emoticons import emo
import HTMLParser, itertools, urllib, urlparse, json
from nltk.stem.wordnet import WordNetLemmatizer

html_parser = HTMLParser.HTMLParser()
exclude = set(string.punctuation)
lmtzr = WordNetLemmatizer()



from textblob import Word

def appos_look_up(text):
	words = text.split()
	new_text = []
	for word in words:
		word_s = word.lower()
		if word_s in appos.appos:
			new_text.append(appos.appos[word_s])
		else:
			new_text.append(word)
	apposed = " ".join(new_text)
	return apposed

def remove_expressions(text):
	newtext = text
	if text.find("[") >= 0:
		indexes = [m.start() for m in re.finditer('\[', text)]
		for ind in indexes:
			indf = text[ind:].find("]")
			newtext = newtext.replace(text[ind:ind + indf] + "]", " ")
	text = newtext.replace("—","  ")
	return text

def handle_encoding(text):
	text = text.encode("utf-8").decode("ascii","ignore")
	return text

def remove_punctuations(text, customlist):
	if not customlist:
		customlist = exclude
	for punc in customlist:
		text = text.replace(punc, " ")
	return text

def remove_stopwords(text):
	tokenized_words = text.split()
	filtered_words = []
	for word in tokenized_words:
		if not word.lower() in stopwords.words('english'):
			filtered_words.append(word)
	text = " ".join(filtered_words)
	return text

def extra_rep(text):
	for each in exclude:
		text = text.replace(each+each, each)
		text = text.lstrip(each).rstrip(each)
	text = re.sub(' +',' ',text)
	text = text.strip()
	return text

def improve_repeated(text):
	text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
	return text 

def escape(text):
    return html_parser.unescape(text)

def emoticons_look_up(text):
	words = text.split()

	emolist = []
	for word in words:
		if word in emo.emo:
			emolist.append(str(emo.emo[word]))
			text = text.replace(word," ")
	emores = ",".join(emolist)
	return text, emores

def slang_look_up(text):
	words = text.split()
	new_text = []
     
	for word in words:
		word_s = word.lower()
		if word_s in slangs.slangs:
			new_text.append(slangs.slangs[word_s])
		else:
			new_text.append(word)
	slanged = " ".join(new_text)
	return slanged


def get_ginger_url(text):
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urllib.urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", text)])
    fragment = ""
    return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))

''' Connect with Ginger Api '''
def get_ginger_result(text):
    url = get_ginger_url(text)
    try:
        response = urllib.urlopen(url)
    except HTTPError as e:
            print("HTTP Error:", e.code)
            quit()
    except URLError as e:
            print("URL Error:", e.reason)
            quit()
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))
        quit
    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")
        quit()
    return(result)

def grammetize(original_text):
    fixed_text = original_text
    results = get_ginger_result(original_text)
    color_gap = 0
    for result in results["LightGingerTheTextResult"]:
        if(result["Suggestions"]):
            from_index = result["From"] + color_gap
            to_index = result["To"] + 1 + color_gap
            suggest = result["Suggestions"][0]["Text"]
            orig = original_text[from_index:to_index]

            fixed_text = original_text[:from_index] + suggest + original_text[to_index:]

    return fixed_text


def remove_url(text):
	urlfree = []
	for word in text.split():
		if not word.startswith("www"):
			urlfree.append(word)
		elif not word.startswith("http"):
			urlfree.append(word)
		elif not word.endswith(".html"):
			urlfree.append(word)
	urlfree = " ".join(urlfree)

	urls = re.finditer(r'http[\w]*:\/\/[\w]*\.?[\w-]+\.+[\w]+[\/\w]+', urlfree)
	for i in urls:
		urlfree = re.sub(i.group().strip(), '', urlfree)
	return urlfree

def remove_url_word(text):
	words = text.split()
	newres = ""
	for each in words:
		if not each.startswith('http'):
			newres += " "
			newres += each
	return newres.strip()

def remove_mention(text):
	urls = re.finditer(r'@[A-Za-z0-9\w]*', text)
	for i in urls:
		text = re.sub(i.group().strip(), '', text)
	return text

def remove_hashtag(text):
	urls = re.finditer(r'#[A-Za-z0-9\w]*', text)

	for i in reversed(list(urls)):
		tag = i.group()
		# print tag, text.index(tag)+len(tag), len(text.strip())
		''' Special condition to check if hashtag lies inside the sentence or not '''
		if len(text.strip()) == (text.index(tag) + len(tag)):
			text = re.sub(i.group().strip(), '', text)
	return text

def splitAttached(line):
	reconstructedWord = []
	for word in line.split():
		if not word.isupper():
			lis = re.findall('[^ ][^A-Z]*', word)
			if len(lis) == 1 or lis[0].islower():
				reconstructedWord.append(word)
			else:
				separateWordReconstruction = ''
				for separateWord in lis:
					# Handling the case of #ItsBMW  # Capital words together
					if(len(separateWord)==1) or (len(separateWord) == 2 and separateWord.endswith('s')):
						separateWordReconstruction = separateWordReconstruction + separateWord
					else:
						separateWordReconstruction = separateWordReconstruction + " " + separateWord.lower() + " "
				reconstructedWord.append(separateWordReconstruction)
		else:
			reconstructedWord.append(word)

	stringToBeReturned = " ".join(reconstructedWord)
	return ' '.join(stringToBeReturned.split())

def twitter_slang_look_up(text):
	twitterSlangLookup = {'rt':'','dm':'direct message'}

	words = text.split()
	new_text = []
     
	for word in words:
		word_s = word.lower()
		if word_s in twitterSlangLookup:
			new_text.append(twitterSlangLookup[word_s])
		else:
			new_text.append(word)
	unSlanged = " ".join(new_text)
	return unSlanged

def removeSmallWordsAndDigits(text):
	new_text = []
	for each in text.split():
		if len(each)>2 and not each.isdigit():
			new_text.append(each)

	return " ".join(new_text)

def LemIt(sent):
	lem = []
	sent = sent.lower()
	for each in sent.split():
		w = Word(each)
		l = w.lemmatize("v")
		if l == w:
			l = w.lemmatize("n")
		if l == w:		
			l = w.lemmatize("a")
		if l == w:
			l = w.lemmatize("r")
		lem.append(l)
	lemsent = " ".join(lem)
	return lemsent

def remove_alphanumerics(text):
	txt = []
	for each in text.split():
		if not any(x in each.lower() for x in "0123456789"):
			txt.append(each)
	txtsent = " ".join(txt)
	return txtsent 

def remove_badchars(text):
	updated = []
	for wrd in text.split():
		if len(wrd) == 3 and wrd.startswith("x"):
			pass
		else:
			updated.append(wrd)
	return " ".join(updated)

def clean(text):
	text = str([text])
	text = escape(text)
	text = handle_encoding(text)
	
	text = remove_url(text)

	text = appos_look_up(text)
	text = improve_repeated(text)
	
	# text, emo = emoticons_look_up(text)
	text = remove_punctuations(text, customlist = [])

	# # text = remove_expressions(text)
	text = LemIt(text)
	text = splitAttached(text)
	text = remove_stopwords(text)
	
	text = removeSmallWordsAndDigits(text)
	text = remove_alphanumerics(text)
	
	# text = remove_mention(text)
	# text = remove_hashtag(text)

	# text = twitter_slang_look_up(text)
	# text = slang_look_up(text)

	text = extra_rep(text)
	text = remove_badchars(text)
	
	# text = grammetize(text)
	# return text.strip(), emo
	text = text.lower()
	return text.strip()

