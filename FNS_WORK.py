import datetime
import os
import threading
from tkinter import filedialog
import numpy as np
import pandas as pd
from subprocess import call
import time
import tkinter as tk
from tkinter import *
from dateutil.utils import today
from webtrack.container import one_track, cosco_mbl_track, sm_track, hap_track, sud_track, apl_track, ww_track, \
    mae_track, mat_track, wan_track, evg_track
from FNS_data.static import apl_key, ww_key, mae_cont, one_conts, tracks, wan_cont, wan_key, non_tracks
from msc_fncs.fncs import min_sec, todo, current_date


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('FNS')
        self.configure(background='#595959')
        self.geometry("400x200")
        # p1 = tk.PhotoImage(file='pics/logo.png')
        # self.iconphoto(False, p1)
        self.files = []
        self.folders = []
        self.edt_file = []
        self.my_fold = []
        t_date = today()
        t_day = t_date.day
        t_mon = t_date.month
        t_day = t_day if len(str(t_day)) > 1 else f'0{t_day}'
        t_mon = t_mon if len(str(t_mon)) > 1 else f'0{t_mon}'
        self.date_info = f'{current_date()[0]}'
        main_btn_color = "#a6a6a6"
        file1_txt = tk.StringVar()
        file1_btn = tk.Button(self, textvariable=file1_txt, command=self.open_file,
                               bg=main_btn_color, fg='black', border=1)
        file1_txt.set("Select File #1")
        file1_btn.place(relx=0.02, rely=0.45, relwidth=0.3, relheight=0.15)

        file2_txt = tk.StringVar()
        file2_btn = tk.Button(self, textvariable=file2_txt, command=self.open_file2,
                                bg=main_btn_color, fg="black", border=1)
        file2_txt.set("Select File #2")
        file2_btn.place(relx=0.02, rely=0.65, relwidth=0.3, relheight=0.15)

        self.label = tk.Label(text="", bg='#404040', fg='#d9d9d9', borderwidth=1, relief = 'solid')
        self.label.place(relx=0.02, rely=0.14, relwidth=0.96, relheight=0.29)
        self.label1 = tk.Label(text="", bg='#565656', fg='#cccccc', anchor='w')
        self.label1.place(relx=0.02, rely=0.03)
        self.label1['text'] = todo()
        # FILTER BUTTONS:
        rel_x = 0.35

        # Choose Filter
        self.OPTIONS = ['Choose filter:', 'LGE Raw', "Non LGE Raw", "FRT Raw", 'FTV Error',
                   'Fdest NotIN-All', 'LEAD TIME Raw', 'ETA_WEB_TRACK', 'MERGE']  # etc

        self.variable = StringVar()
        self.variable.set(self.OPTIONS[0])  # default value
        self.fltr_list = OptionMenu(self, self.variable, *self.OPTIONS)
        self.fltr_list.config(bd = 0, bg = "#bfbfbf")
        self.fltr_list.place(relx=rel_x, rely=0.45, relwidth=0.3, relheight=0.15)

        # APPLY BUTTON
        flt_text = tk.StringVar()
        flt_btn = tk.Button(self, textvariable=flt_text, command=self.apply_filter,
                            font="Arial 10", bg="#ffffe6", fg="black", height=2, border=1)
        flt_text.set(">>")
        flt_btn.place(relx=rel_x, rely=0.65, relwidth=0.3, relheight=0.15)

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_folder,
                               font="Gray 10", bg=main_btn_color, fg="Black", border=1
                               ).place(relx=0.68, rely=0.45, relwidth=0.3, relheight=0.35)
        folder_text.set("Open Folder")

        width_ = 0.09
        b_color = '#999999'
        brd = 1
        vert_coor = 0.85

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_lge_f,
                               font="Black 8", bg=b_color, fg="Black", border=brd
                               ).place(relx=0.02, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("LGE")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_nlge_f,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.12, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("NLGE")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_frt_f,
                               font="Black 8", bg=b_color, fg="Black", height=2,border=brd
                               ).place(relx=0.22, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("FRT")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_ftv_f,
                               font="Black 8", bg=b_color, fg="Black", height=2,border=brd
                               ).place(relx=0.32, rely=vert_coor, relwidth=width_-0.01, relheight=0.1)
        folder_text.set("FTV")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_fdest_f,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.41, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("FDST")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_lead_f,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.51, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("LEAD")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_mbl_f,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.61, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("MBL")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_blm_f,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.71, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("BLMG")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_fns_f,
                               font="Black 8", bg='#bfbfbf', fg="Black", height=2, border=brd
                               ).place(relx=0.81, rely=vert_coor, relwidth=0.17, relheight=0.1)
        folder_text.set("FNS")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_f_codes,
                               font="Black 8", bg='#595959', fg="#999999", height=2, border=0
                               ).place(relx=0.87, rely=0.02, relheight=0.1)
        folder_text.set("Notes")

        folder_text = tk.StringVar()
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_emails,
                               font="Black 8", bg='#595959', fg="#999999", height=2, border=0
                               ).place(relx=0.75, rely=0.02, relheight=0.1)
        folder_text.set("Emails")

    def open_f_codes(self):
        pdf_f = 'msc_fncs/f_codes.txt'
        try:
            call(["open", pdf_f])
        except:
            path = os.path._getfullpathname(pdf_f)
            os.system(f"explorer {path}")

    def open_emails(self):
        pdf_f = 'msc_fncs/fns_emails.pdf'
        try:
            call(["open", pdf_f])
        except:
            path = os.path._getfullpathname(pdf_f)
            os.system(f"explorer {path}")

    def lge_eta(self, filename, path):
        lge_raw = filename
        LGE_path = path
        info = []
        info_text = ''
        east = ('USSAV', 'USNYC', 'USNNY', 'USCHS', 'USMIA', 'USJAX', 'USBOS', 'USBAL',
                'USHOU', 'USEWR', 'USTPA', 'USORF', 'USMOB', 'USMSY')
        start_t = time.time()
        df = pd.read_excel(f'{LGE_path}{lge_raw}', na_filter=False)

        try:
            df = df[df['House B/L No'].str.contains('PLI')]
            df = df[df['Container No'] != '-']
            df = df[df['POD Port'].str.startswith('MX') == False]
            df = df[df['POD Port'].str.startswith('TW') == False]
            df = df[df['POL ATD'].str.contains('202')]
            df = df[df['POD ATA'].str.contains('20') == False]
            df = df.drop_duplicates(subset=['Container No'])

            e_west = np.where(df['POD Port'].isin(east), 'East', 'West')
            df.insert(loc=63, column='East_West', value=e_west)

            total_data = len(df['House B/L No'])
            east_cnt = len(df[df['POD Port'].isin(east)])
            west_cnt = total_data - east_cnt

            info.append(f'Total: {total_data}')
            info.append(f'West: {west_cnt}')
            info.append(f'East: {east_cnt}')

            df.to_excel(f'{LGE_path}{lge_raw[:-5]}_edited.xlsx',
                        sheet_name='Contents', index=None)
            self.edt_file.append(f'{lge_raw[:-5]}_edited.xlsx')
            exec_time = time.time() - start_t
            total_t = min_sec(exec_time)
            info.append(f'Time consumed: {total_t}')
            info_text = info[0] + ' ' + info[1] + ' ' + info[2] + '\n' + info[3]
        except:
            info_text = 'Please select a correct file'
        self.label['text'] = info_text
        self.files, self.folders = [], []

    def n_lge_eta(self, filename, path):
        lge_raw = filename
        LGE_path = path
        info = []
        east = ['USSAV', 'USNYC', 'USNNY', 'USCHS', 'USMIA', 'USJAX', 'USBOS', 'USBAL',
                'USHOU', 'USEWR', 'USTPA', 'USORF', 'USMOB', 'USMSY']
        start_t = time.time()

        df = pd.read_excel(f'{LGE_path}{lge_raw}', na_filter=False)

        try:
            df = df[['HBL No', 'MBL No', 'CNTR No', 'Cust CNEE', 'POL ATD', 'Current Vessel',
                     'POD\nLOC', 'POD ETA', 'POD ATA', 'F.DEST\nLOC', 'F.DEST ETA']]

            df = df[df['HBL No'].str.contains('PLI')]
            df = df[df['CNTR No'] != '']
            df = df[df['POL ATD'].str.contains('202')]
            df = df[df['POD ATA'].str.contains('202') == False]
            df = df[df['POD\nLOC'].str.startswith('US') | df['POD\nLOC'].str.startswith('CA')]
            df = df[df['POD\nLOC'].str.startswith('CA') & df['F.DEST\nLOC'].str.startswith('CA') == False]
            df = df.drop('POL ATD', 1)

            e_west = np.where(df['POD\nLOC'].isin(east), 'East', 'West')
            df.insert(loc=6, column='East_West', value=e_west)

            total_data = len(df['HBL No'])
            east_cnt = len(df[df['POD\nLOC'].isin(east)])
            west_cnt = total_data - east_cnt

            info.append(f'Total: {total_data}')
            info.append(f'West: {west_cnt}')
            info.append(f'East: {east_cnt}')

            df.to_excel(f'{LGE_path}{lge_raw[:-5]}_edited.xlsx', index=None)
            self.edt_file.append(f'{lge_raw[:-5]}_edited.xlsx')
            exec_time = time.time() - start_t
            total_t = min_sec(exec_time)
            info.append(f'Time consumed: {total_t}')
            info_text = info[0] + ' ' + info[1] + ' ' + info[2] + '\n' + info[3]
        except:
            info_text = 'Please select a correct file'
        self.label['text'] = info_text
        self.files, self.folders = [], []

    def frt_terminal(self, filename, path):

        LGE_path = path
        lge_raw = filename
        start_t = time.time()
        df = pd.read_excel(f'{LGE_path}{lge_raw}', na_filter=False)
        df['EmptyCol'] = ''
        df = df[df['HBL No'].str.contains('PLI')]
        df = df[df['CNTR No'] != '']
        df = df[df['Terminal ↓'] == '']
        df = df[df['POD'].str.startswith('US') | df['POD'].str.startswith('CA')]
        df = df[df['POD'].str.startswith('CA') & df['F.DEST'].str.startswith('CA') == False]
        df['Key'] = df['HBL No'] + df['MBL No'] + df['CNTR No']
        df = df[['HBL No', 'MBL No', 'CNTR No', 'Current Vessel',
                 'Key', 'EmptyCol', 'EmptyCol', 'EmptyCol', 'POD\nLOC', 'POD ETA', 'F.DEST\nLOC', 'F.DEST ETA']]
        total_data = len(df['HBL No'])
        output_file = f'{LGE_path}FRT_edited_p.xlsx'
        self.edt_file.append(output_file)
        df.to_excel(output_file, index=None)
        exec_time = time.time() - start_t
        self.label['text'] = 'Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
        self.files, self.folders = [], []

    def ftv_error(self, filename, path):

        LGE_path = path
        Error_path = path
        file_error = filename
        start_t = time.time()
        df = pd.read_excel(f'{LGE_path}{file_error}', na_filter=False)

        df['FDEST ETA'] = pd.to_datetime(df['FDEST ETA'])
        df['POD ETA'] = pd.to_datetime(df['POD ETA'])
        df['FDest ETA - POD ETA'] = (df['FDEST ETA'].apply(lambda x: x.value) - df['POD ETA'].apply(
            lambda x: x.value)) / (86400 * (10 ** 9))

        df = df[['Master B/L No', 'House B/L No', 'Container No', 'Current Vessel',
                 'POD Port', 'POD ETA', 'POD ATA', 'FDEST Port', 'FDEST ETA', 'FDEST ATA', 'FDest ETA - POD ETA']]

        df = df[df['House B/L No'].str.contains('PLI')]
        df = df[df['Container No'] != '-']
        df = df[df['FDEST Port'].str.startswith('MX') == False]
        df = df[df['FDEST ATA'] == '']
        df = df[df['FDest ETA - POD ETA'] < 0]
        total_data = len(df['House B/L No'])
        output_file = f'{Error_path}{file_error[:-8]} Error_fix_p.xlsx'
        df.to_excel(output_file, index=None)
        self.edt_file.append(output_file)
        exec_time = time.time() - start_t
        self.label['text'] = 'Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
        self.files, self.folders = [], []

    def fdest_all(self, filename1, filename2, path1):

        LGE_path = path1

        lge_raw = filename1
        nlge_raw = filename2
        start_t = time.time()

        del_cont = ('DFSU6749793', 'CAIU7463420', 'KOCU4443003')
        del_cont_hbl = ('PLISZ4B13324', 'PLISZ4B13326', 'PLISZ4B13328')

        df = pd.read_excel(f'{LGE_path}{lge_raw}', na_filter=False)

        df['BRANCH'] = ''
        df['IMP Operator'] = ''
        df['LOAD TYPE'] = ''

        df = df[df['House B/L No'].str.contains('PLI')]
        df = df[df['Container No'] != '-']
        df = df[df['FDEST Port'].str.startswith('US')]
        df = df[df['FDEST ATA'] == '']
        df = df.drop_duplicates(subset=['Container No'])
        data_0 = len(df['House B/L No'])
        df = df[df['Container No'].isin(del_cont) & df['House B/L No'].isin(del_cont_hbl) == False]
        total_data = len(df['House B/L No'])
        del_conts = f'Del containers: {data_0 - total_data}'
        lge_total = f'LGE: {total_data}'
        df = df[['House B/L No', 'Master B/L No', 'Container No', 'Current Vessel', 'POD Port', 'POD ETA',
                 'POD ATA', 'FDEST Port', 'FDEST ETA', 'FDEST ATA',
                 'BRANCH', 'IMP Operator', 'LOAD TYPE', 'Buyer']]
        # output_lge = f'{LGE_path}p_LGE_Raw_edited.xlsx'
        # df.to_excel(output_lge, index=None)

        # sort rrrrrrrrrrrrrrrrr NON LGE rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

        df2 = pd.read_excel(f'{LGE_path}{nlge_raw}', na_filter=False)

        df2 = df2[df2['HBL No'].str.contains('PLI')]
        df2 = df2[df2['CNTR No'] != '']
        df2 = df2[df2['Cust CNEE'] != 'ENUS']
        df2 = df2[df2['F.DEST ATA'] == '']
        df2 = df2[df2['POD\nLOC'].str.startswith('US') | df2['POD\nLOC'].str.startswith('CA')]
        df2 = df2[df2['POD\nLOC'].str.startswith('CA') & df2['F.DEST\nLOC'].str.startswith('CA') == False]
        df2 = df2.drop_duplicates(subset=['CNTR No'])

        df2['BRANCH'] = ''
        df2['IMP Operator'] = ''
        df2['LOAD TYPE'] = ''

        df2 = df2[['HBL No', 'MBL No', 'CNTR No', 'Current Vessel', 'POD\nLOC', 'POD ETA', 'POD ATA', \
                   'F.DEST\nLOC', 'F.DEST ETA', 'F.DEST ATA',
                   'BRANCH', 'IMP Operator', 'LOAD TYPE', 'CNEE\nName']]

        # output_nlge = f'{LGE_path}p_NON_LGE_Raw_edited.xlsx'
        # df2.to_excel(output_nlge, index=None)

        df2 = df2.rename(columns={'HBL No': 'House B/L No', 'MBL No': 'Master B/L No',
                                  'CNTR No': 'Container No', 'POD\nLOC': 'POD Port',
                                  'F.DEST\nLOC': 'FDEST Port', 'F.DEST ETA': 'FDEST ETA', 'F.DEST ATA': 'FDEST ATA',
                                  'CNEE\nName': 'Buyer'})

        total_data2 = len(df2['House B/L No'])
        nlge_total = f'Non LGE: {total_data2}'
        all_total = f'Total :{total_data + total_data2}'
        output_file = f'{LGE_path}p_All_edited.xlsx'
        self.edt_file.append(output_file)
        df3 = df.append(df2)
        df3.to_excel(output_file, index=None)
        exec_time2 = time.time() - start_t

        self.label['text'] = f' {all_total}' + f'\n{lge_total}, {nlge_total}' + \
                        '\nTime consumed: ' + f'{min_sec(exec_time2)}'
        self.files, self.folders = [], []
        self.my_fold = []

    def lead_time(self, filename, path):
        LGE_path = path
        raw_file = filename
        edited_file = f'{filename[:-5]} - Edited_p.xlsx'
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
        self.edt_file.append(edited_file)
        exec_time = time.time() - start_t
        self.label['text'] = 'Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
        self.files, self.folders = [], []

    def open_file(self):
        # file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("Excel", "*.xlsx")])
        file = filedialog.askopenfilename()
        len_file = len(file)
        f_idx = file[::-1].find('/')
        file_n = file[len_file - f_idx:]
        path = file[:len_file - f_idx]
        self.my_fold.clear()
        self.my_fold.append(path)
        if file_n.find('.xlsx') > 0 or file_n.find('.xls') > 0:
            self.files.clear()
            self.folders.clear()
            self.files.append(file_n)
            self.folders.append(path)
            self.edt_file.append(file_n)
            self.label_func(f'File 1: {self.files[0]}')
        else:
            self.label_func('Please select a file')

    def open_file2(self, ):
        if len(self.files) == 0:
            self.label['text'] = 'Please select a file'
        else:
            file = filedialog.askopenfilename()
            len_file = len(file)
            f_idx = file[::-1].find('/')
            file_n = file[len_file - f_idx:]
            if len(self.files) == 0:
                self.label['text'] = 'Please select a File 1'
            elif file_n.find('.xlsx') > 0 and file_n != self.files[0]:
                self.files.append(file_n)
                self.variable.set(self.OPTIONS[5])
                self.label['text'] = self.files[0] + ' + ' + self.files[1]
            else:
                self.label['text'] = f'Please choose different file 2. \n File 1: {self.files[0]}'

    def label_func(self, info):
        self.label['text'] = info

    def open_folder(self):
        if len(self.my_fold) > 0:
            try:
                call(["open", self.my_fold[0]])
            except:
                path = os.path._getfullpathname(self.my_fold[0])
                os.system(f"explorer {path}")
        else:
            self.label_func('Choose a file first')
            pass

    def apply_filter(self, ):
        x = self.variable.get()
        if len(self.files) == 0:
            info = 'Choose files first'
            self.label_func(info)
            self.variable.set(self.OPTIONS[0])
        elif x == 'Choose filter:':
            info = f'Select a filter for the file [{self.files[0]}]'
            self.label_func(info)
        elif len(self.files) == 1 and x == 'LGE Raw':
            info = f'File 1: {self.files[0]}' + '\nApplied Filter: ' + x
            self.label_func(info)
            time.sleep(1)
            self.lge_eta(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'ETA_WEB_TRACK':
            self.eta_tracking(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'Non LGE Raw':
            info = f'File 1: {self.files[0]}' + '\nApplied Filter: ' + x
            self.label_func(info)
            self.n_lge_eta(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'FRT Raw':
            self.frt_terminal(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'FTV Error':
            self.ftv_error(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'LEAD TIME Raw':
            self.lead_time(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'MERGE':
            self.bl_lge(self.folders[0])
        else:
            self.variable.set(self.OPTIONS[5])
            x = self.variable.get()
            self.label['text'] = f'{self.files[0]} & {self.files[1]}' + '\nApplied Filter: ' + x
            self.fdest_all(self.files[0], self.files[1], self.folders[0])

    def eta_tracking(self,filename, path):
        LGE_path = path
        lge_raw = filename
        output_file = f'{LGE_path}{lge_raw[:-5]}_track_p.xlsx'
        start_t = time.time()
        df = pd.read_excel(f'{LGE_path}{lge_raw}', sheet_name='data', na_filter=False)
        df.insert(loc=14, column='MBL_4', value=df['Master B/L No'].astype(str).str[0:4])
        df.insert(loc=15, column='MBL_KEY', value='')
        df["MBL_KEY"] = df['Current Vessel'] + '_' + df['POD Port'] + '_' + df['MBL_4']
        df["S_KEY"] = df['Current Vessel'] + df['POD Port']
        df['New ETA'] = ''
        df['ETA/ATA'] = ''
        df = df[['Current Vessel', 'Carrier', 'Master B/L No', 'Container No', 'MBL_KEY', 'POD Port', 'S_KEY', 'MBL_4',
                 'POD ETA', 'ETA/ATA', 'New ETA']]
        df = df[df['MBL_4'].isin(non_tracks) == False]
        df = df.drop_duplicates(subset=['MBL_KEY'])
        df = df.drop_duplicates(subset=['S_KEY'])
        total = len(df['Master B/L No'])
        print('Total: ', total, 'Est.time:', min_sec(total*9))
        self.label_func(f'Total: {total} Est.time: {min_sec(total*9)}')
        eta_list = self.list_m(df)
        df['New ETA'] = eta_list[0]
        df['ETA/ATA'] = eta_list[1]
        df.to_excel(output_file, sheet_name='Contents', index=None)
        exec_time = time.time() - start_t
        self.label_func(f'File Saved \n Time consumed: {min_sec(exec_time)} (Per cont: {min_sec(int(exec_time/total))})')

    def list_m(self, df):
        my_l = []
        my_l_2 = []
        total_data = df.shape[0]
        for cont, key in zip(df['Container No'], df['MBL_4']):
            ea, eta = '-', '-'
            if key == 'ONEY':
                try:
                    eta_info = one_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'COSU':
                try:
                    eta_info = cosco_mbl_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'SMLM':
                try:
                    eta_info = sm_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key in apl_key :
                try:
                    eta_info = apl_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'MAEU' or key.isdigit():
                try:
                    eta_info = mae_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'EGLV':
                try:
                    eta_info = evg_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'MATS':
                try:
                    eta_info = mat_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'SUDU':
                try:
                    eta_info = sud_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key == 'HLCU':
                try:
                    eta_info = hap_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key in ww_key:
                try:
                    eta_info = ww_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif key in wan_key or cont[:4] in wan_cont:
                try:
                    eta_info = wan_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0]
                except:
                    eta = '--'
                    ea = '--'
            elif cont[:4] == 'CCLU' or cont[:4] == 'OOCU':
                try:
                    eta_info = cosco_mbl_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0] + '/COS'
                except:
                    eta = '--'
                    ea = '--'
            elif cont[:4] in mae_cont:
                try:
                    eta_info = mae_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0] + '/MAE'
                except:
                    eta = '--'
                    ea = '--'
            elif cont[:4] == 'CMAU':
                try:
                    eta_info = apl_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0] + '/APL'
                except:
                    eta = '--'
                    ea = '--'
            elif cont[:4] in one_conts:
                try:
                    eta_info = one_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0] + '/ONE'
                except:
                    eta = '--'
                    ea = '--'
            if eta == '--':
                try:
                    eta_info = one_track(cont)
                    eta = eta_info[1]
                    ea = eta_info[0] + '/ONE'
                except:
                    eta = '--'
                    ea = '--'
            my_l.append(eta)
            my_l_2.append(ea)
            if len(my_l) % (total_data//10) == 0:
                completed = round((len(my_l) / total_data) * 100, 0)
                print(f'Progress: {completed} %')
        return my_l, my_l_2

    def open_lge_f(self ):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/2 LGE Tracking'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")

        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_nlge_f(self ):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/2 Non LGE Tracking'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")
        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_frt_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/3 FRT Terminal'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")
        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_ftv_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/4 FTV Report'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")

    def open_fdest_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/5 FDEST NOT INPUT'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")
        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_lead_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/1 Lead TUE'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")

    def open_mbl_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/1 MBL 2WED'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")
        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_blm_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/6 BL MERGE'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")
        new_abs_path = os.path.join(fns_path, f'{self.date_info}')
        if not os.path.exists(new_abs_path):
            os.mkdir(new_abs_path)

    def open_fns_f(self):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")

    def bl_lge(self, path):
        output_name = f'{self.date_info} Merged File.xlsx'
        output_path = f'{path}{output_name}'
        files = os.listdir(path)
        start = time.time()
        file_1 = files.pop(0)
        df = pd.read_excel(f'{path}{file_1}', na_filter=False)
        i = 2
        for file in files:
            df_2 = pd.read_excel(f'{path}{file}', na_filter=False)
            # df_len = len(df_2['HBL No'])
            # self.label_func(f'file {i}: {df_len}')
            df = df.append(df_2)
            i += 1
        tt = df.shape[0]
        df.to_excel(output_path, sheet_name='Data', index=None)
        end = time.time()
        exec_time = end - start
        self.label_func(f'File saved. Total {tt} \nTime consumed: {min_sec(exec_time)}')

if __name__ == '__main__':
    app = App()
    app.mainloop()