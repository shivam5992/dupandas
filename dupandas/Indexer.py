import whoosh
from whoosh.index import create_in
import whoosh.index as index
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

	res = searcher.search(FuzzyTerm("name", unicode(text), maxdist=1, prefixlength=1))
	# res1 = searcher.search(FuzzyTerm("name", unicode(text).split(), maxdist=5, prefixlength=1))

	visited = {}
	for r in res:
		if r['name'] not in visited:
			visited[r['name']] = 1

	# for r in res1:
	# 	if r['name'] not in visited:
	# 		visited[r['name']] = 1

	searcher.close()

	candidates = visited.keys()
	return candidates
	
def _create_pairs(inpDF, colname, ID):

	# create index
	# _index = _index_data(inpDF, colname)
	print "ER"
	_index = index.open_dir("indexdir", indexname="idx_name")
	print "ER1 "

	# search relevant pairs 
	candidates = inpDF.apply(lambda x: _search_index(_index, x[colname]), axis = 1)
	print "#$"

	# create cartesian pairs
	pairs = []
	for i, candidate in enumerate(candidates):

		for value in candidate:
			value_index = inpDF[inpDF[colname] == value].index.tolist()
			for cell in value_index:

				# create cartesian row 
				row = []
				row.append(inpDF.ix[i][ID])
				row.append(inpDF.ix[i][colname])
				row.append(cell+1)
				row.append(value)
				pairs.append(row)

	# generate final dataframe
	header = [ID,colname,ID+"_",colname+"_"]
	pairsDF = pd.DataFrame(pairs, columns = header)
	return pairsDF

input_config = {
	'input_data' : pd.read_csv('../data/sample.csv'),
	'column' : 'city',
	'_id' : 'id',
}
print _create_pairs(input_config['input_data'], 'city' , 'id')