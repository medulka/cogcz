#!usr/bin/env python3.8
"""
varianty - info
"""


import pandas as pd    
import numpy as np
import matplotlib.pyplot as plt
import csv


### ideas
# src1 = '/Users/hanamedova/Documents/COG/week20/report/input/hmedova/nextclade.tsv'
# usecols = ["seqName", "clade", "aaSubstitutions", "aaDeletions"]
# tab1 = pd.read_csv(src1, delimiter = '\t', usecols = usecols) #all
#tab1c = tab1["aaSubstitutions"].str.split(pat = ",", expand = True) #jen sloupec se substitucem
# lst_all_mutations = pd.unique(pd.Series(pd.Categorical(lst_all_in_one, ordered = True) ))  #Length: 2015

nextclade = "/Users/hanamedova/Documents/COG/week20/datafreeze/df-20210521_kolarmi/fastaAll_nextclade_0.14.3.tsv"
pangolin = "/Users/hanamedova/Documents/COG/week20/datafreeze/df-20210521_kolarmi/fastaAll_pangolin_v.2.4.2_pangoLEARN_2021-05-19.csv"

def join_tables(src1, src2):
    with open(nextclade) as csv1:
        f1 = pd.read_csv(csv1, sep = "\t") # usecols=
    with open(pangolin) as csv2:
        f2 = pd.read_csv(csv2, sep = ",")
    tab_joined = pd.merge(f1, f2, how="inner", left_on = "seqName", right_on = "taxon", sort = True)
    cols = ["seqName", "clade","aaSubstitutions","totalAminoacidSubstitutions", "aaDeletions", "totalAminoacidDeletions", "taxon", "lineage" ]
    return tab_joined[cols]


tab = join_tables(nextclade, pangolin) #[4168 rows x 8 columns]
tab.columns
tab["clade"].value_counts() 
# 20I/501Y.V1    3262
# 20A             716
# 20B              88
# 20H/501Y.V2      51
# 20E (EU1)        24
# 20D              13
# 21A               8
# 20G               3
# 19B               2
# 20C               1

ls_lineage_counts = list(tab["lineage"].value_counts(sort = False))
len(ls_lineage_counts) #44
ls_lineage_counts = list(tab["lineage"].value_counts(normalize=True))
# B.1.1.7       3261
# B.1.258        533
# B.1.221         75
# B.1.160         52
# B.1.351         51  #>1% vyskyt
# B.1.1           35
# B.1             26
# B.1.1.153       12
# B.1.177         12
# B.1.1.277       11
# B.1.177.8       10
# B.1.527          8
# B.1.1.219        8
# B.1.416.1        7
# C.35             7
# P.2              6
# C.36             4
# B.1.617.2        4
# B.1.1.170        4
# B.1.617.1        3
# B.1.620          3
# B.1.1.318        3
# B.1.2            3
# B.1.258.12       2
# B.1.396          2
# B.1.258.15       2
# B.1.1.266        2
# B.1.153          2
# B.1.1.397        2
# B.1.1.243        2
# B.1.177.86       2
# B.1.1.317        2
# B.1.623          1
# B.1.1.1          1
# B.1.177.35       1
# B.1.1.374        1
# B.1.177.77       1
# B.1.533          1
# A                1
# B.1.258.3        1
# C.16             1
# B.1.1.39         1
# A.21             1
# B.1.1.28         1

#lineage ze souboru nextclade od Michala Kolare, df_20210521
ls_unique_lineages = list(pd.unique(list(tab["lineage"]) ) )   # filter - vetsi jak 10
#['B.1.1.7', 'B.1.160', 'B.1.258', 'B.1.527', 'B.1.221', 'C.35', 'B.1.1.153', 'B.1.396', 'B.1.1.219', 'B.1.177', 'B.1.153', 'B.1.1', 'B.1.1.317', 'B.1.351', 'C.36', 'B.1.177.86', 'B.1.1.266', 'P.2', 'B.1.620', 'B.1', 'B.1.617.2', 'B.1.1.39', 'B.1.1.243', 'B.1.416.1', 'B.1.1.277', 'B.1.177.77', 'B.1.1.170', 'B.1.258.12', 'B.1.1.1', 'B.1.177.8', 'B.1.1.374', 'B.1.258.15', 'B.1.2', 'B.1.177.35', 'B.1.623', 'A.21', 'B.1.258.3', 'B.1.1.28', 'B.1.1.397', 'C.16', 'A', 'B.1.1.318', 'B.1.617.1', 'B.1.533']
len(ls_unique_lineages) #44


