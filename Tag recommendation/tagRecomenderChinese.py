# -*- coding: utf-8 -*-
from lxml import etree
from StringIO import StringIO
import jieba
import jieba.analyse

#http://www.hanxiaogang.com/writing/parsing-evernote-export-file-enex-using-python/
p = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
def parseNoteXML(xmlFile):
    context = etree.iterparse(xmlFile, encoding='utf-8', strip_cdata=False)
    note_dict = {}
    notes = []
    for ind, (action, elem) in enumerate(context):
        text = elem.text
        if elem.tag == 'content':
            text = []
            r = etree.parse(StringIO(elem.text.encode('utf-8')), p)
            for e in r.iter():
                if e.tag == 'tag':
                    print e.text.encode('utf-8')
                try:
                    text.append(e.text)
                except:
                    print 'cannot print'
        note_dict[elem.tag] = text
        if elem.tag == "note":
            notes.append(note_dict)
            note_dict = {}
    return notes



if __name__ == '__main__':
    notes = parseNoteXML('Notes.enex')

    # note = notes[2]
    # text = note["title"]
    # tags = jieba.analyse.extract_tags(text)
    # print len(note["tag"])
    # for tag in note["tag"]:
    #     print tag.encode('utf-8')
    # print "*---------------------*"
    # print "Estimated tags:"
    # for tag in tags:
    # 	print tag.encode('utf-8')

