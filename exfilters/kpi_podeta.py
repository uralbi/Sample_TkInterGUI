import pandas as pd
import numpy as np
import time
import datetime
from msc_fncs.fncs import min_sec
from msc_fncs.my_decorators import timing

# U.POD ETA
# POD ATA

in_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/7 KPI FDEST/03-2022/Original 3/(Sea) U.POD ETA Accuracy_POD ATA On Time Input_2022.03.08 v1.1.xlsb'
out_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/7 KPI FDEST/03-2022/Original 3/p_U.POD ETA Accuracy_POD ATA On Time Input_2022.03.08.xlsx'

sheet = 'KPI_RAW(U.POD ETA & POD ATA)'

#  ----------------------------------------------------------------  U.POD ETA Raw extractor
df = pd.read_excel(in_file, sheet_name=sheet, na_filter=False)
df = df[df['Relevant corp(대상법인)'] == 'FNS US']
df['YEAR'] = '2022'
df['MONTH'] = '3'

df1 = df[df["KPI Target Y/N(U.POD ETA)"] == 'Y']
df1 = df1[['YEAR', 'MONTH', 'MBL No', 'HBL No', 'CNTR No', 'CNEE', 'POD Port', 'POD ETA', 'POD ATA', 'U.POD ETA', 'U.POD ACCR Y/N (Final)']]
print(f'UPOD ETA: {len(df1.index)}')
print(df1['U.POD ACCR Y/N (Final)'].value_counts())
#  ----------------------------------------------------------------  POD ATA Raw extractor
df2 = df[df["KPI Target Y/N(POD ATA)"] == 'Y']
df2 = df2[['YEAR', 'MONTH', 'MBL No', 'HBL No', 'CNTR No', 'CNEE', 'POD Port', 'POD ATA', 'POD ATA Ins', 'POD ATA On Time(Final)' ]]
print(f'UPOD ETA: {len(df2.index)}')
print(df2['POD ATA On Time(Final)'].value_counts())
with pd.ExcelWriter(out_file) as writer:
    df1.to_excel(writer, sheet_name='UPOD ETA', index=None)
    df2.to_excel(writer, sheet_name='PODATA', index=None)