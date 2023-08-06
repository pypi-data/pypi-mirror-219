
# SuperFastPython.com
# load many files concurrently with processes and threads in batch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from cffi import FFI
from tqdm import tqdm
import time
from threading import Thread

# USAGE EXAMPLE:
# io_bound(thread_func, iterator, args)
# thread_func:define the task function to run parallel. Ie: read_files,days_trading_from_to
# iteration: single iteration items of parallel task
# args: commom task variables 

# thread_func EXAMPLES

# IO BOUND EXAMPLE
# def read_files(iteration, args):
#     fileid = iteration[0]    
#     file_list = args[0]
#     fpath = file_list[fileid]
#     df = pd.read_csv(fpath)
#     return [df]

# CPU BOUND EXAMPLE
# def days_trading_from_to(iteration, args):
#     cal = iteration[0]
#     start = iteration[1]
#     end = iteration[2]
#     calendars = args[0]
#     idx = (calendars[cal]>=start) & ((calendars[cal]<=end))
#     return [np.count_nonzero(idx)]


# load all files in a directory into memory
def io_bound(thread_func, iterator, args, maxproc=None, maxthreads=10):
    results = []    
    # determine chunksize
    niterator = len(iterator)
    if niterator>0:
        n_workers = multiprocessing.cpu_count() - 2
        n_workers = min(n_workers,niterator)
        if not maxproc is None:
            n_workers = min(n_workers,maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:        
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(io_bound_process, thread_func, proc_iterator, args, maxthreads)
                futures.append(future)
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]                
    return results

# return the contents of many files
def io_bound_process(thread_func, proc_iterator, args, maxthreads):
    results = []
    # create a thread pool
    nthreads = len(proc_iterator)
    nthreads = min(nthreads,maxthreads)
    if nthreads>0:
        with ThreadPoolExecutor(nthreads) as exe:
            # load files
            futures = [exe.submit(thread_func, iteration, args) for iteration in proc_iterator]
            # collect data
            for future in futures:
                res = future.result()
                results = [*results, *res]
        
    return results
 

def cpu_bound(thread_func, iterator, args, maxproc = None):
    results = []    
    # determine chunksize
    niterator = len(iterator)
    if niterator>0:
        n_workers = multiprocessing.cpu_count() - 2    
        n_workers = min(n_workers,niterator)
        if not maxproc is None:
            n_workers = min(n_workers,maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:        
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(cpu_bound_process, thread_func, proc_iterator, args)
                futures.append(future)                                 
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]    
    return results


# return the contents of many files
def cpu_bound_process(thread_func, proc_iterator, args):
    results = []
    for iteration in proc_iterator:
        res = thread_func(iteration, args)
        results = [*results, *res]              
    return results

def progressbar_thread(progress,niterations):
    pbar = tqdm(total=niterations,desc='Running multi proc...')
    while True:        
        pbar.update(progress - pbar.n)
        if progress >= niterations:
            break
        time.sleep(0.2)
        
        