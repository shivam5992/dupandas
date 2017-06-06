import whoosh
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.query import FuzzyTerm
import pandas as pd 

def _index_data(inputDF, colname):
	
	# todo - save old indexes, custom index path and name 
	schema = Schema(name=TEXT(stored=True))
	_index = create_in("indexdir", schema, "idx_name")
	writer = _index.writer()

	inputDF.apply(lambda x: writer.add_document(name=unicode(x[colname])), axis = 1)

	writer.commit()
	return _index 

def _search_index(my_index, text):
	searcher = my_index.searcher()

	res = searcher.search(FuzzyTerm("name", unicode(text), maxdist=5, prefixlength=1))
	res1 = searcher.search(FuzzyTerm("name", unicode(text).split(), maxdist=5, prefixlength=1))
	
	visited = {}
	for r in res:
		if r['name'] not in visited:
			visited[r['name']] = 1

	for r in res1:
		if r['name'] not in visited:
			visited[r['name']] = 1

	searcher.close()

	return visited.keys()

def _create_pairs(inputDF, colname):
	pairsDF = pd.DataFrame()

	# create index
	my_index = _index_data(inputDF, colname)

	# create cartesian pairs
	print inputDF.apply(lambda x: _search_index(my_index, x[colname]), axis = 1)


inputDF = pd.read_csv('../data/test_data.csv')
colname = 'city'
print inputDF
_create_pairs(inputDF, colname)