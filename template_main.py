#!/usr/bin/env python3.8
"""
titulek:    Jinja2 templating
vysledek:   vysledne html
autor:      medulka
verze:      week20
datum:      od 21. kvetna 2021 a dale
"""

import datetime
import csv
from jinja2 import Environment, PackageLoader, select_autoescape, Template
from weasyprint import HTML
import shutil
import os
import base64


#vytvoreni prostredi
env = Environment(
    loader = PackageLoader('__main__', '.'),
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


def main():
    #datum a pocitani tydnu
    now=datetime.datetime.now()
    now = now.strftime('%d. %m. %Y' )
    #week = datetime.datetime.isocalendar(now)  - nefunguje

    seznam_kapitol = precti_seznam_kapitol("template/seznam_kapitol.csv")

    #copy css
    shutil.copyfile("template/report.css", "output/report.css")


    #nacteni template
    template = env.get_template("template/template_main.html")

    #kopirovani obrazku z adresare input do output
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
            seznam_kapitol = seznam_kapitol, 
            now = now, 
            enumerate = enumerate,  
            float = float, 
            int = int,
            input_table = input_table,
            obrazek = obrazek
        )
        f_result.write(content)     
        #kovertovat obrazky do data url formatu
        
        
    print(f"Obrazky: {' '.join(obrazky)}")
    HTML("output/main.html").write_pdf("output/report_week20.pdf")

if __name__ == '__main__':
    main()


# [r'(\sna)\s+', ..]
# re.gsub(item, r'\1&nbsp;', re.G)