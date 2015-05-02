import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import inventory
import logging
import os, uuid
import json
import SampleClassifier

_UPLOADS = "uploads/"
SETTINGS = {"static_path": "./webapp"}
REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "0123456789=[]\\\"\'")

class UploadHandler(web.RequestHandler):

    def post(self):
        #logging.info(self.request.files)
        fileinfo = self.request.files['file'][0]
        #logging.info("fileinfo is %s" % fileinfo)
        fname = fileinfo['filename']
        ftype = fileinfo['content_type']
        logging.info("Upload File Name is %s" % fname)
        logging.info("Upload File Type is %s" % ftype)
        logging.info("File size is %d" % len(fileinfo['body']))
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        logging.info(_UPLOADS)
        fh = open(_UPLOADS + cname, 'w')
        fh.write(fileinfo['body'])
        textBody, oriTags = self.loadVergeText(fileinfo['body'])
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
            "classify_tags" : tags,
            "origianl_tags" : ",".join(clean_tags)
        }
        self.finish(json.dumps(response))

    def loadVergeText(self, content):
        cons = json.loads(content)
        return cons['Main text'], cons['Tags'] 

class IndexDotHTMLAwareStaticFileHandler(web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path += 'index.html'
        return super(IndexDotHTMLAwareStaticFileHandler, self).parse_url_path(url_path)

def makeBackend():
    return web.Application([
         (r"/upload", UploadHandler),
         (r"/(.*)", IndexDotHTMLAwareStaticFileHandler, dict(path=SETTINGS['static_path']))
         ],**SETTINGS)

def main():
    app = httpserver.HTTPServer(makeBackend())
    app.add_sockets(netutil.bind_sockets(inventory.BASE_PORT))
    logging.info("Back end listening on %d" % inventory.BASE_PORT)
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()
