import pandas as pd

ftvcols = ['Mode', 'Shipper', 'Consignee', 'AU', 'Division', 'P/O No', 'S/A No', 'House B/L No', 'Invoice No', 'Container No', 'Item', 'QTY', 'Dropship Y/N', 'Master B/L No', 'Container Type', 'Seal No', 'Gross_Weight', 'Incoterms', 'Carrier', 'Route', 'HOT Cntr', 'Diversion', 'Buyer', 'Terminal', 'Current Status', 'Current Port', 'Current Date', 'Current Vessel', 'Exception', 'Exception Status', 'EXF Port', 'EXF ATD', 'POL Mode', 'POL Port', 'POL Vessel', 'MIN_SR_ETD', 'POL Initial ETD', 'POL ETD', 'RSD', 'POL ATD', 'TS1 Port', 'TS1 Vessel', 'TS1 ETA', 'TS1 ATA', 'TS1 Initial ETD', 'TS1 ETD', 'TS1 ATD', 'TS2 Port', 'TS2 Vessel', 'TS2 ETA', 'TS2 ATA', 'TS2 Initial ETD', 'TS2 ETD', 'TS2 ATD', 'TS3 Port', 'TS3 Vessel', 'TS3 ETA', 'TS3 ATA', 'TS3 Initial ETD', 'TS3 ETD', 'TS3 ATD', 'POD Mode', 'POD Port', 'POD Standard ETA (L/T)', 'POD Carrier ETA', 'POD ETA', 'POD ATA', 'POD RAD', '내륙운송 LT', 'CY1 Port', 'CY1 ETA', 'CY1 ATA', 'CY1 Mode', 'CY1 ETD', 'CY1 ATD', 'CY2 Port', 'CY2 ETA', 'CY2 ATA', 'CY2 Mode', 'CY2 ETD', 'CY2 ATD', 'CY3 Port', 'CY3 ETA', 'CY3 ATA', 'CY3 Mode', 'CY3 ETD', 'CY3 ATD', 'Import Declaration', 'FDEST Mode', 'FDEST Port', 'FDEST Initial ETA', 'FDEST ETA', 'FDEST ATA', 'RAD', 'RAD(Final)', 'PO Type', 'W/H In Date', 'Remark', 'LGE P/O No', 'LGE SO No', 'SO Type', 'CBM', 'MH/CH', 'FDEST Port(MBL)', 'Updated M.PDEL']
p44cols = ['Branch', 'MBL No', 'HBL No', 'Busi Group', 'CNTR No', 'Part', 'DC', 'Status Verbose', 'Carrier Name', 'Carrier Scac', 'POL Loc Locode', 'POL Loc Name', 'Leg1 Vessel Name', 'Leg1 Voyage', 'POD Loc Locode', 'POL ATD', 'POD Loc Name', 'POD ETA', 'POD ETA(RPA)', 'POD ATA', 'CY1 ATA', 'CY1 ATD', 'CY1 ATD(Railinc)', 'CY2 ATA', 'CY2 ATA(Railinc)', 'CY2 ATD', 'Dlv Loc Locode', 'FDEST ETA', 'FDEST ATA', 'FDEST ATA Recv Time', 'Dlv Loc Name', 'Empty Loc Locode', 'Empty Loc Name', 'Empty Return Date', 'Last Upd Dt']

ftv_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/P44 - FTV check/Test/FTV POD ATA 0101-0228 Raw.xlsx'
p44_file = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/9 P44/P44 - FTV check/Test/10.01 - 03.25 P44 Updated.xlsx'

df2 = pd.read_excel(f'{p44_file}', na_filter=False)

df1 = pd.read_excel(f'{ftv_file}', na_filter=False)
c_names1 = df1.columns.values.tolist()




print(c_names1)

