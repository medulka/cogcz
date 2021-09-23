#!/usr/bin/env python3.8
"""
titulek:    Jinja2 templating
vysledek:   vysledne html
autor:      medulka
verze:      week24
datum:      od 21. kvetna 2021 a dale
"""

import datetime
import csv
from re import A
from turtle import screensize
from jinja2 import DictLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape, Template
from weasyprint import HTML
import shutil
import os
import base64

#update regularly
#change in the reporting since 16.7.2021 (week28) - only last 12 months
DF_DATE = "10.9.2021"
ACTUAL_SAMPLE_SIZE = "1 739"
LINEAGE_COUNTS = "24"
WEEK = "36"
STARTING_WEEK = "25"
SEQUENCED_RATIO = "12,1"
MUTATIONS_COUNT = "1 400"
NOW=datetime.datetime.now().strftime('%d. %m. %Y' )
VOC = ['B.1.351', 'P.1', 'B.1.617.2', "AY.1", "AY.2", "AY.4", "AY.5", "AY.5.2", "AY.6", "AY.7.2", "AY.9", "AY.12", "AY.16", "AY.20", "AY.21" ]
VOI = ['B.1.620', 'B.1.621', "C.37" ]
# uprav tyden v range()

#vytvoreni prostredi
env = Environment(
    loader = FileSystemLoader('.'),
    autoescape = select_autoescape(['html']),
    extensions=['jinja2.ext.debug']
    )

#seznam kapitol - obsah
def precti_seznam_kapitol(filename):
    seznam_kap = []  
    with open(filename, newline = '') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            seznam_kap.append(row)
    return seznam_kap 

#vytvareni tabulek
def input_table_tsv(src_file):
    "a text file transformation to an item"
    with open(src_file) as g:
        lst = []
        for line in g:
            items = line.split('\t')
            items = [item.strip("\"").strip("\n").strip(" ") for item in items]
            lst.append(items)    
        for line in lst:
            for item in line:
                item.replace('NA','0')
        return lst 
    
def prejmenovani_hlavicky(hlavicka, zkratky_regionu):
    "in: tabulka, out: prvni radek s prejmenovanymi sloupci"
    print('-----------')
    print(zkratky_regionu)
    print(hlavicka)
    list_zkratek = [] 
    for item in hlavicka:
        for key in zkratky_regionu:
            if key in item:
                list_zkratek.append(zkratky_regionu[key]) 
                break
        else:   
            print(item," - nazev nenalezen v hashovaci tabulce")    
    return list_zkratek

def is_non_zero_line(line):
    "in: a line, boolean value"
    summ = sum([ float(item) for item in line[-11:-2] ])
    return summ > 0.0

def sort_time_table(tbl):
    "in: slices of the table, only rows with mutations, out: table"
    tbl.sort(key=lambda x:float(x[-1]), reverse=True)
    return tbl

def open_hash_table(filename):
    hash_table = {}   
    with open(filename, newline = '') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            key = row[0]
            value = row[1]
            hash_table[key] = value
        return hash_table   


def color_class(item,line):
    "in: item of a sublist, out: str"
    max_item = max([int(float(i)) for i in line if i != '' and i != 'NA'])
    color_class = ""
    if item != "" and item != 'NA':
        ratio = int(float(item))/max_item
        for level in [80,60,40,20]:
            if ratio >= level/100:
                color_class = 'level_%02d' % level
                break
        else:
            color_class = 'level_00'
    print(color_class)
    return color_class


def main():
    #the templates to be used    
    seznam_kapitol = precti_seznam_kapitol("template/seznam_kapitol.csv")

    #nacteni hashovaci tabulky
    zkratky_regionu = open_hash_table("template/hash_table_regions.csv")

    #copy css
    shutil.copyfile("template/report.css", "output/report.css")

    #nacteni template
    template = env.get_template("template/template_main.html")

    #kopirovani obrazku z adresare input do output
    #vlozeni obrazku do html - konvertovani obrazku do data url formatu
    obrazky = []
    def obrazek(tmpl, src):
        "input: cesta, jmeno obrazku, outpt: zkopirovany obrazek do adresare output"
        tdir = os.path.split(tmpl)[0]
        obrazky.append(os.path.join(tdir, src))
        src_file = os.path.join(tdir, src)
        if os.path.getsize(src_file) > 1500000:
            target_file = os.path.join("output", src)
            shutil.copyfile(src_file, target_file)
            return src
        else:
            with open(src_file, "rb") as obr:
                encoded_obr = base64.b64encode(obr.read()).decode("utf-8")       
            if src.lower().endswith('.png'):
                prefix = "data:image/png;base64,"
            elif src.lower().endswith('.svg'):        
                prefix = "data:image/svg+xml;base64,"
            else:
                raise RuntimeError("neznama pripona obrazku")
            return prefix + encoded_obr

    #zalozeni vychoziho souboru - main.html
    with open("output/main.html","w") as f_result:
        content = template.render(
            NOW = NOW, 
            DF_DATE = DF_DATE,
            ACTUAL_SAMPLE_SIZE = ACTUAL_SAMPLE_SIZE,
            VOC = VOC,
            VOI = VOI,
            MUTATIONS_COUNT = MUTATIONS_COUNT,
            WEEK = WEEK,
            LINEAGE_COUNTS = LINEAGE_COUNTS,
            SEQUENCED_RATIO = SEQUENCED_RATIO,
            STARTING_WEEK = STARTING_WEEK,
            seznam_kapitol = seznam_kapitol, 
            enumerate = enumerate,  
            float = float, 
            int = int,
            str = str,
            sort_time_table = sort_time_table,
            len = len,
            input_table_tsv = input_table_tsv,
            is_non_zero_line = is_non_zero_line, 
            obrazek = obrazek,
            color_class = color_class,
            prejmenovani_hlavicky = prejmenovani_hlavicky,
            zkratky_regionu = zkratky_regionu,    
        )
        f_result.write(content)     
 
        
        
    #print(f"Obrazky: {' '.join(obrazky)}")
    HTML("output/main.html").write_pdf("output/report.pdf")

if __name__ == '__main__':
    main()
