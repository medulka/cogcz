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
DF_DATE = "6.1.2023"
ACTUAL_SAMPLE_SIZE = "3 437"
LINEAGE_COUNTS = "130"
WEEK = "1"
STARTING_WEEK = "42"
SEQUENCED_RATIO = "2,94"
MUTATIONS_COUNT = "2 000"
MUTATIONS_COUNT_SPIKE = "310"
NOW=datetime.datetime.now().strftime('%d. %m. %Y' )
VOC = ["B.1.1.529", "BA.2","BA.2.1", "BA.2.12.1", "BA.2.13", "BA.2.15", "BA.2.17", "BA.2.22", "BA.2.3", "BA.2.3.2", "BA.2.3.9", "BA.2.3.11", "BA.2.3.16", "BA.2.3.17", "BA.2.3.20", "BA.2.36", "BA.2.37", "BA.2.38", "BA.2.38.1", "BA.2.4",  "BA.2.40.1", "BA.2.41", "BA.2.44", "BA.2.45", "BA.2.46", "BA.2.47", "BA.2.48", "BA.2.5", "BA.2.5.1", "BA.2.51", "BA.2.5.6", "BA.2.50", "BA.2.52", "BA.2.53", "BA.2.54", "BA.2.56", "BA.2.6", "BA.2.65", "BA.2.67", "BA.2.7", "BA.2.70", "BA.2.71", "BA.2.72", "BA.2.75.2", "BA.2.75.5", "BA.2.76", "BA.2.77", "BA.2.8", "BA.2.9", "BA.2.9.2", "BA.2.9.3", "BA.2.9.4", "BA.2.9.5", "BA.2.10", "BA.2.10.1", "BA.2.11", "BA.2.12", "BA.2.14", "BA.2.18", "BA.5.2.22", "BA.2.23", "BA.2.25", "BA.2.25.1", "BA.2.27", "BA.2.29", "BA.2.32", "BA.4", "BA.4.1", "BA.4.1.1", "BA.4.1.4", "BA.4.1.5", "BA.4.1.8", "BA.4.4", "BA.4.5", "BA.4.6", "BA.4.6.4", "BA.4.6.5", "BA.4.7", "BA.5", "BA.5.1", "BA.5.1.10", "BA.5.1.1", "BA.5.1.2", "BA.5.1.3", "BA.5.1.4", "BA.5.1.5", "BA.5.1.9", "BA.5.1.12", "BA.5.1.17", "BA.5.1.18", "BA.5.1.19", "BA.5.1.21", "BA.5.1.22", "BA.5.1.23", "BA.5.1.24", "BA.5.1.25", "BA.5.1.26", "BA.5.1.30", "BA.5.2", "BA.5.2.1", "BA.5.2.2", "BA.5.2.3", "BA.5.2.4", "BA.5.2.6", "BA.5.2.7", "BA.5.2.8", "BA.5.2.9", "BA.5.2.12", "BA.5.2.13", "BA.5.2.16", "BA.5.2.18", "BA.5.2.19", "BA.5.2.20", "BA.5.2.21", "BA.5.2.24", "BA.5.2.25", "BA.5.2.26", "BA.5.2.27", "BA.5.2.28", "BA.5.2.30", "BA.5.2.31", "BA.5.2.32", "BA.5.2.33", "BA.5.2.34", "BA.5.2.35", "BA.5.3.1", "BA.5.3.2",  "BA.5.3.3", "BA.5.3.4", "BA.4.2", "BA.5.2.44", "BA.4.1.9", "BA.4.6.1", "BA.5.3", "BA.5.5", "BA.5.5.1", "BA.5.5.3", "BA.5.6", "BA.5.6.1", "BA.5.6.4", "BA.5.8", "BA.5.9", "BA.5.10", "BE.1", "BE.1.1", "BE.1.1.1", "BE.1.1.2", "BE.1.2", "BE.1.3", "BE.1.4", "BE.3", "BE.4", "BE.6", "BF.1", "BF.1.1","BF.2", "BF.3", "BF.4", "BF.5", "BF.6", "BF.7", "BF.7.3", "BF.7.4", "BF.7.5","BF.7.5.1", "BF.7.6", "BF.7.8", "BF.8", "BF.10", "BF.11", "BF.11.1", "BF.11.3", "BF.12", "BF.13", "BF.14", "BF.15", "BF.17", "BF.19", "BF.20", "BF.21", "BF.23", "BF.25", "BF.26", "BF.27", "BF.28", "BF.29", "BG.2", "BG.5", "BK.1", "BL.1", "BL.2", "BM.1.1", "BM.1.1.1", "BN.1.1", "BM.1.1.3", "BN.1.1.1", "BN.1.2", "BN.1.3","BN.1.3.1", "BN.1.4", "BN.1.5", "BN.6", "BV.1", "BV.2", "BT.2", "BQ.1.1", "BQ.1.10", "BQ.1.11", "BQ.1.18", "BQ.1.23", "BQ.1.1.1","BQ.1.1.3", "BQ.1.1.12", "BQ.1.1.13", "BQ.1.1.27", "BQ.1.1.4", "BQ.1.1.5", "BQ.1.1.7","BQ.1.22", "BQ.1.1.15", "BQ.1.1.18", "BQ.1.2", "BQ.1.5","BQ.1.13.1","BQ.1.19","BQ.1.8", "BR.1", "BY.1", "BY.1.2", "CA.7","CC.1", "CG.1", "CK.1", "CK.2.1", "CK.2.1.1", "CL.1", "CN.1", "CP.1", "CP.3", "CR.1", "CV.1", "DF.1", "DG.1"]
VOI = ["BA.2.75","BQ.1", "XBB", "XBB.1.5" ]
# uprav tyden v range()
#VUM=BA.2.3.20, BF.7, XBC, BN.1, CH.1.1 a XAY
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
    summ = sum([ float(item) for item in line[-10:-2] ])
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
