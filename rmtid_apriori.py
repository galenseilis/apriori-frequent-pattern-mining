#!/usr/bin/env python3
#-*- coding:utf-8 - *-

"""
This CLI tool is a Python implementation of a modification of the classic 'apriori' frequent patten mining algorithm.

GNU General Public License v3.0
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications,
which include larger works using a licensed work, under the same license.
Copyright and license notices must be preserved.
Contributors provide an express grant of patent rights.

Reference Materials:
[1] https://jiffyclub.github.io/snakeviz/
[2] http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/
[3] https://github.com/twmht/pyApriori
[4] https://github.com/marcoszh/PyApriori
"""

import argparse
from collections import Counter
from itertools import product
from time import ctime

__author__ = 'Galen Seilis'
__copyright__ = 'Copyright 2020, Assignment 1, CPSC-673-A1'
__credits__ = ['Galen Seilis', 'Fan Jiang (Instructor)']
__license__ = 'GNU General Public License v3.0'
__version__ = '0.1.0'
__maintainer__ = 'Galen Seilis'
__email__ = 'seilis@unbc.ca'
__status__ = 'School Project'

def get_db_size(file_name):
    '''
    This function gets the number of transactions
    from the transaction database by reading and
    returning only the first line of the file.

    This function is intended to be run only once
    at the beginning of a frequent pattern mining
    algorithm.

    Make sure that the first line of the transaction
    database is suitable for this purpose.

    ARGUMENTS
        file_name (str): The name of the transaction database file.

    RETURNS
        (int): Number of transactions in transaction database.
    '''
    with open(file_name) as f:
        return int(f.readline().rstrip())

def clean_line(line):
    '''
    This helper function parses a line from the
    transaction database.

    ARGUMENTS
        line (str): A line from the transaction database.
        
    RETURNS
        t_id (int): The transaction identifier.
        t_n (int): The number of items in the transaction.
        t_set (frozenset[int]): The set of items as integers in the transaction.
    '''
    t_id, t_n, t_set = line.rstrip().split('\t')
    t_id = int(t_id)
    t_n = int(t_n)
    t_set = frozenset([int(i) for i in t_set.split(' ')])
    return t_id, t_n, t_set

def first_scan(file_name, epsilon):
    '''
    This function perfoms the first database scan
    for the apriori frequent pattern mining algorithm.

    Compared to the function later_scan, first_scan will
    assume that all items are candidates while later_scan
    will assume that the candidates are provided.

    ARGUMENTS
        file_name (str): The name of the transaction database file.
        epsilon (float/int): Absolute minimum support threshold.

    RETURNS
        (dict): A count table of each item in the database.
    '''
    L1_counter = Counter()
    transactions = {}
    with open(file_name) as file:
        offset = 0
        for i, line in enumerate(file):
            if i != 0:
                t_id, t_n, t_set = clean_line(line)
                transactions[t_id] = (offset, offset + len(line))
                offset += len(line) + 1
                L1_counter += Counter(t_set)
            else:
                offset += len(line) + 1
    L1_counter = {k:v for (k,v) in L1_counter.items() if v >= epsilon}
    return L1_counter, transactions

def read_transaction(file_name, start, stop):
    '''
    This function will read a specific transaction
    from the given transaction database rather than
    reading the entire file.

    ARGUMENTS
        file_name (str): Transaction database filename.
        start (int): File byte index to start reading.
        stop (int): File byte index to stop reading.

    RETURNS
        line (str): String representation of transaction.
    '''
    file = open(file_name)
    file.seek(start)
    line = file.read(stop - start)
    file.close()
    return line

def candidate_generation(l, k):
    '''
    This function takes the previous L table
    to construct all the candidate itemsets for
    the next C table.

    ARGUMENTS
        l (dict): The previous L table.
        k (int): The size of the itemsets. Also the iteration number.

    RETURNS
        candidates (dict): A table of the candidates for the next iteration of
                           the apriori algorithm.
    '''
    candidates = {}
    for i, ki in enumerate(l.keys()):
        for j, kj in enumerate(l.keys()):
            if i < j:
                if isinstance(ki, int) and isinstance(kj, int):
                    candidates[frozenset({ki, kj})] = 0
                elif isinstance(ki, frozenset) and isinstance(ki, frozenset):
                    union = ki.union(kj)
                    if len(union) == k:
                        candidates[union] = 0
                    else:
                        continue
                else:
                    print('WARNING: Incorrect typing. Please check data input. Quitting...')
                    quit()
            else:
                continue
    return candidates

