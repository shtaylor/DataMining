#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 15:13:39 2020

@author: shane

Class to perform Apriori pattern mining
"""

class Apriori():
    def __init__(self, data_file_path: str, item_sep: str = ';', 
                 rel_minsup: float = 0.01, abs_minsup: int = 0):
        self.item_sep = item_sep
        self.data_file_path = data_file_path
        self.data_file = open(self.data_file_path)
        self.data = []
        linecount = 0
        for line in self.data_file:
            self.data.append(frozenset(line.replace('\n','').split(sep=self.item_sep)))
            linecount += 1
        if abs_minsup != 0:
            self.minsup = abs_minsup
        else:
            self.minsup = int(rel_minsup * linecount)
        self.F = []
    
    def get_freq_1_itemset(self)->dict:
        counts = {}
        for line in self.data:
            for item in line:
                itemset = frozenset([item])
                if itemset in counts.keys():
                    counts[itemset] += 1
                else:
                    counts[itemset] = 1
        freq1 = {}
        for count in counts:
            if counts[count] > self.minsup:
                freq1[count] = counts[count]
        return(freq1)
        
    def get_k_subsets(self, aset: frozenset)->list:
        subset_list = []
        for element in aset:
            diff = aset.difference(frozenset([element]))
            subset_list.append(diff)
        return subset_list
    
    def generate_kplus1_itemset(self, k: int)->set:
        candidate_set = set([])
        F_keys = list(self.F[k].keys())
        for i in range(0, len(F_keys)):
            for j in range(i+1, len(F_keys)):
                candidate = F_keys[i].union(F_keys[j])
                if len(candidate) == k+2:
                    candidate_k_subsets = self.get_k_subsets(candidate)
                    candidate_is_valid = True
                    for subset in candidate_k_subsets:
                        if subset not in F_keys:
                            candidate_is_valid = False
                            break
                    if candidate_is_valid:
                        candidate_set.add(candidate)
        return(candidate_set)
        
    def derive_freq_kplus1_itemsets(self, candidate_set: set):
        counts = {}
        for candidate in candidate_set:
            for line in self.data:
                if candidate.issubset(line):
                    if candidate in counts.keys():
                        counts[candidate] += 1
                    else:
                        counts[candidate] = 1
        freq = {}
        for count in counts:
            if counts[count] > self.minsup:
                freq[count] = counts[count]
        return(freq)
        
    def run(self):
        k = 0
        self.F.append(self.get_freq_1_itemset())
        while True:
            candidate_set = self.generate_kplus1_itemset(k)
            self.F.append(self.derive_freq_kplus1_itemsets(candidate_set))
            k += 1
            if len(self.F[k]) == 0:
                return
    
    def format_output(self):
        output = []
        for k_itemset in self.F:
            for itemset in k_itemset:
                output.append("{}:{}".format(k_itemset[itemset],";".join(itemset)))
        return output
    
    def write_output(self):
        output = self.format_output()
        f = open('patterns.txt', mode='w')
        for entry in output:
            f.write('{}\n'.format(entry))
        f.close()
    