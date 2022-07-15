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
DF_DATE = "17.06.2022"
ACTUAL_SAMPLE_SIZE = "3 874"
LINEAGE_COUNTS = "80"
WEEK = "26"
STARTING_WEEK = "15"
SEQUENCED_RATIO = "5.7"
MUTATIONS_COUNT = "3 000"
MUTATIONS_COUNT_SPIKE = "350"
NOW=datetime.datetime.now().strftime('%d. %m. %Y' )
VOC = ['B.1.351',"B.1.1.529", 'P.1', 'B.1.617.2','B.1.1.7',"B.1.351.2", "B.1.351.5", "BA.1.1", "BA.1.1.2", "BA.1.1.1", "BA.1.1.4", "BA.1.1.7", "BA.1.1.10","BA.1.1.11", "BA.1.1.12", "BA.1.1.13", "BA.1.1.14", "BA.1.1.15","BA.1.1.16","BA.1.1.16.2","BA.1.1.18",  "BA.1", "BA.1.4", "BA.1.5", "BA.1.6", "BA.1.7", "BA.1.8", "BA.1.10", "BA.1.12", "BA.1.13", "BA.1.13.1", "BA.1.14", "BA.1.15", "BA.1.15.1","BA.1.16", "BA.1.16.2",  "BA.1.17", "BA.1.17.2","BA.1.18", "BA.1.19", "BA.1.20", "BA.1.21","BA.1.21.1", "BA.2","BA.2.1", "BA.2.12.1", "BA.2.13", "BA.2.15", "BA.2.17", "BA.2.22", "BA.2.3", "BA.2.3.2", "BA.2.36", "BA.2.37", "BA.2.38","BA.2.4", "BA.2.41", "BA.2.5", "BA.2.6", "BA.2.7", "BA.2.8", "BA.2.9", "BA.2.9.2",  "BA.2.10","BA.2.10.1", "BA.2.11", "BA.2.12", "BA.2.14", "BA.2.18", "BA.2.23", "BA.2.25", "BA.2.25.1", "BA.2.27", "BA.2.29", "BA.2.32", "BA.3", "BA.4", "BA.5"]
VOI = ['B.1.620', 'B.1.621', "C.37","BA.2.75" ]
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
    max_item = max([float(i) for i in line if i != '' and i != 'NA'])
    color_class = ""
    if item != "" and item != 'NA':
        ratio = float(item)/max_item
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
            MUTATIONS_COUNT_SPIKE = MUTATIONS_COUNT_SPIKE,
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
