#!/usr/bin/env python3
"""
barplot - Varianty vs tydny
"""

import csv
from dataclasses import dataclass  
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pprint import pprint
# sns.set_theme(style="whitegrid")

src1 = "/Users/hanamedova/Documents/COG/week32/datafreeze-2021-08-13_12_weeks_good.pangolin-3.1.11-pangoLEARN-2021-08-09.csv"
src2 = "/Users/hanamedova/Documents/COG/week32/datafreeze-2021-08-13_12_weeks_good.tsv"

def join_tables(src1, src2):
    d1 = {}
    d2 = {}
    merged = {}
    with open(src1, newline ='') as csv1:
        f1 = csv.reader(csv1, delimiter = ",") 
        for row in f1:
            d1[row[0]] = row[1]
    with open(src2, newline ='') as csv2:
        f2 = csv.reader(csv2, delimiter = "\t") 
        for row in f2:
            d2[row[0]] = row[-1]
    for k, v in d1.items():
        merged.setdefault(k, [])  #check for duplicates
        #print(merged[k].append(v))
        merged[k].append(v)
        #print(merged.setdefault(k, []))
    for k, v in d2.items():
        merged.setdefault(k, [])
        merged[k].append(v)
    print (len(list(merged.values())))
    return list(merged.values()) 
    
data = join_tables(src1, src2)

def counts_lineage(src1, src2):
    "in:src files, out: Counter(dictionary), keys: lineage, weeks, values: counts"
    data_lineage = join_tables(src1, src2)
    list_of_tuples = [ (sublist[0],sublist[1]) for sublist in data[1:-1] ]   #hashtable type "list" for the Counter
    d = dict(Counter(list_of_tuples))  
    return { k:v for k,v in d.items() if v > 2 and k != ""}   #values filter
     
pprint(data)
data2 = counts_lineage(src1,src2)

k = list(set(data2.keys()))
unique_lineages = sorted(set(k[i][0] for i in range(len(k))))
unique_weeks = sorted(set(k[i][1] for i in range(len(k))))
len(unique_weeks)
len(unique_lineages)

def adding_zeros(data):
    k = list(set(data.keys()))
    unique_lineages = sorted(set(k[i][0] for i in range(len(k))))
    unique_weeks = sorted(set(k[i][1] for i in range(len(k))))
    l = []
    for lineage in unique_lineages:
        for week in unique_weeks:
            l.append((lineage,week))
    l2 = []
    for tpl in l:
        if tpl in data2.keys():
            l2.append( (tpl[0],tpl[1],data2[tpl]) )
        else:
            l2.append( (tpl[0],tpl[1],0) )
    sorted(l2)
    return l2

pprint(data2)
data3 = adding_zeros(data2)
len(data3)

def reordered_dict(data):
    "in: lst of tuples, values: out: dict, key - lineage, values - counts in time"
    d = {}
    for item in data:
        k, v1, v2 = item
        d.setdefault(k, [])
        d[k].append(v2)
    return d

data4 = reordered_dict(data3)


def add_color_code(item):
    "in: lst of lineages, labels of the graph, out: dictionary value"
    d = {}
    with open("/Users/hanamedova/Documents/COG/report/input/hmedova/color_pallette.csv", newline='') as f3:
        pallette = csv.reader(f3, delimiter = ";")
        for line in pallette:
            d[line[0]] = line[1]
    for key,value in d.items():
        if item == key:
            return value

x = add_color_code("B.1.351")


def create_graph(labels, data):
    '''
    Where data looks like:
    {'AL.1': [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
     'AY.1': [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
     ...}
    '''
    f, ax = plt.subplots(figsize=(11, 6))
    width = 0.35
    heights = None
    for key, values in data.items():
        if heights is None:
            heights = [0 for v in values]
        assert len(heights) == len(values)

        ax.bar(labels, values, width, bottom=heights, label=key, color = add_color_code(key))

        for n, v in enumerate(values):
            heights[n] += v

    ax.legend(ncol=1, loc="upper right", frameon=True, prop={'size':12}).draw_frame(False)
    ax.set()
    ax.set_ylabel(ylabel="Počet záchytů", fontsize = 12)
    ax.set_xlabel(xlabel="Týden v roce", fontsize =12)
    ax.set_xlim(-1,11)
    ax.set_ylim(0,250)
    ax.grid(b = 0)

    #plt.show()
    plt.savefig('/Users/hanamedova/Documents/COG/report/input/hmedova/plot.png', dpi = 300)

create_graph(unique_weeks, data4)

