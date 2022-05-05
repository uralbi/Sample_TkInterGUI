import threading

import pandas as pd
import time
from msc_fncs.fncs import current_date
from msc_fncs.fncs import min_sec
from msc_fncs.to_file_log import fns_log_file


def exc_kpi_orig(file, folder):
    bgn = time.time()
    date = current_date()[0]
    f_ndx = folder[-2::-1].find('/')
    prev_f = f'{folder[:-f_ndx - 1]}'
    f_path = f'{folder}{file}'
    out_file = f'FDEST ATA _key_ {date}.xlsx'
    df = pd.read_excel(f'{f_path}', sheet_name='KPI_RAW(FDEST ATA)', na_filter=False)
    df = df[df["Relevant Corp(대상법인)"] == 'FNS US']
    df = df[df["KPI Target Y/N"] == 'Y']
    df.insert(loc=23, column='key', value='')
    df['key'] = df['MBL No'] + df['HBL No'] + df['CNTR No']
    df.insert(loc=24, column='FTV FDEST ETA', value='')
    df.insert(loc=25, column='FTV FDEST ATA', value='')
    df.insert(loc=26, column='FTV FDEST ATA Insert', value='')

    total = len(df['CNTR No'])
    y_sum = (df['F.DEST On Time (Final)'].values == 'Y').sum()
    n_sum = (df['F.DEST On Time (Final)'].values == 'N').sum()

    no_fdeta_sum = (df['FDEST ATA'].values == '').sum()
    y_prcnt = round((y_sum/(y_sum+n_sum))*100,0)
    n_prcnt = round((n_sum/(y_sum+n_sum))*100,0)
    no_fdeta_prcnt = round((no_fdeta_sum/total)*100,0)

    print('Total cntrs: ', total)
    print('Y: ', y_sum, f'({y_prcnt}%)', '|| N: ', n_sum, f'({n_prcnt}%)')
    print('No FDEST ETA:', no_fdeta_sum, f'({no_fdeta_prcnt}%)')
    txt_info = f'KPI Total: {total} Y:{y_sum} / {y_prcnt}% || N:{n_sum} / {n_prcnt}% || ' \
               f'NO FDEST DATE: {no_fdeta_sum} / {no_fdeta_prcnt}%'
    fns_log_file(txt_info)

    df.to_excel(f'{prev_f}{out_file}', sheet_name='Data', index=None)
    end = time.time()
    info = f"Total: {total}  (Cons.time {min_sec(end-bgn)})\n Y: {y_sum} ({y_prcnt}%) // N: {n_sum} ({n_prcnt}%) " \
           f"\nNo Fdest Eta: {no_fdeta_sum} ({no_fdeta_prcnt}%)"
    print('KPI Raw : Saved')
    return info


def kpi_key_data(files, folders):
    bgn = time.time()
    df1 = pd.read_excel(f'{folders[0]}{files[0]}', na_filter=False)
    df2 = pd.read_excel(f'{folders[1]}{files[1]}', na_filter=False)
    df2.insert(loc=76, column='key', value='')
    df2['key'] = df2['MBL No'] + df2['HBL No'] + df2['CNTR No']

    df3 = df1.merge(df2[['key','F.DEST ETA', 'F.DEST ATA', 'F.DEST ATA CRT']],
                    left_on='key', right_on='key', how='left', indicator=True)
    df2.to_excel(f'{folders[1]}{files[1][:-5]}_key.xlsx', sheet_name='Data', index=None)
    df3.to_excel(f'{folders[0]}{files[0][:-5]}_k_merged.xlsx', sheet_name='Data', index=None)
    end = time.time()
    print(f'KPI Files Saved at {time.strftime("%H:%M")}  // Time cons:{min_sec(end-bgn)}')

    return f'Saved. Time cons: {min_sec(end-bgn)}'


def kpi_key_and_merge(files, folders):
    m_info = 'KPI Key and merge ... '
    print(m_info)
    file = files[0]
    folder = folders[0]
    bgn = time.time()
    date = current_date()[0]
    f_ndx = folder[-2::-1].find('/')
    prev_f = f'{folder[:-f_ndx - 1]}'
    f_path = f'{folder}{file}'
    out_file = f'FDEST ATA _key_ {date}.xlsx'
    df = pd.read_excel(f'{f_path}', sheet_name='KPI_RAW(FDEST ATA)', na_filter=False)
    df = df[df["Relevant Corp(대상법인)"] == 'FNS US']
    df = df[df["KPI Target Y/N"] == 'Y']
    df.insert(loc=23, column='key', value='')
    df['key'] = df['MBL No'] + df['HBL No'] + df['CNTR No']
    df.insert(loc=24, column='FTV FDEST ETA', value='')
    df.insert(loc=25, column='FTV FDEST ATA', value='')
    df.insert(loc=26, column='FTV FDEST ATA Insert', value='')

    total = len(df['CNTR No'])
    y_sum = (df['F.DEST On Time (Final)'].values == 'Y').sum()
    n_sum = (df['F.DEST On Time (Final)'].values == 'N').sum()

    no_fdeta_sum = (df['FDEST ATA'].values == '').sum()
    y_prcnt = round((y_sum / (y_sum + n_sum)) * 100, 0)
    n_prcnt = round((n_sum / (y_sum + n_sum)) * 100, 0)
    no_fdeta_prcnt = round((no_fdeta_sum / total) * 100, 0)

    # print('Total cntrs: ', total)
    # print('Y: ', y_sum, f'({y_prcnt}%)', '|| N: ', n_sum, f'({n_prcnt}%)')
    # print('No FDEST ETA:', no_fdeta_sum, f'({no_fdeta_prcnt}%)')

    txt_info = f'KPI Total: {total} Y:{y_sum} / {y_prcnt}% || N:{n_sum} / {n_prcnt}% || ' \
               f'NO FDEST DATE: {no_fdeta_sum} / {no_fdeta_prcnt}%'
    fns_log_file(txt_info)
    end = time.time()

    txt_info=f"Total: {total}  (Cons.time {min_sec(end - bgn)})\n Y: {y_sum} ({y_prcnt}%) || N: {n_sum} ({n_prcnt}%) " \
           f"\nNo Fdest Eta: {no_fdeta_sum} ({no_fdeta_prcnt}%)"
    print(txt_info)

    bgn = time.time()
    df2 = pd.read_excel(f'{folders[1]}{files[1]}', na_filter=False)
    df2.insert(loc=76, column='key', value='')
    df2['key'] = df2['MBL No'] + df2['HBL No'] + df2['CNTR No']

    df3 = df.merge(df2[['key', 'F.DEST ETA', 'F.DEST ATA', 'F.DEST ATA CRT']],
                    left_on='key', right_on='key', how='left', indicator=True)
    # df2.to_excel(f'{folders[1]}{files[1][:-5]}_key.xlsx', sheet_name='Data', index=None)
    df3.to_excel(f'{folders[0]}{files[0][:-5]}_k_merged.xlsx', sheet_name='Data', index=None)
    end = time.time()
    txt_info2 = f'KPI File Saved at {time.strftime("%H:%M")}  // Time cons:{min_sec(end - bgn)}'
    print(txt_info2)
    # final_info = f'Saved. Time cons: {min_sec(end - bgn)}'
    return


