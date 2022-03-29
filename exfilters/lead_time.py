import time
import pandas as pd
from msc_fncs.fncs import min_sec


def lead_time(filename, path):
    LGE_path = path
    raw_file = filename
    edited_file = f'p_{filename[:-5]}.xlsx'
    start_t = time.time()
    df = pd.read_excel(f'{LGE_path}{raw_file}', na_filter=False)
    fdest_ports = ('USFW7', 'USLOT', 'USMCH', 'USSBT', 'USSOJ', 'USXF7')
    route_e = ('AWT', 'MLB')
    df['CY1 ATD - POD ATA'] = '=Q2-M2'
    df['F.DEST ATA - CY1 ATD'] = '=X2-Q2'
    df['TOTAL'] = '=Z2+Y2'
    df = df[['House B/L No', 'Invoice No', 'Container No', 'Carrier', 'Route', 'HOT Cntr', 'Diversion', 'Buyer',
             'Terminal', 'Current Vessel', 'POD Mode', 'POD Port', 'POD ATA', 'CY1 Port', 'CY1 ATA', 'CY1 Mode',
             'CY1 ATD', 'CY2 Port', 'CY2 ATA', 'CY2 Mode', 'CY2 ATD', 'FDEST Mode', 'FDEST Port', 'FDEST ATA',
             'CY1 ATD - POD ATA', 'F.DEST ATA - CY1 ATD', 'TOTAL']]
    df = df[df['FDEST Port'].isin(fdest_ports)]
    df = df[df['Route'].isin(route_e)]
    df = df.drop_duplicates(subset=['Container No'])
    total_data = len(df['House B/L No'])
    df.to_excel(f'{LGE_path}{edited_file}', sheet_name='Contents', index=None)
    exec_time = time.time() - start_t
    return 'Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
