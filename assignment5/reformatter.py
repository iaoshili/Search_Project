#!/usr/bin/env python

import os,sys, getopt
import logging
import shutil
import codecs
import pickle
import json
from collections import *

logging.basicConfig(level=logging.INFO)
REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "0123456789=[]\\\"\'")
WORKING_DIR = "SmallData/"

def main():
    docID_tagList = defaultdict(list)
    with open('tags.json') as tag_file:
        all_tags = json.load(tag_file)['tags']
    #logging.info(all_tags)
    numParitition = 10
    paths = ["df_jobs/", 'i_df_jobs/', 'idf_jobs/']
    for jobPath in paths:
        if os.path.exists(jobPath):
            shutil.rmtree(jobPath)
        os.makedirs(jobPath)
        docID = 0
        all_files_name = [jobPath + str(x)+".in" for x in range(numParitition)]
        contents = [ dict() for x in range(numParitition)]
        for fileName in os.listdir(WORKING_DIR):
            if "The Verge" not in fileName:
                continue
            filePath = WORKING_DIR + fileName
            with open(filePath) as data_file:   
                input_file  = file(filePath, "r")
                data = json.loads(input_file.read())
                myTags = set()
                for tag in data['Tags']:
                    tag = tag.translate(REMOVE_PUNCT_MAP)
                    if len(tag) != 0:
                        temp = tag.split(",")
                    for t in temp:
                        if t in all_tags:
                            myTags.add(t)
                myTags = list(myTags)
                docID_tagList[docID] = myTags   
                partition_index = docID % numParitition
                title = data['Title']
                bodies = data['Main text']
                page_dict = dict()
                page_dict["docID"] = str(docID)
                page_dict["title"] = unicode(title)
                page_dict["docBody"] = unicode(bodies)
                contents[partition_index][docID] = page_dict
                docID += 1
        for idx, file_name in enumerate(all_files_name):
            pickle.dump(contents[idx], open(file_name,"wb"))
            logging.info("Dump to %s", file_name)
    # with open('docTagList.json', 'w') as outfile:
    #     json.dump(docID_tagList, outfile)

    
if __name__ == "__main__":
    main()