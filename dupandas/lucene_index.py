import lucene

from lucene import * 


def make_index():

    lucene.initVM()
    path = "test.txt"
  
    # 1. create an index
    index_path = File(path)
    analyzer = StandardAnalyzer(Version.LUCENE_35)
    index = SimpleFSDirectory(index_path)
    config = IndexWriterConfig(Version.LUCENE_35, analyzer)
    writer = IndexWriter(index, config)

    # 2 construct documents and fill the index

    doc = Document()
    doc.add(Field("Text", "this is a sample text", Field.Store.YES, Field.Index.ANALYZED))
    doc.add(Field("Text", "many new data is a sample text", Field.Store.YES, Field.Index.ANALYZED))
    doc.add(Field("Text", "another beautgy data science is a sample text", Field.Store.YES, Field.Index.ANALYZED))
    doc.add(Field("Text", "company is a working text", Field.Store.YES, Field.Index.ANALYZED))
    doc.add(Field("Text", "this google a sample worder", Field.Store.YES, Field.Index.ANALYZED))
    writer.addDocument(doc)

    # 3. close resources
    writer.close()
    index.close()



def search(indexDir, kwds):
    '''Simple Search
    Input paramenters:
        1. indexDir: directory name of the index
        2. kwds: query string for this simple search
    display_verse(): procedure to display the specified bible verse 
    '''
    lucene.initVM()
    # 1. open the index
    analyzer = StandardAnalyzer(Version.LUCENE_35)
    index = SimpleFSDirectory(File(indexDir))
    reader = IndexReader.open(index)
    n_docs = reader.numDocs()

    # 2. parse the query string
    queryparser = QueryParser(Version.LUCENE_35, "Text", analyzer)
    query = queryparser.parse(kwds)

    # 3. search the index 
    searcher = IndexSearcher(reader)
    hits = searcher.search(query, n_docs).scoreDocs

    # 4. display results
    for i, hit in enumerate(hits):
        doc = searcher.doc(hit.doc)
        # book = doc.getField('Text').stringValue()
        print doc 

        
    # 5. close resources
    searcher.close()

# make_index()
search("test.txt","text")