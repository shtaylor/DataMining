#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 13:32:44 2020
@author: Shane Taylor
"""

class ContiguousSequentialPatterns():
    def __init__(self, data_file_path: str, item_sep: str = ' ', 
                 rel_minsup: float = 0.01, abs_minsup: int = 0):
        self.item_sep = item_sep
        self.data_file = open(data_file_path)
        self.data = []
        self.data_raw = []
        linecount = 0
        
        for line in self.data_file:
            self.data.append(list(line.replace('\n','').split(sep=self.item_sep)))
            self.data_raw.append(line.replace('\n',''))
            
            linecount += 1
        if abs_minsup != 0:
            self.minsup = abs_minsup
        else:
            self.minsup = int(rel_minsup * linecount)
        self.F = []
    
    def extend_tuple(self, t: tuple, t2: tuple)->tuple:
        return t + (t2[0],)
        
    def line_contains(self, line: str, pattern: list)->bool:
        return(" ".join(pattern) in line)
    
    def get_freq_1_itemsets(self)->dict:
        candidates = set()
        for line in self.data:
            for item in line:
                candidates.add((item,0))
        counts = dict(candidates)
        counts_keys = set(counts.keys())
        for line in self.data:
            isect = counts_keys.intersection(set(line))
            for k in isect:
                counts[k] += 1
        freq = {}
        for k in counts:
            if counts[k] > self.minsup:
                freq[(k,)] = counts[k]
        return(freq)
    
    def generate_kplus1_itemsets(self, k: int)->list:
        print("generating {}-itemsets".format(k+2))
        candidate_set = set()
        keys = list(self.F[k].keys())
        for i in range(0, len(keys)):
            for j in range(0, len(keys)):
                candidate_set.add((self.extend_tuple(keys[i],keys[j]),0))
        return list(candidate_set)
    
    def derive_freq_kplsu1_itemsets(self, candidates: list)->dict:
        counts = dict(candidates)
        counts_keys = list(counts.keys())
        ck_len = len(counts_keys)
        i_print = 1
        for key in counts_keys:
            print("Testing {} of {}".format(i_print, ck_len))
            for line in self.data_raw:
                if self.line_contains(line, key):
                    counts[key]+=1
            i_print += 1
        freq = {}
        for k in counts:
            if counts[k] > self.minsup:
                freq[k] = counts[k]
        return(freq)
                    
    def format_output(self)->list:
        output = []
        for k_itemset in self.F:
            for itemset in k_itemset:
                output.append("{}:{}".format(k_itemset[itemset],";".join(itemset)))
        return output
    
    def write_output(self, output_filepath: str = 'patterns.txt'):
        output = self.format_output()
        f = open(output_filepath, mode='w')
        for entry in output:
            f.write('{}\n'.format(entry))
        f.close()
    
    def run(self):
        k = 0
        self.F.append(self.get_freq_1_itemsets())
        print("Generated frequent 1-itemsets")
        while True:
            print("k = {}".format(k+2))
            candidates = self.generate_kplus1_itemsets(k)
            self.F.append(self.derive_freq_kplsu1_itemsets(candidates))
            k += 1
            if len(self.F[k]) == 0:
                return
