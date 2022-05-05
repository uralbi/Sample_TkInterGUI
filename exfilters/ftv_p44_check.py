import pandas as pd
import numpy as np
import time
import datetime
from msc_fncs.fncs import min_sec
from msc_fncs.my_decorators import timing
fdest = ['USFW7', 'USLOT', 'USSBT', 'USSOJ', 'USXF7']
cdc_codes = {
'USSBT':'NF2',
'USLOT':'N1D',
'USXF7':'N1F',
'USSOJ':'N1A',
'USFW7':'NTX' }

def excel_step1():
    """
    1. Merging: FTV(fdest 5) + Empty + P44
    2. Drop Duplicates in Key
    3. Renaming columns: FTV / P44
    :return: Savid file ... _all_merged.xlsx
    """
    start = time.time()
    ftv_file='C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/FTV LGE 0101-0331 Raw.xlsx'
    p44_file='C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/P44 FNS Raw_2.xlsx'
    empt_file='C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/EMPTY RETURN REPORT_1201-0406.xlsx'
    ftv_all_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/p_FTV_all_merged.xlsx'

    df_ftv = pd.read_excel(ftv_file, na_filter=None)
    df_ftv['Key'] = df_ftv['House B/L No'] + df_ftv['Master B/L No'] + df_ftv['Container No']
    df_ftv = df_ftv[['House B/L No','Master B/L No', 'Container No', 'Carrier', 'FDEST Port', 'Key', 'POD ETA', 'POD ATA',
                     'CY1 ATA', 'CY1 ATD', 'CY2 ATA', 'CY2 ATD']]
    print('FTV Total len:',len(df_ftv.index))

    df_ftv = df_ftv[df_ftv['FDEST Port'].isin(fdest)]

    print('FTV fdest 5:', len(df_ftv.index))

    df_ftv = df_ftv.drop_duplicates(subset=['Key'])

    print('After dropping duplicates in key:', len(df_ftv.index))

    # get Empty return date from the empty file:

    df_emp = pd.read_excel(empt_file, na_filter=None)
    df_emp['Key'] = df_emp['HBL No']+df_emp['MBL No']+df_emp['CNTR No']
    df_emp = df_emp.drop_duplicates(subset=['Key'])

    df_emp=df_emp[['Key', 'Empty Return Date ↓']]

    df_ftv_emp = df_ftv.merge(df_emp[['Key', 'Empty Return Date ↓']], left_on='Key', right_on='Key', how='left', indicator=False)

    print('FTV + EMPTY:', len(df_ftv_emp.index))
    df_ftv_emp = df_ftv_emp.rename(columns={'POD ETA':'FTV POD ETA', 'POD ATA': 'FTV POD ATA', 'CY1 ATA': 'FTV CY1 ATA',
                                            'CY1 ATD': 'FTV CY1 ATD', 'CY2 ATA': 'FTV CY2 ATA', 'CY2 ATD': 'FTV CY2 ATD',
                                            'Empty Return Date ↓':'FTV Empty Return Date'})

    df_p44 = pd.read_excel(p44_file, na_filter=None)
    df_p44['Key'] = df_p44['HBL No'] + df_p44['MBL No'] + df_p44['CNTR No']
    df_p44 = df_p44[['Key', 'POD ETA', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY2 ATA', 'CY2 ATD', 'Empty Return Date']]

    df_p44 = df_p44.drop_duplicates(subset=['Key'])

    df_all = df_ftv_emp.merge(df_p44[['Key', 'POD ETA', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY2 ATA', 'CY2 ATD', 'Empty Return Date']],
                              left_on='Key', right_on='Key', how='left', indicator=True)

    print('FTV + EMPTY + P44:', len(df_all.index))
    df_all = df_all.rename(columns={'POD ETA':'P44 POD ETA', 'POD ATA': 'P44 POD ATA', 'CY1 ATA': 'P44 CY1 ATA',
                                    'CY1 ATD': 'P44 CY1 ATD', 'CY2 ATA': 'P44 CY2 ATA', 'CY2 ATD': 'P44 CY2 ATD',
                                    'Empty Return Date': 'P44 Empty Return Date'})

    print('after duplicates: ', len(df_all.index))
    print('saving ... FTV_all_merged.xlsx')
    df_all.to_excel(ftv_all_file, index=None)
    end = time.time()
    print(f'time consumed: {min_sec(end-start)}')


def date_cnv(str):
    if str:
        try:
            a = pd.to_datetime(str)
            if a.month < 10 and a.day < 10:
                return f'{a.year}-0{a.month}-0{a.day}'
            elif a.month < 10 and a.day > 9:
                return f'{a.year}-0{a.month}-{a.day}'
            elif a.month > 9 and a.day < 10:
                return f'{a.year}-{a.month}-0{a.day}'
            else:
                return f'{a.year}-{a.month}-{a.day}'
        except:
            return str
    return str


def excel_step2():
    """
    1. All data to str_Date
    2. Rearranging columns
    3. Delete Duplicates
    :return: Saved file ..._d3.xlsx
    """
    start = time.time()
    print('started...')
    ftv_all_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/p_FTV_all_merged.xlsx'
    ftv_all_file2 = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/p_FTV_all_merged_d3.xlsx'
    df = pd.read_excel(ftv_all_file, na_filter=None)
    df = df.applymap(lambda x: date_cnv(x), na_action='ignore')

    df['Duplicates'] = df.duplicated('Container No')
    t_dups = df['Duplicates'].eq(True).sum()
    print('Duplicated containers: ', t_dups)
    df = df[df['Duplicates'].eq(True) & df['_merge'].eq('left_only') == False]
    print(f'Data {len(df.index)} / Dropped duplicates (cntr_No cntr)')
    d_list = df.loc[df['Duplicates'].eq(True), 'Container No'].to_list()
    df = df[df['Container No'].isin(d_list) & df['_merge'].eq('left_only') == False]
    print(f'Data {len(df.index)} / Dropped duplicates (cntr_No cntr)')

    month_ver = {1: 'JAN', 2: 'FEB', 3: 'MAR'}
    df['Month'] = df['FTV POD ATA'].map(lambda x: month_ver.get(int(x[5:7])))
    df['CDC'] = df['FDEST Port'].map(lambda x: cdc_codes.get(x))

    df = df[['Key', 'House B/L No','Master B/L No', 'Container No', 'FDEST Port', 'CDC', 'Carrier', 'Month',  'FTV POD ETA', 'P44 POD ETA', 'FTV POD ATA','P44 POD ATA',
             'FTV CY1 ATA', 'P44 CY1 ATA', 'FTV CY1 ATD', 'P44 CY1 ATD', 'FTV CY2 ATA', 'P44 CY2 ATA', 'FTV CY2 ATD', 'P44 CY2 ATD',
             'FTV Empty Return Date', 'P44 Empty Return Date', '_merge']]

    print('data len:', len(df.index))
    print('saving... FTV_all_merged_d3.xlsx')

    df.to_excel(ftv_all_file2, index=None)

    end = time.time()
    print(f'time consumed: {min_sec(end-start)}')


@timing
def excel_step3():
    print('Starting step 3...')
    in_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/p_FTV_all_merged_d3.xlsx'
    out_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/01-03 FTV-P44 Check/p_FTV_all_merged_CHECK.xlsx'

    df = pd.read_excel(in_file, na_filter=None)

    month_ver = {1:'JAN', 2: 'FEB', 3: 'MAR'}
    df['Month'] = df['FTV POD ATA'].map(lambda x: month_ver.get(int(x[5:7])))

    cols = ['POD ETA', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY2 ATA', 'CY2 ATD', 'Empty Return Date']

    psx = 22
    for col in cols[::-1]:
        df.insert(loc=psx, column=f'{col} V1', value='')
        psx -= 2

    for vi in cols:
        df[f'FTV {vi}'] = df[f'FTV {vi}'].map(lambda x: x if x else 'No Date')
        df[f'P44 {vi}'] = df[f'P44 {vi}'].map(lambda x: x if x else 'No Date')
        df.loc[df["_merge"] == "left_only", f'P44 {vi}'] = 'No Cntr'

    for col in cols:
        conditions = [
            df['_merge'] == 'left_only',
            df[f'FTV {col}'].eq('No Date') & df[f'P44 {col}'].eq('No Date'),
            df[f'FTV {col}'].eq('No Date') & df[f'P44 {col}'].ne('No Date'),
            df[f'FTV {col}'].ne('No Date') & df[f'P44 {col}'].eq('No Date'),
            df[f'FTV {col}'] == df[f'P44 {col}'],
            df[f'FTV {col}'] != df[f'P44 {col}'],
        ]
        choices = ["6) P44에 Cntr 없음", '5) FTV 및 P44에 Date 없음', "4) FTV에 없고 P44에 있음", "3) FTV에 있고 P44 Date 없음", "1) 같음", "2) 다름" ]

        df[f'{col} V1'] = np.select(conditions, choices)
    print('Saving ... FTV_all_merged_CHECK.xlsx')
    df.to_excel(out_file, index=None)


# excel_step1()
# excel_step2()
excel_step3()



