#!/use/bin/env python
import shlex, subprocess
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
NUM_REDUCERS = 10

def main():
    
    inverted_process_args = "python assignment4/coordinator.py --mapperPath=assignment4/inverted_index/index_mapper.py --reducerPath=assignment4/inverted_index/index_reducer.py --jobPath=assignment5/df_jobs --numReducers=%d" % NUM_REDUCERS
    logging.debug("Inverted_Server mapReduce param: %s" % inverted_process_args)
    inverted_process_args = shlex.split(inverted_process_args)
    inverted_process = subprocess.Popen(inverted_process_args)
    inverted_return_code = inverted_process.wait()
    if inverted_return_code is not 0:
        logging.error("MapReduce Inverted return code %d" % inverted_return_code)
        sys.exit(2)
    
        
if __name__ == "__main__":
    main()
    


