#!/usr/bin/env python3
"""
barplot - Varianty vs tydny
"""

import csv
from dataclasses import dataclass
from matplotlib.font_manager import FontProperties  
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from pprint import pprint


src1 = "/Users/hanamedova/Documents/COG/week34/datafreeze-2021-08-27_12_weeks_good.tsv"
src2 = "/Users/hanamedova/Documents/COG/week34/datafreeze-2021-08-27_12_weeks_good.nextclade.1.2.3.tsv"

src3 = "/Users/hanamedova/Documents/COG/report/input/hmedova/statistics_week34.tsv"

def join_tables(src1, src2):
    d1 = {}
    d2 = {}
    merged = {}
    with open(src1, newline ='') as csv1:
        f1 = csv.reader(csv1, delimiter = "\t") 
        for row in f1:
            d1[row[0]] = row[-1]
    with open(src2, newline ='') as csv2:
        f2 = csv.reader(csv2, delimiter = "\t") 
        for row in f2:
            d2[row[0]] = row[15]
    for k, v in d1.items():
        merged.setdefault(k, [])  #check for duplicates
        #print(merged[k].append(v))
        merged[k].append(v)
        #print(merged.setdefault(k, []))
    for k, v in d2.items():
        merged.setdefault(k, [])
        merged[k].append(v)
    print(len(list(merged.values())))
    return sorted(list(merged.values())) 
    
data1 = join_tables(src1, src2)
data1[1:10]

def open_total_sequenced(src3):
    with open(src3, newline ='') as csv3:
        f3 = csv.reader(csv3, delimiter = "\t") 
        d3 = {}
        for row in f3:
            d3[row[0]] = row[1]
        a = list(reversed(list(d3.values())[1:]))
        b = [int(i) for i in a[:-1] ]  #pozor na 34. tyden
        print(b)
        print(len(b))
    return b
    
total_sequenced_samples = open_total_sequenced(src3)
 

def count_frequencies_a222v(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "A222V" in sublist[1]]   #hashtable type "list" for the Counter
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

def count_frequencies_d253a(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "D253A" in sublist[1]]
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

def count_frequencies_d979e(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "D979E" in sublist[1]]
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

def count_frequencies_trio(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "A222V" and "D253A" and "D979E" in sublist[1]]   #hashtable type "list" for the Counter
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

def count_frequencies_kvartet(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "A222V" and "D253A" and "D979E" and "T95I" in sublist[1]]   #hashtable type "list" for the Counter
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

def count_frequencies_95(data):
    "in:src files, out: Counter(dictionary), keys: weeks, values: counts"
    list_of_weeks = [ sublist[0] for sublist in data[:-2] if "T95I" in sublist[1]]   #hashtable type "list" for the Counter
    d = dict(Counter(list_of_weeks)) 
    print(d)
    print(len(d))
    return d

data_trio = count_frequencies_trio(data1)
# {'2021-24': 7, '2021-25': 48, '2021-26': 104, '2021-27': 141, '2021-28': 139, '2021-29': 42, '2021-30': 61, '2021-31': 52, '2021-32': 20, '2021-33': 4}
data_kvartet = count_frequencies_kvartet(data1)
# {'2021-23': 2, '2021-25': 6, '2021-26': 12, '2021-27': 33, '2021-28': 43, '2021-29': 22, '2021-30': 30, '2021-31': 51, '2021-32': 38, '2021-33': 6}
# data_duo = count_frequencies_duo(data1)
mut_a222v = count_frequencies_a222v(data1)
mut_d253a = count_frequencies_d253a(data1)
mut_d979e = count_frequencies_d979e(data1)
mut_T95I = count_frequencies_95(data1)
# {'2021-23': 2, '2021-25': 6, '2021-26': 12, '2021-27': 33, '2021-28': 43, '2021-29': 22, '2021-30': 30, '2021-31': 51, '2021-32': 38, '2021-33': 6}

len(data_trio)
len(mut_a222v)
len(mut_d253a)
len(mut_d979e)

def extract_values(data):
   return [ values  for key, values in data.items()] 

data_trio_lst = [0] + extract_values(data_trio)

ratio = [ f'{data_trio_lst[i]/total_sequenced_samples[i]:.2f}' for i in range(len(data_trio_lst))] 
# ['0.00', '0.09', '0.41', '0.53', '0.57', '0.56', '0.31', '0.42', '0.24', '0.20', '0.33']
sum(data_trio_lst)


def create_graph():
    '''
    Where data looks like:
    {'2021-24': 7, '2021-25': 48, '2021-26': 104, '2021-27': 141, '2021-28': 139, '2021-29': 42, '2021-30': 61, '2021-31': 52, '2021-32': 20, '2021-33': 4}
    '''
    fig, ax = plt.subplots()
    #fig, ax = plt.subplots(figsize=(15, 6))
    width = 0.15
    
    #tick labels - the week numbers
    labels = [key for key, values in mut_a222v.items()]

    #data for each plot
    data_mut_a222v = extract_values(mut_a222v)
    data_mut_d253a = [0] + extract_values(mut_d253a)
    data_mut_d979e = [0] + extract_values(mut_d979e)

    #x-axis
    x1 = np.arange(len(labels))
    x2 = [i + width for i in x1 ]
    x3 = [i + width for i in x2 ]
    x4 = [i + width for i in x3 ]

    #plot the barplots
    ax.bar(x1, total_sequenced_samples, width, color = 'black', edgecolor = "none", label = "celkový počet")
    ax.bar(x2, data_mut_a222v, width, color = 'r', edgecolor = "none", label = "S:A222V")
    ax.bar(x3, data_mut_d253a, width, color = 'w', edgecolor = "black", label = "S:D253A")
    ax.bar(x4, data_mut_d979e, width, color = 'blue', edgecolor = "none", label = "S:D979E")
  
    #plt.show()

    ax.legend(ncol=1, loc="upper right", frameon=False, prop={'size':12}).draw_frame(False)
    ax.set()
    ax.set_ylabel(ylabel="Počet vzorků", fontsize = 12, weight = 'heavy')
    ax.set_xlabel(xlabel="Týden v roce", fontsize =12, weight = 'heavy' )
    ax.set_xticks([ i + width for i in range(11) ])
    ax.set_xticklabels(labels)
    #ax.set_xlim(-1,11)
    #ax.set_ylim(0,250)
    #ax.grid(b = 0)
    fig.tight_layout()
    plt.show()
    #plt.savefig('/Users/hanamedova/Documents/COG/report/input/hmedova/AY_CZ_counts.png', dpi = 300)

create_graph()
