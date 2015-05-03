#!/use/bin/env python
import shlex, subprocess
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
NUM_REDUCERS = 10

def main():
    doc_process_args = "python assignment4/coordinator.py --mapperPath=assignment4/document_store/doc_mapper.py --reducerPath=assignment4/document_store/doc_reducer.py --jobPath=assignment5/i_df_jobs --numReducers=%d" % NUM_REDUCERS
    logging.debug("Doc_Server mapReduce param: %s" % doc_process_args)
    doc_process_args = shlex.split(doc_process_args)    
    doc_process = subprocess.Popen(doc_process_args)
    doc_return_code = doc_process.wait()
    if doc_return_code is not 0:
        logging.error("MapReduce Doc return code %d" % doc_return_code)
        sys.exit(2)
        
if __name__ == "__main__":
    main()
    


