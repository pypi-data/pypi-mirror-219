import multiprocessing
from multiprocessing import Pool
from typing import List, Tuple


def cpu_count():
    return multiprocessing.cpu_count()


def do_parallel(func, args: List[Tuple], processes=cpu_count() // 2):
    if processes <= 1:
        processes = 1
    processes = min(max(1, processes), cpu_count())
    with Pool(processes=processes) as pool:
        results = pool.starmap(func, args)
        return results
