import pandas as pd
from my_decorators import timing

file1 = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/01 - 기타 업무/TRUCK RAIL.xlsx'
p_file1 = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/01 - 기타 업무/p_TRUCK RAIL.xlsx'

def exc_flt(file1):
    df = pd.read_excel(f'{file1}', sheet_name='Description', na_filter=False)

    df.insert(loc=2, column='cities', value='')
    df.insert(loc=3, column='State', value='')
    df['cities'] = ''
    df['State'] = ''

    cities = []
    states = []
    for i in df['Descr']:
        idx = i.find(',')
        cities.append(i[:idx])
        states.append(i[idx+1:].strip())

    df['cities'] = cities
    df['State'] = states

    df.to_excel(p_file1, index=None)



HBL = f'C:/Users/URAL KOZHOKMATOV/Documents/FNS/7 KPI FDEST/03-2022/HBL/HBL LL.xlsx'


@timing
def HBL_data(kpi_file):
    df1 = pd.read_excel(f'{kpi_file}', na_filter=False)
    cols = df1.columns.values.tolist()
    print(cols[:5])

HBL_data(HBL)