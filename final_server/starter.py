import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import inventory
import logging
import os, uuid
import json
import SampleClassifier
import codecs
import pickle
import index
import doc
import urllib
from itertools import chain
from collections import *
import hashlib

NUM_RESULTS = 10
_UPLOADS = "./uploads/"
SETTINGS = {"static_path": "./webapp"}
REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "0123456789=[]\\\"\'")

class HashPartitioner:
    def __init__(self, numReducers):
        self.numReducers = numReducers

    def __call__(self, key):
        return int(hashlib.md5(key).hexdigest()[:8], 16) % self.numReducers

class UploadHandler(web.RequestHandler):

    def post(self):
        #logging.info(self.request.files)
        fileinfo = self.request.files['file'][0]
        #logging.info("fileinfo is %s" % fileinfo)
        fname = fileinfo['filename']
        ftype = fileinfo['content_type']
        #logging.info("Upload File Name is %s" % fname)
        #logging.info("Upload File Type is %s" % ftype)
        #logging.info("File size is %d" % len(fileinfo['body']))
        #print type(fileinfo['body']) 
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        #logging.info(_UPLOADS)
        fh = open(_UPLOADS + cname, 'w')
        fh.write(fileinfo['body'])
        #textBody, oriTags = self.loadVergeText(fileinfo['body'])
        oriTags = []
        textBody = unicode(fileinfo['body'], "utf-8")
        clean_tags = set()
        for tag in oriTags:
                tag = tag.translate(REMOVE_PUNCT_MAP)
                if len(tag) != 0:
                    temp = tag.split(",")
                for t in temp:
                    clean_tags.add(t)
        clean_tags = list(clean_tags)
        tags = SampleClassifier.classifyDocument(textBody)
        response = {
            "status" : "OK",
            "file_name" : cname,
            "folder" : _UPLOADS,
            "classify_tags" : ",".join(tags),
            "origianl_tags" : ",".join(clean_tags)
        }
        self.finish(json.dumps(response))

    def loadVergeText(self, content):
        cons = json.loads(content)
        return cons['Main text'], cons['Tags'] 

class Web(web.RequestHandler):
    def head(self):
        self.finish()

    @gen.coroutine
    def get(self):
        q = self.get_argument('q', None)
        if q is None:
            return

        # Fetch postings from index servers
        http = httpclient.AsyncHTTPClient()     
        responses = yield [http.fetch("http://%s/index?%s" % 
                                      (server, urllib.urlencode({'q': q}))) 
                          for server in inventory.servers['index']]
        # Flatten postings and sort by score
        postings = sorted(chain(*[json.loads(r.body)["postings"]
                                 for r in responses]),
                         key=lambda x: -x[1])

        # Batch requests to doc servers
        serverToDocIDs = defaultdict(list)
        docIDToResultIx = {}
        partition = HashPartitioner(inventory.NUM_DOC_SHARDS)
        for i in range(len(postings[:NUM_RESULTS])):
            docID = postings[i][0]
            docIDToResultIx[docID] = i
            server = self._getServerForDocID(docID, partition)
            serverToDocIDs[server].append(docID)
        responses = yield self._getDocServerFutures(q, serverToDocIDs)

        # Parse outputs and insert into sorted result array
        resultList = [None] * min(len(postings), NUM_RESULTS)
        for response in responses:
            for result in json.loads(response.body)['results']:
                resultList[docIDToResultIx[int(result['docID'])]] = result
        self.write(json.dumps({"numResults": len(resultList), "results": resultList}))
        self.finish()

    def _getDocServerFutures(self, q, serverToDocIDs):
        http = httpclient.AsyncHTTPClient()
        futures = []        
        for server, docIDs in serverToDocIDs.iteritems():
            queryString = urllib.urlencode({'ids': ",".join([str(x) for x in docIDs]), 'q': q})
            futures.append(http.fetch("http://%s/doc?%s" % (server, queryString)))
        return futures

    def _getServerForDocID(self, docID, partition):
        servers = inventory.servers['doc']
        #ix = docID % len(servers)
        ix = partition(str(docID))
        return servers[ix]  


class IndexDotHTMLAwareStaticFileHandler(web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path += 'index.html'
        return super(IndexDotHTMLAwareStaticFileHandler, self).parse_url_path(url_path)

# def makeBackend():
#     return web.Application([
#          (r"/upload", UploadHandler),
#          (r"/(.*)", IndexDotHTMLAwareStaticFileHandler, dict(path=SETTINGS['static_path']))
#          ],**SETTINGS)

# def main():
#     app = httpserver.HTTPServer(makeBackend())
#     app.add_sockets(netutil.bind_sockets(inventory.BASE_PORT))
#     logging.info("Back end listening on %d" % inventory.BASE_PORT)
#     IOLoop.current().start()

def main():
    numProcs = inventory.NUM_INDEX_SHARDS + inventory.NUM_DOC_SHARDS + 1
    taskID = process.fork_processes(numProcs, max_restarts=0)
    port = inventory.BASE_PORT + taskID
    if taskID == 0:
        app = httpserver.HTTPServer(tornado.web.Application([
                (r"/search", Web),
                (r"/upload", UploadHandler),
                (r"/(.*)", IndexDotHTMLAwareStaticFileHandler, dict(path=SETTINGS['static_path']))
            ], **SETTINGS))
        logging.info("Front end is listening on " + str(port))
    else:       
        if taskID <= inventory.NUM_INDEX_SHARDS:
            shardIx = taskID - 1
            #data = pickle.load(open("data/index%d.pkl" % (shardIx), "r"))
            inverted_path = os.path.join(os.getcwd(),"../assignment5/i_df_jobs/%d.out"  % (shardIx))
            logging.info("Inverted file path: %s" % inverted_path)
            data = pickle.load(open(inverted_path ,'r'))
            idf_path = os.path.join(os.getcwd(), "../assignment5/idf_jobs/0.out")
            logIDF = pickle.load(open(idf_path,'r'))
            app = httpserver.HTTPServer(web.Application([(r"/index", index.Index, dict(data=data, logIDF=logIDF))]))
            logging.info("Index shard %d listening on %d" % (shardIx, port))
        else:
            shardIx = taskID - inventory.NUM_INDEX_SHARDS - 1
            #data = pickle.load(open("data/doc%d.pkl" % (shardIx), "r"))
            doc_path = os.path.join(os.getcwd(),"../assignment5/df_jobs/%d.out" % (shardIx))
            logging.info("Doc Server path %s" % doc_path)
            data = pickle.load(open(doc_path, "r"))
            app = httpserver.HTTPServer(web.Application([(r"/doc", doc.Doc, dict(data=data))]))
            logging.info("Doc shard %d listening on %d" % (shardIx, port))
    app.add_sockets(netutil.bind_sockets(port))
    IOLoop.current().start()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()
