from subprocess import call
from timeit import timeit
import numpy as np

def testit(script, data, minconf, n=3):
    results = []
    for i in range(n):
        results.append(timeit(f"call('python3 {script} -i {data} -m {minconf} -o FPs_{script.replace('.py', '')}_{data.replace('.txt', '')}_{minconf}.txt', shell=True)", globals={'call':call}, number=1))
    return results

data_files = ['retail.txt']
conf_ranges = [(0.001, 0.01)]
programs = ['p_rmtid_apriori.py', 'rmtid_apriori.py', 'apriori.py']

for file, (start, stop) in zip(data_files, conf_ranges):
    for MS in np.arange(start, stop, (stop - start) / 10)[::-1]:
        for program in programs:
            print(f'\nTESTING {file} at min_conf={MS} using {program}...\n')
            for result in testit(program, file, minconf=MS):
                with open('performance_results.csv', 'a') as f:
                    f.write(f'{program},{file},{MS},{result}\n')
