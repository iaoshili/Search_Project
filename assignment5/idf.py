#!/use/bin/env python
import shlex, subprocess
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
NUM_REDUCERS = 10

def main():
    
    tf_idf_args = "python assignment4/coordinator.py --mapperPath=assignment4/idf_index/idf_mapper.py --reducerPath=assignment4/idf_index/idf_reducer.py --jobPath=assignment5/idf_jobs --numReducers=1" 
    logging.debug("IDF mapReduce param: %s" % tf_idf_args)
    tf_idf_args = shlex.split(tf_idf_args)
    idf_process = subprocess.Popen(tf_idf_args)
    idf_return_code = idf_process.wait()
    if idf_return_code is not 0:
        logging.error("MapReduce IDF return code %d" % idf_return_code)
        sys.exit(2)
        
if __name__ == "__main__":
    main()
    


