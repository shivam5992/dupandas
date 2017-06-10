import pandas as pd 

from lucene import Document, Field, RAMDirectory, Term
from lucene import IndexWriter, WhitespaceAnalyzer, FuzzyQuery, IndexSearcher
import lucene
lucene.initVM()

class LuceneIndexer:
	"""
	python class to index the text data using lucene. It uses pylucene for indexing
	and searching purposes
	"""

	def _addDoc(self, text, writer):
		"""
		function to add documents in the lucene index. 
		text fields are indexed by the name "field"
		"""

		doc = Document()
		doc.add(Field("field", text, Field.Store.YES, Field.Index.ANALYZED))
		writer.addDocument(doc)

	def _createIndex(self, inputDF, colname):
		"""
		function to create lucene index, iterates over inputDF row 
		by row, and indexes the relevant column

		By default - WhitespaceAnalyzer is used, other Analyzers are also available.
		"""

		# Create index directory
		directory = RAMDirectory()
		writer = IndexWriter(directory, WhitespaceAnalyzer(), True, IndexWriter.MaxFieldLength.LIMITED)
	  	
	  	# Inline indexing of column data
		inputDF.apply(lambda x: self._addDoc(x[colname], writer), axis = 1)

		# Optimize, close and return 
		writer.optimize()
		writer.close()
		return directory

	def _searchIndex(self, searcher, row, colname, id_col):
		"""
		function to search text in the lucene index, iterates over inputDF row 
		by row, and search the matched candidates with a match score

		By default - WhitespaceAnalyzer is used, other Analyzers are also available.
		"""

		text = row[colname]
		idd = row[id_col]

		# Search word by word of a text containing multiple keywords
		words = text.split()
		results = []
		for word in words:
			query = FuzzyQuery(Term("field", word))
			scoreDocs = searcher.search(query, 50).scoreDocs

			candidates = str(scoreDocs).split("[")[1].split("]")[0].split(",")
			for i, candidate in enumerate(candidates):
				if not candidate:
					continue
				
				# Matches : Value + Score
				score = float(candidate.split("score=")[1].replace(">","").strip())
				value = searcher.doc(scoreDocs[i].doc).get("field")
				if value in results:
					continue

				results.append((idd, text, value))

		return results
		
	def _create_pairs(self, inpDF, colname, idd):
		"""
		function to create cartesian pairs of matched-similar text records
		first calls create index function followed by search index row by row 
		in a pandas dataframe 
		"""

		pairs = []
		directory = self._createIndex(inpDF, colname)

		searcher = IndexSearcher(directory, True)
		matches = inpDF.apply(lambda x: self._searchIndex(searcher, x, colname, idd), axis = 1)
		
		for match_pair in matches:
			for matched in match_pair:
				value_index = inpDF[inpDF[colname] == matched[2]].index.tolist()
				for cell_index in value_index:
					if matched[0] != cell_index:
						row = []
						row.append(matched[0])
						row.append(matched[1])
						row.append(cell_index)
						row.append(matched[2])
						pairs.append(row)

		searcher.close()
		directory.close()

		header = [idd,colname,idd+"_",colname+"_"]
		pairDF = pd.DataFrame(pairs, columns = header)
		return pairDF