def later_scan(file_name, candidates, transactions, epsilon):
    '''
    This function perfoms later database scans
    for the apriori frequent pattern mining algorithm.

    Compared to first_scan, later_scan will take a table of
    candidates as input while first_scan will assume that all
    items are candidates.

    ARGUMENTS
        file_name (str): The name of the transaction database file.
        candidates (dict[frozenset[int]]: Dictionary of candidates for next iteration.
        transactions (dict[int:tuple[int, int]]: Dictionary of transactions still being considered.
        epsilon (float/int): Absolute minimum support threshold.

    RETURNS
        (dict): A count table of each given candidate in the database.
    '''
    l = candidates.copy()
    trans = transactions.copy()
    for t_id, (start, stop) in transactions.items():
        useful = False
        t_id, t_n, t_set = clean_line(read_transaction(file_name, start, stop))
        for candidate in candidates.keys():
            if candidate.issubset(t_set):
                useful = True
                l[candidate] += 1
        if not useful:
            del trans[t_id]
    l = {k:v for (k,v) in l.items() if v >= epsilon}
    return l, trans
    
    

def apriori(file_name, epsilon):
    '''
    This function performs the modified Apriori frequent pattern
    mining algorithm.

    ARGUMENTS
        file_name (str): The input data file name of transactions.
        epsilon (float/int): Absolute minimum support threshold.

    RETURNS
        L (dict[int:dict[frozenset[int]:int]]): Dictionary of all frequent patterns found by the algorithm.   
    '''
    print(ctime(), 'Searching for k=1 frequent patterns.')
    L1, trans = first_scan(file_name, epsilon)
    L = {1:L1}
    print(ctime(), f"RmTID found {len(L[1])} new frequent pattern(s).\n")
    k = 2
    while True:
        candidates = candidate_generation(L[k-1], k)
        if not candidates:
            break
        else:
            print(ctime(), f'Searching for k={k} frequent patterns.')
            candidates, trans = later_scan(file_name, candidates, trans, epsilon)
            if not candidates:
                print(ctime(), f"RmTID found {len(candidates)} new frequent pattern(s).\n")
                break
            else:
                print(ctime(), f"RmTID found {len(candidates)} new frequent pattern(s).\n")
                L[k] = candidates
                k += 1
    return L

def write_rules(file_out, rules):
    '''
    This function writes the discovered
    frequent patterns into a text file.

    ARGUMENTS
        file_out (str): The output file name of frequent patterns.
        rules (dict[int:dict[frozenset[int]:int]]): Dictionary of all frequent patterns found by the algorithm.

    RETURNS
        None
    '''
    with open(file_out, 'w') as file:
        count = 0
        lines = []
        for (k, ruleset) in rules.items():
            for (itemset, support) in ruleset.items():
                count += 1
                if isinstance(itemset, int):
                    itemstr = str(itemset)
                else:
                    itemstr = str(set(itemset)).replace('{', '').replace('}', '')
                line = f'{itemstr} : {support}\n'
                lines.append(line)
        file.write(f'|FPs| = {count}\n')
        print(f'|FPs| = {count}\n')
        for i, line in enumerate(lines):
            file.write(line)

if '__main__' == __name__:
    # Prepare command line parser
    parser = argparse.ArgumentParser()
    parser.description = '''A CLI that performs a modified Apriori frequent pattern learning algorithm.
    This program expects an input text file with a particular format.
    The first line of the input file should be the number of transactions in the transaction database.
    All subsequent lines are expected to have a tab-delimited format where the first column is the transaction ID,
    the second column is the number of items in the transaction, and the third column is a space-delimited set of items.
    Failure to format the input file correctly may result in errors or unexpected behaviour.'''
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--in_file", type=str, required=True, help="Input data file.")
    parser.add_argument("-o", "--out_file", type=str, default="MiningResults.txt", help="Output results file. (default='MiningResults.txt')")
    parser.add_argument("-m", "--min_supp", type=float, default=0.5, help="Minimum support threshold as a float between 0 and 1. (default=0.5)")
    args = parser.parse_args()
    
    # Check validity of CLI arguments
    assert 0 <= args.min_supp <= 1
    epsilon = args.min_supp * get_db_size(args.in_file)
    print(ctime(), 'Starting\n')
    rules = apriori(args.in_file, epsilon)
    print(ctime(), 'Writing rules to file...')
    write_rules(args.out_file, rules)
    print(ctime(), 'Finished\n')
