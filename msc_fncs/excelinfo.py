import pandas as pd

def excelinfo(file1, file2):
    df1 = pd.read_excel(f'{file1}', na_filter=False)
    c_names1 = df1.columns.values.tolist()
    total1 = len(df1[f'{c_names1[0]}'])

    df2 = pd.read_excel(f'{file2}', na_filter=False)
    c_names2 = df2.columns.values.tolist()
    total2 = len(df2[f'{c_names2[0]}'])

    same_cols = [i for i in c_names1 for j in c_names2 if i==j]

    df1["KEY"] = df1['MBL No'] + df1['HBL No'] + df1['CNTR No']

    df2["KEY"] = df2['Master B/L No'] + df2['House B/L No'] + df2['Container No']

    print(f'file1: Rows{total1} / file2: rows{total2}')
    print(f'Same cols:{len(same_cols)}')




file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/P44 - FTV check/FTV LGEGlobal Data.xlsx'


p44 = ['Branch', 'MBL No', 'HBL No', 'Busi Group', 'CNTR No', 'Part', 'DC', 'Status Verbose', 'Carrier Name', 'Carrier Scac', 'POL Loc Locode', 'POL Loc Name', 'Leg1 Vessel Name', 'Leg1 Voyage',
       'POD Loc Locode', 'POL ATD', 'POD Loc Name', 'POD ETA', 'POD ETA(RPA)', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY1 ATD(Railinc)', 'CY2 ATA', 'CY2 ATA(Railinc)', 'CY2 ATD', 'Dlv Loc Locode',
       'FDEST ETA', 'FDEST ATA', 'FDEST ATA Recv Time', 'Dlv Loc Name', 'Empty Loc Locode', 'Empty Loc Name', 'Empty Return Date', 'Last Upd Dt']

ftv = ['Mode', 'Shipper', 'Consignee', 'AU', 'Division', 'P/O No', 'S/A No', 'House B/L No', 'Invoice No', 'Container No', 'Item', 'QTY', 'Dropship Y/N', 'Master B/L No', 'Container Type', 'Seal No',
       'Gross_Weight', 'Incoterms', 'Carrier', 'Route', 'HOT Cntr', 'Diversion', 'Buyer', 'Terminal', 'Current Status', 'Current Port', 'Current Date', 'Current Vessel', 'Exception', 'Exception Status',
       'EXF Port', 'EXF ATD', 'POL Mode', 'POL Port', 'POL Vessel', 'MIN_SR_ETD', 'POL Initial ETD', 'POL ETD', 'RSD', 'POL ATD', 'TS1 Port', 'TS1 Vessel', 'TS1 ETA', 'TS1 ATA', 'TS1 Initial ETD',
       'TS1 ETD', 'TS1 ATD', 'TS2 Port', 'TS2 Vessel', 'TS2 ETA', 'TS2 ATA', 'TS2 Initial ETD', 'TS2 ETD', 'TS2 ATD', 'TS3 Port', 'TS3 Vessel', 'TS3 ETA', 'TS3 ATA', 'TS3 Initial ETD', 'TS3 ETD',
       'TS3 ATD', 'POD Mode', 'POD Port', 'POD Standard ETA (L/T)', 'POD Carrier ETA', 'POD ETA', 'POD ATA', 'POD RAD', '내륙운송 LT', 'CY1 Port', 'CY1 ETA', 'CY1 ATA', 'CY1 Mode', 'CY1 ETD', 'CY1 ATD',
       'CY2 Port', 'CY2 ETA', 'CY2 ATA', 'CY2 Mode', 'CY2 ETD', 'CY2 ATD', 'CY3 Port', 'CY3 ETA', 'CY3 ATA', 'CY3 Mode', 'CY3 ETD', 'CY3 ATD', 'Import Declaration', 'FDEST Mode', 'FDEST Port',
       'FDEST Initial ETA', 'FDEST ETA', 'FDEST ATA', 'RAD', 'RAD(Final)', 'PO Type', 'W/H In Date', 'Remark', 'LGE P/O No', 'LGE SO No', 'SO Type', 'CBM', 'MH/CH', 'FDEST Port(MBL)', 'Updated M.PDEL']

s_cols = ['POL ATD', 'POD ETA', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY2 ATA', 'CY2 ATD', 'FDEST ETA', 'FDEST ATA']


print(len(s_cols))
print(s_cols)