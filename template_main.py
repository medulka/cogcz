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
DF_DATE = "25.03.2022"
ACTUAL_SAMPLE_SIZE = "9 588"
LINEAGE_COUNTS = "57"
WEEK = "12"
STARTING_WEEK = "1"
SEQUENCED_RATIO = "1.0"
MUTATIONS_COUNT = "4 300"
NOW=datetime.datetime.now().strftime('%d. %m. %Y' )
VOC = ['B.1.351',"B.1.1.529", 'P.1', 'B.1.617.2','B.1.1.7',"B.1.351.2", "B.1.351.5", "BA.1.1", "BA.1", "BA.1.4", "BA.1.5", "BA.1.6", "BA.1.7", "BA.1.8", "BA.1.10", "BA.1.12", "BA.1.13", "BA.1.13.1", "BA.1.14", "BA.1.15", "BA.1.15.1", "BA.2", "BA.3",  "AY.1", "AY.2", "AY.3", "AY.4", "AY.4.1", "AY.4.2", "AY.4.2.1", "AY.4.2.2", "AY.4.2.3", "AY.4.3", "AY.4.13", "AY.4.4","AY.4.5", "AY.4.6", "AY.4.7", "AY.4.9", "AY.5", "AY.5.2", "AY.5.4", "AY.6","AY.7","AY.7.1", "AY.7.2", "AY.9","AY.9.1", "AY.9.2", "AY.10", "AY.11", "AY.12", "AY.16", "AY.20", "AY.20.1", "AY.21", "AY.23","AY.23.1", "AY.25", "AY.25.1", "AY.26","AY.27", "AY.31", "AY.32", "AY.33", "AY.34", "AY.35","AY.36", "AY.37", "AY.38", "AY.39", "AY.39.1", "AY.40", "AY.41","AY.42", "AY.43", "AY.43.2", "AY.43.3", "AY.43.4", "AY.43.6", "AY.43.7", "AY.43.8", "AY.43.9", "AY.44", "AY.45", "AY.46", "AY.46.1", "AY.46.5", "AY.46.6","AY.46.2", "AY.46.6", "AY.47", "AY.51", "AY.60", "AY.61", "AY.66", "AY.68", "AY.71", "AY.74", "AY.79", "AY.84", "AY.91", "AY.94", "AY.95", "AY.96", "AY.98", "AY.98.1", "AY.100", "AY.102", "AY.103", "AY.106", "AY.110", "AY.111", "AY.112", "AY.113", "AY.116", "AY.117", "AY.118", "AY.119", "AY.120", "AY.121", "AY.121.1", "AY.122", "AY.122.1", "AY.123", "AY.124", "AY.125", "AY.126", "AY.127", "AY.129"]
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