# #spojeni dvou listu - varianty + pocet vzorku jejich vyskytu
# ls_doubles = []
# for i in range(len(ls_unique_lineages)):
#     ls_doubles.append([ls_unique_lineages[i],ls_lineage_counts[i]])
# print(ls_doubles)
# ls_lineage_counts[0]
# ls_unique_lineages[0]
# #nedava smysl, spatne serazene, pouzij jinou fuknci na pocitani cetnosti
# #TO DO: napsat fci

#vybiram linie - ECDC
#https://www.ecdc.europa.eu/en/covid-19/variants-concern

def pick_ecdc_variants_in_czechia(ls_scr):
    "in: list with actual Czech variants(nextclade, Michal Kolar),out: list of variants in Czechia klasified after ECDC"
    ls_voc = ['B.1.1.7','B.1.1.7+E484K', 'B.1.351','P.1']
    ls_voi = ['B.1.525','B.1.427','B.1.429','P.3','B.1.616','B.1.617.1','B.1.617.2','B.1.617.3','B.1.620', 'B.1.621']
    ls_vom = ['B.1.214.2','A.23.1','A.23.1+E484K','A.27','A.28','C.16','C.37','B.1.351+P384L','B.1.351+E516Q','B.1.1.7+L452R', 'B.1.1.7+S494P','C.36','C.36+L452R','AT.1','B.1.526','B.1.526.1','B.1.526.2','B.1.1.318','P.2']
    ls_ecdc_variants_all = ls_voc + ls_voi + ls_vom
    ecdc_variants_cz = []
    for item in ls_scr:
        if item in ls_ecdc_variants_all:
            ecdc_variants_cz.append(item)
    return sorted(ecdc_variants_cz)        

pick = pick_ecdc_variants_in_czechia(ls_unique_lineages)
ls1 = ['B.1.1.318', 'B.1.1.7', 'B.1.351', 'B.1.617.1', 'B.1.617.2', 'B.1.620', 'C.16', 'C.36', 'P.2']
ls2 = [3, 3261, 51, 3, 4, 3, 1, 4, 6]
tab_b11318  = tab.loc[tab["lineage"] == "B.1.1.318"] #3
tab_b117  = tab.loc[tab["lineage"] == "B.1.1.7"] #3261
tab_b1351 = tab.loc[tab["lineage"] == "B.1.351"] #51
tab_b16171 = tab.loc[tab["lineage"] == "B.1.617.1"] #3
tab_b16172 = tab.loc[tab["lineage"] == "B.1.617.2"] #4
tab_b1620 = tab.loc[tab["lineage"] == "B.1.620"] #3
tab_c16 = tab.loc[tab["lineage"] == "C.16"] #1
tab_c36 = tab.loc[tab["lineage"] == "C.36"] #4
tab_p2 = tab.loc[tab["lineage"] == "P.2"] #6

 #spojeni dvou listu - varianty + pocet jejich vyskytu
def spojeni_dvou_listu(l1, l2):
    ls_doubles = []
    for i in range(len(l1)):
        ls_doubles.append([ls1[i],ls2[i]])
    return ls_doubles
ls2[0]
spojeni_dvou_listu(ls1, ls2)
#[['B.1.1.318', 3], ['B.1.1.7', 3261], ['B.1.351', 51], ['B.1.617.1', 3], ['B.1.617.2', 4], ['B.1.620', 3], ['C.16', 1], ['C.36', 4], ['P.2', 6]]

#melange mutaci: 
m1 = []
m2 = []
for lineage in ls1:
    t = tab.loc[tab["lineage"] == lineage]["aaSubstitutions"]
    print(t)

for line in t:
    item = line.split(",")
    m1.append(item)
for sublist in m1:  
    for item in sublist:
        m2.append(item)

# a ted zpracuj jeden list a vytvor data pro jednu mutaci, vloz do df


#melange mutaci
#b1160
lst_mutations_b1160 = []
all_mutations_b1160 = []
for line in tab_b1160["aaSubstitutions"]:
    item = line.split(",")
    lst_mutations_b1160.append(item)
