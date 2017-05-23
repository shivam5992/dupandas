from _process import Matcher

input_config = {
	'column' : 'city',
	'input_data' : 'data/data1.csv'
}

match = Matcher()
results = match.process(input_config)
print results