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

src1 = "/Users/hanamedova/Documents/COG/week34/datafreeze-2021-08-27_12_weeks_good.nextclade.1.2.3"
src2 = "/Users/hanamedova/Documents/COG/week34/datafreeze-2021-08-27_12_weeks_good.tsv"