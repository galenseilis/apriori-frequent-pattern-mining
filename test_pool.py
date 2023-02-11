from multiprocessing import Pool
from itertools import islice
from collections import ChainMap

def partition_dict(d, n=10000):
    it = iter(d)
    for i in range(0, len(d), n):
        yield {k:d[k] for k in islice(it, n)}

def func2(d):
    return {i:i *j for i,j in d}

output = {i:i+1 for i in range(40)}
with Pool(4) as p:
    items = list(output.items())
    chunksize = 4
    chunks = [items[i:i + chunksize ] for i in range(0, len(items), chunksize)]
    reduced_values= p.map(func2, chunks)
    print(dict(ChainMap(*reduced_values)))