for sublist in lst_mutations_b1160:  #??? napsat si fci, jak pocitat prevalence mutaci pres podseznamy v seznamu
    for item in sublist:
        all_mutations_b1160.append(item)

len(all_mutations_b1160) #521

unique_mutations_b1160 = sorted(list(pd.unique(all_b1160))) #list
# ['E:V62F', 'N:A376T', 'N:I337F', 'N:M210I', 'N:M234I', 'N:P396S', 'N:R385K', 'N:T166I', 'ORF1a:A1049V', 'ORF1a:A2097V', 'ORF1a:A2593V', 'ORF1a:A690V', 'ORF1a:E93K', 'ORF1a:G400S', 'ORF1a:H110Y', 'ORF1a:I1785V', 'ORF1a:I3369T', 'ORF1a:L1559F', 'ORF1a:L1713I', 'ORF1a:L3606F', 'ORF1a:L681F', 'ORF1a:L730F', 'ORF1a:M3087I', 'ORF1a:M3655I', 'ORF1a:N3118S', 'ORF1a:P309L', 'ORF1a:R3368H', 'ORF1a:S391F', 'ORF1a:T1543I', 'ORF1a:T1605I', 'ORF1a:T2846I', 'ORF1a:T4159I', 'ORF1a:T814I', 'ORF1a:V106A', 'ORF1a:V3718F', 'ORF1a:V774I', 'ORF1b:A176S', 'ORF1b:A2143T', 'ORF1b:A2513V', 'ORF1b:A2565V', 'ORF1b:E1184D', 'ORF1b:G2151D', 'ORF1b:H1897Y', 'ORF1b:H2388Y', 'ORF1b:K1141R', 'ORF1b:K2231N', 'ORF1b:L1220F', 'ORF1b:L1351F', 'ORF1b:L1504F', 'ORF1b:P218L', 'ORF1b:P314L', 'ORF1b:P970S', 'ORF1b:Q1669R', 'ORF1b:R1315C', 'ORF1b:S2031I', 'ORF1b:S2198I', 'ORF1b:S961P', 'ORF1b:T2040I', 'ORF1b:V1811F', 'ORF1b:V1984L', 'ORF1b:V767L', 'ORF3a:A110P', 'ORF3a:A110S', 'ORF3a:A99V', 'ORF3a:D155Y', 'ORF3a:D265E', 'ORF3a:Q57H', 'ORF3a:V202L', 'ORF3a:W193R', 'ORF7a:A13V', 'ORF7a:P99S', 'ORF7b:M24I', 'ORF7b:T40N', 'ORF8:E59*', 'ORF8:I121X', 'ORF8:W45L', 'ORF9b:T83I', 'S:A1070V', 'S:A570V', 'S:A845S', 'S:D614G', 'S:G1085A', 'S:G261V', 'S:I569V', 'S:M153I', 'S:Q677H', 'S:S477N', 'S:V1230L', 'S:V213M']
counts_all_mut_b110 = np.asarray([pd.DataFrame(all_mutations_b1160).value_counts(sort = False)]) #array
# [1, 31, 1, 2, 33, 1, 27, 3, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 8, 1, 1, 33, 1, 4, 1, 1, 2, 2, 1, 2, 1, 1, 4, 1, 2, 33, 2, 1, 2, 33, 1, 4, 1, 33, 1, 1, 1, 2, 1, 32, 1, 1, 1, 1, 1, 1, 1, 2, 1, 33, 1, 1, 4, 1, 1, 33, 2, 2, 1, 2, 1, 4, 9, 1, 1, 1, 5, 1, 2, 33, 2, 1, 1, 1, 3, 33, 1, 1]


#data pro heatmapu
df_mut_counts_b1160 = pd.DataFrame(data = counts_all_mut_b110, columns = unique_mutations_b1160, index = ["B.1.160"]) # data - array, columns - list

#pozor - kazda varianta ma vlastni mutace
#filter na cetnost




#frekvence
len(unique_mutations_b1160)  #89
len(unique_mutations_b1160) / len(all_mutations_b1160)  #0.17


import matplotlib.pyplot as plt
plt.hist(df_mut_counts_b1160)
plt.plot(df_mut_counts_b1160)







###
def main():

if __name__ == '__main__':
    main()