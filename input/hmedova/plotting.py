#!/usr/bin/env python3
"""
barplot - Varianty vs celkove pocty
"""

import pandas as pd    
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.algorithms import value_counts
import seaborn as sns
sns.set_theme(style="whitegrid")

def join_tables(src1, src2):
    with open(src1) as csv1:
        f1 = pd.read_csv(csv1, sep = ",", usecols=["taxon","lineage"]) 
    with open(src2) as csv2:
        f2 = pd.read_csv(csv2, sep = "\t", usecols=["fasta_id", "region", "week_number"])    
    two_joined_tables = pd.merge(f1, f2, how="inner", left_on = "taxon", right_on = "fasta_id", sort = True)
    # print(two_joined_tables.head())    
    return two_joined_tables

def counts_lineage(src1, src2):
    data_lineage = join_tables(src1, src2)
    " aggregate the lineages, counts for a lineage and a week; in: dataframe, out: dataframe"
    data_lineage2 = pd.DataFrame({"week_number": data_lineage["week_number"], "lineage" : data_lineage["lineage"]})
    value_counts = list(data_lineage2.value_counts().items())
    ls = []
    labels = []
    for index,tuples in enumerate(value_counts):
        if tuples[1] > 2:
            a = value_counts[index][0][0]
            b = value_counts[index][0][1]
            c = value_counts[index][1]
            ls.append([a,b,c])
    data = pd.DataFrame(ls, columns=("week_number", "lineage", "count")).sort_values("lineage")
    return data

def adding_zeros(df):
    weeks = sorted(df["week_number"].unique())
    for lin in df["lineage"]
        for item in weeks:
            if item not in df["week_number"]:
                df = df.append({"week_number": item, "lineage": lin, "count": 0}, ignore_index = True)


def unique_lineges(src1, src2):
    " get  the lineages with counts >=3 in a week; in: dataframe, out: list"
    data_lineage = join_tables(src1, src2)
    data_lineage2 = pd.DataFrame({"week_number": data_lineage["week_number"], "lineage" : data_lineage["lineage"]})
    value_counts = list(data_lineage2.value_counts().items())
    ls = []
    labels = []
    for index,tuples in enumerate(value_counts):
        if tuples[1] > 2:
            b = value_counts[index][0][1]
            if b not in labels:
                labels.append(b)  
    return labels


#def main():
# Load the dataset
src1 = "/Users/hanamedova/Documents/COG/week28/datafreeze-2021-07-16_12_weeks.pangolin-3.1.7-pangoLEARN-2021-07-09.csv"
src2 = "/Users/hanamedova/Documents/COG/week28/datafreeze-2021-07-16_12_weeks.tsv"
src3 = "/Users/hanamedova/Documents/COG/week28/statistics-2021-07-16.csv"

# the total cases of covid-19
with open(src3) as csv3:
    data_total = pd.read_csv(csv3, sep = ";", encoding="unicode_escape", usecols=["kraj_code", "week_number", "cases"], parse_dates=["week_number"])      
data_total.dtypes
data_total = data_total.sort_values("week_number")

# get the lineages
data_lin = counts_lineage(src1, src2)
list_of_unique_lineages = unique_lineges(src1,src2)
#['B.1.1.7', 'B.1.617.2', 'P.1', 'C.36.3', 'B.1.351', 'B.1.1.354']
weeks = sorted(data_lin["week_number"].unique())

    # def split_lineages(df, lst_of_lineages):
    #     for lin in lst_of_lineages:
    #         s(lin) = df.loc[df["lineage"]== lin].sort_values("week_number")
    #     return s(lin)

s1 = data_lin.loc[data_lin["lineage"]== 'B.1.1.7'].sort_values("week_number")
s2 = data_lin.loc[data_lin["lineage"]== 'B.1.617.2'].sort_values("week_number")
s3 = data_lin.loc[data_lin["lineage"]== 'P.1'].sort_values("week_number")
s4 = data_lin.loc[data_lin["lineage"]== 'C.36.3'].sort_values("week_number")
s5 = data_lin.loc[data_lin["lineage"]== 'B.1.351'].sort_values("week_number")
s6 = data_lin.loc[data_lin["lineage"]== 'B.1.1.354'].sort_values("week_number")

    s6b = pd.DataFrame (['2021-18', 'B.1.1.354', 0], columns = ["week_number", "lineage", "count"])
for week in weeks:
    if week not in s6["week_number"]:
        df = s6.append( {"week_number": i, "lineage": 'B.1.1.354', "count": 0}, ignore_index = True)
    s6 = df
print(s6)
print(df)

s6c = s6b.append(s6b)
    
#data_lineage2 = pd.DataFrame({"week_number": data_lineage["week_number"], "lineage" : data_lineage["lineage"]})
# data_lineage2.columns
# lin = data_lineage2["lineage"].unique()
# weeks = list(data_lineage2["week_number"].unique())
# value_counts = list(data_lineage2.value_counts().items())
# len(value_counts) #58


#categoricka data
# source_columns = data_lin.columns
# new_cols = [str(x) + "_cat" for x in source_columns]
# categories = {"2021-21": "21", "2021-17": 17}
# data_lineage2[new_cols] = data_lineage2[source_columns].applymap(categories.get)
# data_lineage2

# b.loc[b["week_number"] == "2021-20"]
# data_lineage2.groupby(by = "week_number", dropna = True).count()
# data_lineage2["freq"] = data_lineage2.groupby(by = "week_number", dropna = True)["week_number"].transform("count")
# data_lineage.loc[data_lineage["week_number"] == "2021-20"].agg(["count"])
# data_lineage.loc[data_lineage["week_number"] == "2021-20"].loc[data_lineage["lineage"] == "B.1.1.7"]
# data_lineage.loc[data_lineage["week_number"] == w].loc[data_lineage["lineage"] == l].count())
# data_lineage.loc[data_lineage["week_number"] == "2021-20"].value_counts()
# lin2 = list(data_lineage["lineage"].value_counts().items())  #jak dostat unikatni hodnoty do seznamu


# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(15, 6))

# Plot the total 
# sns.set_color_codes("pastel")
# sns.barplot(x="week_number", y="cases", data=data_total,
#             label="Total cases", color="b")


# Plot the lineages
sns.set_color_codes("muted")

for lineage in set(data_lin['lineage']):
    sns.barplot(
        x='week_number', y='count', 
        data=data_lin.loc[data_lin['lineage'] == lineage], 
        label=lineage, 
        color='#808080')

# sns.barplot(x="week_number", y="count", data=s1,
#             label="B.1.1.7", color = '#F3444B')
# sns.barplot(x="week_number", y="count", data=s2,
#             label="B.1.617.2", color = '#CAB2D6')
# sns.barplot(x="week_number", y="count", data=s3,
#             label="P.1", color = '#B2DF8A')
# sns.barplot(x="week_number", y="count", data=s4,
#             label="C.36.3", color = '#DDD100')
# sns.barplot(x="week_number", y="count", data=s5,
#             label="B.1.351", color = '#FF7F00')
# sns.barplot(x="week_number", y="count", data=s6,
#             label="B.1.1.354", color = '#B15928')


# plt.savefig('/Users/hanamedova/Documents/COG/report/input/hmedova/plot.png')


# Add a legend and informative axis label
ax.legend(ncol=2, loc="higher right", frameon=True)
ax.set(xlim=(0, 24), ylabel="cases detected",
       xlabel="week of the year")


if __name__ == '__main__':
    main()
