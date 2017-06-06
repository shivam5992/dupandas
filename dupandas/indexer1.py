# -*- coding: utf-8 -*-
import whoosh
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser

schema = Schema(name=TEXT(stored=True))
idx = create_in("indexdir", schema, "idx_name")

writer = idx.writer()

writer.add_document(name=u"moombai")
writer.add_document(name=u"new dlhi")
writer.add_document(name=u"nu delhi")
writer.add_document(name=u"kolkatta")
writer.add_document(name=u"calcutta")
writer.add_document(name=u"kolcutta")
writer.add_document(name=u"this is sample text")
writer.add_document(name=u"this is crazy data")
writer.add_document(name=u"deli sample example")
writer.add_document(name=u"to test kolkata sample")
writer.add_document(name=u"data is crazy text")
writer.add_document(name=u"machine data learning")

writer.commit()

s = idx.searcher()

visited = {}
res = s.search(FuzzyTerm("name", u"delhi", maxdist=3, prefixlength=1))
for r in res:
	if r['name'] not in visited:
		visited[r['name']] = 1
		print r['name']

s.close()