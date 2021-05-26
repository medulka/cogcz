#!usr/bin/env python3.8
"""
varianty - info
"""


import pandas as pd    
import numpy as np
import matplotlib.pyplot as plt
import csv

from pandas.core.reshape.concat import concat


src1 = '/Users/hanamedova/Documents/COG/week20/report/input/hmedova/nextclade.tsv'
usecols = ["seqName", "clade", "aaSubstitutions", "aaDeletions"]
tab1 = pd.read_csv(src1, delimiter = '\t', usecols = usecols) #all
tab1b = pd.read_csv(src1, delimiter = '\t', usecols = ["seqName", "clade"]) 
tab1c = tab1["aaSubstitutions"].str.split(pat = ",", expand = True) #jen sloupec se substitucemi
tab1d  = pd.concat([tab1["clade"], tab1c], axis = 1) #CLADE + substituce ve sloupcich
tabm = tab1b = pd.read_csv(src1, delimiter = '\t', usecols = ["clade", "aaSubstitutions"]) 

tab1.shape  #(3027, 4)
tab1b.shape  #(3027, 2)
tab1c.shape  #(3027, 40)
tab1e.shape  #(3027, 2)
tab1d.shape
tab1d.head()

a = tab1.value_counts(subset = ["clade"])
len(a)  # distinct clades
# clade      
# 20I/501Y.V1    2370
# 20A             480
# 20H/501Y.V2      69
# 20B              54
# 20A.EU2          33
# 20E (EU1)        12
# 20D               6
# 19B               2
# 20G               1

#finding unique mutations:
lst_all = []
lst_all_in_one = []
for item in tab1["aaSubstitutions"].loc[tab1["clade"] == "20D"]:
    sublist = item.split(",")
    lst_all.append(sublist)
for sublist in lst_all:
    for item in sublist:
        lst_all_in_one.append(item)
len(lst_all_in_one)
lst_all_in_one.value_count()
lst_all_in_one.sort()



pd.unique(tab1c)
pd.unique(pd.Series(pd.Categorical(lst_all_in_one, ordered = True) ))
lst_all_mutations = pd.unique(pd.Series(pd.Categorical(lst_all_in_one, ordered = True) ))  #Length: 2015


###

###

import pandas as pd
import csv

nextclade = "/Users/hanamedova/Documents/COG/week20/datafreeze/df-20210521_all_nextclade_0.14.3.tsv"
pangolin = "/Users/hanamedova/Documents/COG/week20/datafreeze/df-20210521_all_pangolin_v.2.4.2_pangoLEARN_2021-05-19.csv"

def join_tables(src1, src2):
    with open(nextclade) as csv1:
        f1 = pd.read_csv(csv1, sep = "\t") # usecols=
    with open(pangolin) as csv2:
        f2 = pd.read_csv(csv2, sep = ",")
    tab_joined = pd.merge(f1, f2, how="inner", left_on = "seqName", right_on = "taxon", sort = True)
    cols = ["seqName", "clade","aaSubstitutions","totalAminoacidSubstitutions", "aaDeletions", "totalAminoacidDeletions", "taxon", "lineage" ]
    return tab_joined[cols]


tab = join_tables(nextclade, pangolin) #[2325 rows x 6 columns]
tab.columns
tab["clade"].value_counts()  #??? Jak pracovat s vysledkem fce
# 20I/501Y.V1    1827
# 20A             385
# 20B              44
# 20H/501Y.V2      34
# 20E (EU1)        17
# 20D               9
# 21A               5
# 20G               2
# 19A               1
# 20C               1

ls = tab["lineage"].value_counts()
# B.1.1.7       1827
# B.1.258        279
# B.1.221         36
# B.1.351         34
# B.1.160         33
# B.1             18
# B.1.1           17
# B.1.1.277        9
# B.1.177.8        8
# B.1.177          8
# C.35             6
# B.1.527          4
# B.1.1.170        4
# B.1.617.2        4
# B.1.416.1        4
# B.1.1.219        4
# P.2              3
# None             3
# B.1.2            2
# B.1.1.153        2
# B.1.1.243        2
# C.36             2
# B.1.258.12       2
# B.1.258.15       2
# B.1.1.39         1
# B.1.153          1
# B.1.623          1
# B.1.177.77       1
# B.1.620          1
# B.1.1.266        1
# B.1.1.1          1
# B.1.177.86       1
# B.1.1.374        1
# B.1.1.317        1
# B.1.177.35       1
# B.1.396          1

all_lineages = list(pd.unique(list(tab["lineage"]) ) )   # vysledkem fce - list  #??? filter - vetsi jak 10
len(all_lineages) #36
# ['B.1.1.7', 'B.1.160', 'B.1.258', 'B.1.527', 'B.1.221', 'C.35',
#        'B.1.1.153', 'B.1.396', 'B.1.1.219', 'B.1.177', 'B.1.153', 'B.1.1',
#        'B.1.1.317', 'B.1.351', 'C.36', 'B.1.177.86', 'B.1.1.266', 'P.2',
#        'B.1.177.8', 'B.1.620', 'B.1', 'B.1.1.39', 'B.1.1.243',
#        'B.1.416.1', 'B.1.1.277', 'None', 'B.1.177.77', 'B.1.1.170',
#        'B.1.258.12', 'B.1.1.1', 'B.1.1.374', 'B.1.258.15', 'B.1.2',
#        'B.1.177.35', 'B.1.623', 'B.1.617.2']
len(lins) #36

#vyzobavam linie
tab_b117  = tab.loc[tab["lineage"] == "B.1.1.7"] #1827
tab_b1258 = tab.loc[tab["lineage"] == "B.1.258"] #279
tab_b1221 = tab.loc[tab["lineage"] == "B.1.221"] #36
tab_b1351 = tab.loc[tab["lineage"] == "B.1.351"] #34
tab_b1160 = tab.loc[tab["lineage"] == "B.1.160"] #33

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