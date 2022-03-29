import pandas as pd
import time
from msc_fncs.fncs import min_sec


def n1d_imdl(raw_file, LGE_path):
    edited_file = 'p_N1D_IMDL_Edited_p.xlsx'
    start_t = time.time()
    df = pd.read_excel(f'{LGE_path}{raw_file}', na_filter=False)
    df['FDEST Port'] = ''
    df = df[['HBL',	'CNTR#',	'SSL',	'Firms Code',	'VESSEL',	'POD',	'POD\nATA',	'PORT\nP/U',
    'T/L WH ATA',	'RAILDROP',	'RAIL ATA',	'FDEST Port', 'W/H ATA',
             'POD ATA - P/U', 'FNS - RAIL RAMP', 'On Rail 구간', 'F.RAMP - W/H', 'TTL L/T']]
    total_data = len(df['HBL'])
    total = f'Total: {total_data}'
    df.to_excel(f'{LGE_path}{edited_file}', sheet_name='Data', index=None)
    exec_time = time.time() - start_t
    cons_time = f'\nTime consumed: {min_sec(exec_time)}'
    return total + cons_time
