import pandas as pd
import time
from msc_fncs.fncs import min_sec


def ntx_imdl(raw_file, LGE_path):
    edited_file = 'p_NTX_IMDL_Edited.xlsx'
    start_t = time.time()
    df = pd.read_excel(f'{LGE_path}{raw_file}', na_filter=False)
    df['FDEST Port'] = ''
    df = df[['HBL',	'CNTR No',	'SSL',	'TML',	'VSL',	'POD',	'POD ATA',	'Port Pick Up',
    'T/L W/H ATA',	'Rail Drop',	'Rail ATA',	'FDEST Port', 'W/H ATA',
             'Pod ATA Pu', 'Fns Rail Ramp', 'On Rail Section', 'F.Ramp W/H', 'TTL L/T']]
    total_data = len(df['HBL'])
    total = f'Total: {total_data}'
    df.to_excel(f'{LGE_path}{edited_file}', sheet_name='Contents',index = None)
    exec_time = time.time() - start_t
    cons_time = f'\nTime consumed: {min_sec(exec_time)}'
    return total + cons_time