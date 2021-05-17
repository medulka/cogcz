#!/usr/bin/env python3.8
"""
titulek:    Jinja2 templating
vysledek:   vysledne html
autor:      medulka
verze:      week18
datum:      od 11. kvetna 2021 a dale
"""

import datetime
import csv
from jinja2 import Environment, PackageLoader, select_autoescape, Template
from weasyprint import HTML
import os

#vytvoreni prostredi
env = Environment(
    loader = PackageLoader('__main__', '.'),
    autoescape = select_autoescape(['html'])
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
def input_table(src_file):
    "a text file transformation to an item"
    with open(src_file) as g:
        lst = []
        for line in g:
            items = line.split('\t')
            items = [item.strip("\"").strip("\n") for item in items]
            lst.append(items)
        del(lst[0])    
    return lst

# tab3 = input_table("/Users/hanamedova/Documents/COG/week18/template/input/kolarmi/tab3.tsv")
# tab4 = input_table("/Users/hanamedova/Documents/COG/week18/template/input/kolarmi/tab4.tsv")
# tab5 = input_table("/Users/hanamedova/Documents/COG/week18/template/input/kolarmi/tab5.tsv")
# tab6 = input_table("/Users/hanamedova/Documents/COG/week18/template/input/kolarmi/tab6.tsv")

def main():
    #datum a pocitani tydnu
    now=datetime.datetime.now()
    now = now.strftime('%d. %m. %Y' )
    #week = datetime.datetime.isocalendar(now)  - nefunguje

    #copy css
    os.system("cp template/report.css output/report.css")

    #copy input - obrazku pro tvorbu html
    #os.system("cp ...")

    seznam_kapitol = precti_seznam_kapitol("template/seznam_kapitol.csv")

    #nacteni template
    template = env.get_template("template/template_main.html")

    #zalozeni vychoziho souboru - main.html
    with open("output/main.html","w") as f_result:
        # a jdeme na to!
        content = template.render(
            seznam_kapitol = seznam_kapitol, 
            now = now, 
            enumerate = enumerate,  
            float = float, 
            input_table = input_table 
        )
        f_result.write(content)  #week=week

    HTML("output/main.html").write_pdf("output/report_week18.pdf")

    ###TO DO
    #import os
    #os.walk
    #GitLab

if __name__ == '__main__':
    main()
