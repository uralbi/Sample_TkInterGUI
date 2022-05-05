import time
import numpy as np
import pandas as pd
from msc_fncs.fncs import min_sec
from msc_fncs.to_file_log import fns_log_file

def newlge_flt(filename, path):
    lge_raw = filename
    LGE_path = path
    info = []
    east = ['USSAV', 'USNYC', 'USNNY', 'USCHS', 'USMIA', 'USJAX', 'USBOS', 'USBAL',
            'USHOU', 'USEWR', 'USTPA', 'USORF', 'USMOB', 'USMSY']
    start_t = time.time()

    df = pd.read_excel(f'{LGE_path}{lge_raw}', na_filter=False)

    try:
        df = df[df['HBL No'].str.contains('PLI')]
        df = df[df['CNTR No'] != '']
        df = df[df['POL ATD'].str.contains('202')]
        df = df[df['POD ATA'].str.contains('202') == False]
        df = df[df['POD\nLOC'].str.startswith('US') | df['POD\nLOC'].str.startswith('CA')]
        df = df[df['POD\nLOC'].str.startswith('CA') & df['F.DEST\nLOC'].str.startswith('CA') == False]
        df = df.drop_duplicates(subset=['CNTR No'])

        e_west = np.where(df['POD\nLOC'].isin(east), 'East', 'West')
        df.insert(loc=6, column='East_West', value=e_west)

        total_data = len(df['HBL No'])
        east_cnt = len(df[df['POD\nLOC'].isin(east)])
        west_cnt = total_data - east_cnt

        info.append(f'Total: {total_data}')
        info.append(f'West: {west_cnt}')
        info.append(f'East: {east_cnt}')

        txt_info = f'LGE Raw Total:{total_data} West:{west_cnt} East:{east_cnt}'
        fns_log_file(txt_info)

        df.to_excel(f'{LGE_path}{lge_raw[:-5]}_edited.xlsx', index=None)

        exec_time = time.time() - start_t
        total_t = min_sec(exec_time)
        info.append(f'Time consumed: {total_t}')
        info_text = info[0] + ' ' + info[1] + ' ' + info[2] + '\n' + info[3]
    except:
        info_text = 'Please select a correct file'
    return info_text