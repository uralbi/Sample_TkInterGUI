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

from msc_fncs.to_file_log import fns_log_file
from webtrack.container import one_track, cosco_mbl_track, sm_track, hap_track, sud_track, apl_track, ww_track, \
    mae_track, mat_track, wan_track, evg_track, med_track
from FNS_data.static import apl_key, ww_key, mae_cont, one_conts, tracks, wan_cont, wan_key, non_tracks, med_cont, \
    vessel_names
from msc_fncs.fncs import min_sec, todo, current_date
from exfilters.newlge import newlge_flt
from exfilters.imdl_n1d import n1d_imdl
from exfilters.imdl_ntx import ntx_imdl
from exfilters.lead_time import lead_time
from exfilters.kpi_orig import exc_kpi_orig, kpi_key_data


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('FNS')
        self.configure(background='#595959')
        self.geometry("400x200")
        p1 = tk.PhotoImage(file='pics/cont.png')
        self.iconphoto(True, p1)
        self.files = []
        self.folders = []
        self.edt_file = []
        self.last_fld = ''
        self.text_info = ''
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

        self.label_process = tk.Label(text="", bg='#565656', fg='#cccccc', anchor='w')
        self.label_process.place(relx=0.3, rely=0.03)
        self.label_process['text'] = '|'

        # FILTER BUTTONS:
        rel_x = 0.35

        # Choose Filter
        self.OPTIONS = ['FILTER', 'LGE Raw', "FRT Raw", 'FTV Error', 'FTV Fnl_Sea', 'FTV ERR_Sea',
                        'Fdest All',  'ETA_Tracking', 'CONCAT', 'LEAD Raw', 'N1D_Raw', 'NTX_Raw', 'KPI_ALL', 'KPI_Orig',
                        'KPI_KeyM', 'Concat_2f']  # etc

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

        self.folder_text = tk.StringVar()
        self.folder_btn = tk.Button(self, textvariable=self.folder_text, command=self.open_folder,
                               font="Gray 10", bg=main_btn_color, fg="Black", border=1
                               ).place(relx=0.68, rely=0.45, relwidth=0.3, relheight=0.35)
        self.folder_text.set("Folder")

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
        folder_btn = tk.Button(self, textvariable=folder_text, command=self.open_pier,
                               font="Black 8", bg=b_color, fg="Black", height=2, border=brd
                               ).place(relx=0.12, rely=vert_coor, relwidth=width_, relheight=0.1)
        folder_text.set("PIER")

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

        txt_info = f'FRT Raw Total:{total_data}'
        fns_log_file(txt_info)

        output_file = f'{LGE_path}FRT_edited_p.xlsx'
        self.edt_file.append(output_file)
        df.to_excel(output_file, index=None)
        exec_time = time.time() - start_t
        info  = 'Terminal Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
        print('Terminal Total: ' + f'{total_data}' + 'Time consumed: ' + f'{min_sec(exec_time)}')
        return info

    def ftv_error(self, file1, path1):
        threading.Thread(target=self.status_func, args=('| FTV error ...',)).start()
        filename = file1
        path = path1
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

        txt_info = f'FTV Error Total:{total_data}'
        threading.Thread(target=fns_log_file, args=(txt_info,)).start()
        output_file = f'{Error_path}{file_error[:-8]} Error_fix_p.xlsx'
        df.to_excel(output_file, index=None)
        self.edt_file.append(output_file)
        exec_time = time.time() - start_t
        info = 'FTV Error Total: ' + f'{total_data}' + '\n' + 'Time consumed: ' + f'{min_sec(exec_time)}'
        threading.Thread(target=self.label_func, args=(info,)).start()
        threading.Thread(target=self.status_func, args=(f'|',)).start()

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
        data_0 = len(df.index)
        df = df[df['Container No'].isin(del_cont) & df['House B/L No'].isin(del_cont_hbl) == False]
        total_data = len(df.index)
        del_conts = f'Del containers: {data_0 - total_data}'
        print(del_conts)
        lge_total = f'LGE: {total_data}'
        df = df[['House B/L No', 'Master B/L No', 'Container No', 'Current Vessel', 'POD Port', 'POD ETA',
                 'POD ATA', 'FDEST Port', 'FDEST ETA', 'FDEST ATA',
                 'BRANCH', 'IMP Operator', 'LOAD TYPE', 'Buyer']]
        # output_lge = f'{LGE_path}p_LGE_Raw_edited.xlsx'
        # df.to_excel(output_lge, index=None)
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

        txt_info = f'FDEST Raw Total:{all_total}'
        fns_log_file(txt_info)

        output_file = f'{LGE_path}p_All_edited.xlsx'
        self.edt_file.append(output_file)
        df3 = df.append(df2)

        df3['FDEST ETA'] = pd.to_datetime(df3['FDEST ETA'])
        df3['POD ETA'] = pd.to_datetime(df3['POD ETA'])
        df3['FDEST ATA'] = round((df3['FDEST ETA'].apply(lambda x: x.value) - df3['POD ETA'].apply(
            lambda x: x.value)) / (86400 * (10 ** 9)),0)

        df3.to_excel(output_file, index=None)
        exec_time2 = time.time() - start_t

        info = f' {all_total}' + f'\n{lge_total}, {nlge_total}' + \
                        '\nTime consumed: ' + f'{min_sec(exec_time2)}'
        print(f' {all_total}' + f' {lge_total}, {nlge_total}' + \
                        '// Time consumed: ' + f'{min_sec(exec_time2)}')
        return info

    def open_file(self):
        # file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("Excel", "*.xlsx")])
        file = filedialog.askopenfilename()
        len_file = len(file)
        f_idx = file[::-1].find('/')
        file_n = file[len_file - f_idx:]
        path = file[:len_file - f_idx]
        self.last_fld = path
        f = path[:-1]
        fnx = f[::-1].find('/')
        f = f[-fnx:]
        if file_n.find('.xlsx') > 0 or file_n.find('.xls')> 0:
            self.files.clear()
            self.folders.clear()
            self.files.append(file_n)
            self.folders.append(path)
            self.edt_file.append(file_n)
            self.label_func(f'File 1: {self.files[0]}')
            self.folder_text.set(f"Open folder:\n{f}")
        else:
            self.label_func('Please select a file')
            self.folder_text.set("Folder")

    def open_file2(self):
        if len(self.files) == 0:
            self.label['text'] = 'Please select a file'
        else:
            file = filedialog.askopenfilename()
            len_file = len(file)
            f_idx = file[::-1].find('/')
            file_n = file[len_file - f_idx:]
            path = file[:len_file - f_idx]
            self.folders.append(path)
            if len(self.files) == 0:
                self.label['text'] = 'Please select a File 1'
            elif file_n.find('.xlsx') > 0 and file_n != self.files[0]:
                self.files.append(file_n)
                self.label['text'] = self.files[0] + ' + ' + self.files[1]
            else:
                self.label['text'] = f'Please choose different file 2. \n File 1: {self.files[0]}'

    def label_func(self, info):
        self.label['text'] = info

    def status_func(self, info):
        self.label_process['text'] = info

    def open_folder(self):
        f = self.last_fld[:-1]
        fnx = f[::-1].find('/')
        f = f[-fnx:]
        if len(self.last_fld) > 0:
            try:
                call(["open", self.last_fld])
            except:
                path = os.path._getfullpathname(self.last_fld)
                os.system(f"explorer {path}")
        else:
            self.label_func('Choose a file first')

    def apply_filter(self, ):
        self.text_info = ''
        x = self.variable.get()
        if len(self.files) == 0:
            info = 'Choose files first'
            self.label_func(info)
        elif x == 'Choose filter:':
            info = f'Select a filter for the file [{self.files[0]}]'
            self.label_func(info)
        elif len(self.files) == 1 and x == 'LGE Raw':
            self.text_info= newlge_flt(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'ETA_Tracking':
            threading.Thread(target=self.eta_tracking, args=(self.files[0], self.folders[0])).start()
        elif len(self.files) == 1 and x == 'FRT Raw':
            self.text_info = self.frt_terminal(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'FTV Error':
            threading.Thread(target=self.ftv_error, args=(self.files[0], self.folders[0])).start()
        elif len(self.files) == 1 and x == 'LEAD Raw':
            self.text_info = lead_time(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'CONCAT':
            threading.Thread(target=self.exc_concat, args=(self.folders[0],)).start()
        elif len(self.files) == 1 and x == 'N1D_Raw':
            self.text_info = n1d_imdl(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'NTX_Raw':
            self.text_info = ntx_imdl(self.files[0], self.folders[0])
        elif len(self.files) == 1 and x == 'KPI_Orig':
            self.text_info = exc_kpi_orig(self.files[0], self.folders[0])
        elif len(self.files) == 2 and x == 'FTV Fnl_Sea':
            threading.Thread(target=self.ftv_seastock, args=(self.files, self.folders)).start()
        elif len(self.files) == 2 and x == 'Fdest All':
            self.text_info = self.fdest_all(self.files[0], self.files[1], self.folders[0])
        elif len(self.files) == 2 and x == 'KPI_KeyM':
            # threading.Thread(target=kpi_key_data, args=(self.files, self.folders)).start()
            self.text_info = kpi_key_data(self.files, self.folders)
        elif len(self.files) == 2 and x == 'KPI_ALL':
            threading.Thread(target=self.kpi_key_and_merge, args=(self.files, self.folders)).start()
        elif len(self.files) == 2 and x == 'FTV ERR_Sea':
            threading.Thread(target=self.ftv_seast_error, args=(self.files, self.folders)).start()
        elif len(self.files) == 2 and x == 'Concat_2f':
            threading.Thread(target=self.exc_concat_only2, args=(self.files, self.folders)).start()

        self.files, self.folders = [], []
        self.variable.set(self.OPTIONS[0])
        self.label_func(self.text_info)

    def eta_tracking(self,filename1, path1):
        filename = filename1
        path = path1
        print('Tracking ...')
        self.label_func('Tracking ...')
        LGE_path = path
        lge_raw = filename
        output_file = f'{LGE_path}{lge_raw[9:-5].strip()}_track_p.xlsx'
        start_t = time.time()

        # df = pd.read_excel(f'{LGE_path}{lge_raw}', sheet_name='data', na_filter=False)
        # df.insert(loc=14, column='MBL_4', value=df['Master B/L No'].astype(str).str[0:4])
        # df.insert(loc=15, column='MBL_KEY', value='')
        # df["MBL_KEY"] = df['Current Vessel'] + '_' + df['POD Port'] + '_' + df['MBL_4']
        # df["S_KEY"] = df['Current Vessel'] + df['POD Port']
        # df['New ETA'] = ''
        # df['ETA/ATA'] = ''
        # df = df[['Current Vessel', 'Carrier', 'Master B/L No', 'Container No', 'MBL_KEY', 'POD Port', 'S_KEY', 'MBL_4',
        #          'POD ETA', 'ETA/ATA', 'New ETA']]
        # df = df[df['MBL_4'].isin(non_tracks) == False]
        # df = df.drop_duplicates(subset=['MBL_KEY'])
        # df = df.drop_duplicates(subset=['S_KEY'])
        # total = len(df['Master B/L No'])

        df = pd.read_excel(f'{LGE_path}{lge_raw}', sheet_name='data', na_filter=False)
        df.insert(loc=14, column='MBL_4', value=df['MBL No'].astype(str).str[0:4])
        df.insert(loc=15, column='MBL_KEY', value='')
        df["MBL_KEY"] = df['Current Vessel'] + '_' + df['POD'] + '_' + df['MBL_4']
        df["S_KEY"] = df['Current Vessel'] + df['POD']
        df['New ETA'] = ''
        df['ETA/ATA'] = ''
        df = df[['Current Vessel', 'Carrier\nGrp', 'MBL No', 'CNTR No', 'MBL_KEY', 'POD', 'S_KEY', 'MBL_4',
                 'POD ETA', 'ETA/ATA', 'New ETA']]
        df = df[df['MBL_4'].isin(non_tracks) == False]
        df = df.drop_duplicates(subset=['MBL_KEY'])
        df = df.drop_duplicates(subset=['S_KEY'])
        total = len(df['MBL No'])

        print('Total: ', total, 'Est.time:', min_sec(total*9))
        est_info = f'Total: {total}, Est.time: {min_sec(total*9)}'
        threading.Thread(target=self.label_func, args=(est_info,)).start()

        eta_list = self.list_m(df)

        df['New ETA'] = eta_list[0]
        df['ETA/ATA'] = eta_list[1]
        df.to_excel(output_file, sheet_name='Contents', index=None)
        exec_time = time.time() - start_t
        print(f'File Saved : Time consumed: {min_sec(exec_time)} (Per cont: {min_sec(int(exec_time/total))})')
        info = f'File Saved \n Time consumed: {min_sec(exec_time)} ' \
               f'(Per cont: {min_sec(int(exec_time/total))}) \nEst.time: {min_sec(total*9)}'
        threading.Thread(target=self.status_func, args=('||',)).start()
        threading.Thread(target=self.label_func, args=(info,)).start()

    def list_m(self, df):
        my_l = []
        my_l_2 = []
        total_data = df.shape[0]
        for cont, key in zip(df['CNTR No'], df['MBL_4']):
            ea, eta = '-', '-'
            if key == 'ONEY':
                try:
                    eta_info = one_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'COSU':
                try:
                    eta_info = cosco_mbl_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'SMLM':
                try:
                    eta_info = sm_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key in apl_key :
                try:
                    eta_info = apl_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'MAEU' or key.isdigit():
                try:
                    eta_info = mae_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'EGLV':
                try:
                    eta_info = evg_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'MATS':
                try:
                    eta_info = mat_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key == 'SUDU':
                try:
                    eta_info = sud_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            # elif key == 'HLCU':
            #     try:
            #         eta_info = hap_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0]
            #     except:
            #         eta = '--'
            #         ea = '--'
            elif key in med_cont:
                try:
                    eta_info = med_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key in ww_key:
                try:
                    eta_info = ww_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            elif key in wan_key or cont[:4] in wan_cont:
                try:
                    eta_info = wan_track(cont)
                    eta, ea = eta_info[1], eta_info[0]
                except:
                    pass
            # elif cont[:4] == 'CCLU' or cont[:4] == 'OOCU':
            #     try:
            #         eta_info = cosco_mbl_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0] + '/COS'
            #     except:
            #         eta = '--'
            #         ea = '--'

            # elif cont[:4] in mae_cont:
            #     try:
            #         eta_info = mae_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0] + '/MAE'
            #     except:
            #         pass

            # elif cont[:4] == 'CMAU':
            #     try:
            #         eta_info = apl_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0] + '/APL'
            #     except:
            #         pass

            # elif cont[:4] in one_conts:
            #     try:
            #         eta_info = one_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0] + '/ONE'
            #     except:
            #         pass

            # if eta == '--':
            #     try:
            #         eta_info = one_track(cont)
            #         eta = eta_info[1]
            #         ea = eta_info[0] + '/ONE'
            #     except:
            #         eta = '--'
            #         ea = '--'
            my_l.append(eta)
            my_l_2.append(ea)
            cur_l = len(my_l)
            if len(my_l) % (total_data//5) == 0:
                completed = round((cur_l/total_data) * 100, 0)
                info = f'Tracking Progress: {cur_l} / {completed} %'
                stat = f'| Tracking: {cur_l} / {completed} %'
                print(info)
                threading.Thread(target=self.status_func, args=(stat,)).start()

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

    def open_pier(self ):
        fns_path = 'C:/Users/URAL KOZHOKMATOV/Documents/FNS/1 PIERPASS'
        try:
            call(["open", fns_path])
        except:
            path = os.path._getfullpathname(fns_path)
            os.system(f"explorer {path}")

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

    def exc_concat(self, path):
        cn_path = path
        print('Concatinating ...')
        self.label_func('Concatinating files ...')
        f_ndx = cn_path[-2::-1].find('/')
        prev_f = f'{cn_path[:-f_ndx - 1]}'
        output_name = f'{self.date_info}_raw_all.xlsx'
        output_path = f'{prev_f}{output_name}'
        files = os.listdir(cn_path)
        start = time.time()
        file_1 = files.pop(0)
        df = pd.read_excel(f'{cn_path}{file_1}', na_filter=False)
        i = 1
        fl_len= len(files)
        for file in files:
            self.status_func(f'| {round((i / fl_len) * 100, 0)}%')
            df_2 = pd.read_excel(f'{cn_path}{file}', na_filter=False)
            df = df.append(df_2)
            i += 1
        tt = df.shape[0]
        self.status_func(f'| Saving ...')
        df.to_excel(output_path, sheet_name='Data', index=None)
        self.status_func('|')
        end = time.time()
        exec_time = end - start
        print(f'Concat File saved. Total {tt}  // Time consumed: {min_sec(exec_time)}' )
        info = f'Concat File saved. Total {tt} \nTime consumed: {min_sec(exec_time)}'
        self.label_func(info)

    def kpi_key_and_merge(self, files, folders):
        """
        :param files: Raw KPI, Raw POD ETA file
        :param folders:
        :return: Merged File by Key
        """
        threading.Thread(target=self.status_func, args=('| KPI processing ...',)).start()
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

        txt_info = f"Total: {total}  (Cons.time {min_sec(end - bgn)})\n Y: {y_sum} ({y_prcnt}%) || N: {n_sum} ({n_prcnt}%) " \
                   f"\nNo Fdest Eta: {no_fdeta_sum} ({no_fdeta_prcnt}%)"
        threading.Thread(target=self.label_func, args=(txt_info,)).start()

        bgn = time.time()
        df2 = pd.read_excel(f'{folders[1]}{files[1]}', na_filter=False)
        df2.insert(loc=76, column='key', value='')
        df2['key'] = df2['MBL No'] + df2['HBL No'] + df2['CNTR No']

        threading.Thread(target=self.status_func, args=('| KPI Merging ...',)).start()

        df3 = df.merge(df2[['key', 'F.DEST ETA', 'F.DEST ATA', 'F.DEST ATA CRT']],
                       left_on='key', right_on='key', how='left', indicator=True)
        # df2.to_excel(f'{folders[1]}{files[1][:-5]}_key.xlsx', sheet_name='Data', index=None)

        threading.Thread(target=self.status_func, args=('| KPI Saving ...',)).start()

        df3.to_excel(f'{folders[0]}{files[0][:-5]}_k_merged.xlsx', sheet_name='Data', index=None)
        end = time.time()
        txt_info2 = f'KPI File Saved at {time.strftime("%H:%M")}  || Time cons: {min_sec(end - bgn)}'
        print(txt_info2)
        threading.Thread(target=self.label_func, args=(txt_info2,)).start()
        threading.Thread(target=self.status_func, args=('|',)).start()
        # final_info = f'Saved. Time cons: {min_sec(end - bgn)}'
        return

    def ftv_seastock(self, files, folders):
        file1 = files[0]
        folder1 = folders[0]
        sea_file = files[1]
        sea_folder = folders[1]
        threading.Thread(target=self.status_func, args=('| FTV final ...',)).start()
        start_t = time.time()

        dfs = pd.read_excel(f'{sea_folder}{sea_file}', na_filter=False)
        dfs = dfs[['Origin', 'CNTR#', 'House BL No']]
        dfs = dfs[dfs['Origin'] == "Ocean"]
        dfs = dfs[['CNTR#', 'House BL No']]
        cont_err = ('LCL', 'SEA')
        dfs = dfs[~dfs['CNTR#'].isin(cont_err)]
        dfs = dfs.drop_duplicates(subset=['CNTR#'])

        df = pd.read_excel(f'{folder1}{file1}', na_filter=False)
        df = df[['Mode', 'Shipper', 'Consignee', 'Division', 'P/O No', 'S/A No', 'House B/L No', 'Invoice No',
                 'Container No',
                 'Item', 'Master B/L No', 'Container Type', 'Incoterms', 'Carrier', 'Route', 'HOT Cntr', 'Diversion',
                 'Buyer', 'Terminal', 'Current Status', 'Current Port', 'Current Date', 'Current Vessel', 'Exception',
                 'Exception Status', 'EXF Port', 'EXF ATD', 'POL Mode', 'POL Port', 'POL Vessel', 'POL Initial ETD',
                 'POL ETD', 'POL ATD', 'TS1 Port', 'TS1 Vessel', 'TS1 ETA', 'TS1 ATA', 'TS1 ETD', 'TS1 ATD', 'TS2 Port',
                 'TS2 Vessel', 'TS2 ETA', 'TS2 ATA', 'TS2 ETD', 'TS2 ATD', 'TS3 Port', 'TS3 Vessel', 'TS3 ETA',
                 'TS3 ATA',
                 'TS3 ETD', 'TS3 ATD', 'POD Mode', 'POD Port', 'POD Carrier ETA', 'POD ETA', 'POD ATA', 'CY1 Port',
                 'CY1 ETA',
                 'CY1 ATA', 'CY1 Mode', 'CY1 ETD', 'CY1 ATD', 'CY2 Port', 'CY2 ETA', 'CY2 ATA', 'CY2 Mode', 'CY2 ETD',
                 'CY2 ATD', 'CY3 Port', 'CY3 ETA', 'CY3 ATA', 'CY3 Mode', 'CY3 ETD', 'CY3 ATD', 'Import Declaration',
                 'FDEST Mode', 'FDEST Port', 'FDEST Initial ETA', 'FDEST ETA', 'FDEST ATA', 'Remark']]

        df.loc[df['FDEST ETA'] == '', 'FDEST ETA'] = df['FDEST Initial ETA']
        df['FDEST ETA'] = pd.to_datetime(df['FDEST ETA'], format='%Y-%m-%d')
        df['FDEST ATA'] = pd.to_datetime(df['FDEST ATA'], format='%Y-%m-%d')
        df['CY1 ATD'] = pd.to_datetime(df['CY1 ATD'], format='%Y-%m-%d')

        df.replace({'Current Vessel': vessel_names}, inplace=True, regex=True)
        df.replace({'POL Vessel': vessel_names}, inplace=True, regex=True)
        df['Current Vessel'] = df['Current Vessel'].str.strip()

        dfs = dfs[~dfs['CNTR#'].isin(df['Container No'])]
        seas_cnts = len(dfs.index)

        dfs.to_excel(f'{sea_folder}p_Seastock_{current_date()[0]}.xlsx', sheet_name='Check', index=None)

        fd_ports = ('USXF7', 'USSBT')
        df2 = df[df['FDEST Port'].isin(fd_ports)]
        df2.loc[:,('FDATA-CY1ATD')] =(df2['FDEST ATA'].apply(lambda x: x.value) - df2['CY1 ATD'].apply(lambda x: x.value)) // (86400 * (10 ** 9))
        df2 = df2[['House B/L No', 'Container No', 'Master B/L No', 'CY1 ATD', 'FDEST ATA', 'FDATA-CY1ATD']]
        df2 = df2[df2['FDATA-CY1ATD'] < 0]
        df2.sort_values(by=['FDATA-CY1ATD'])
        total_data = len(df.index)
        errs = len(df2.index)

        df3 = df[df['FDEST Port'].isin(fd_ports)]
        df3 = df3[['House B/L No', 'Container No', 'Master B/L No', 'FDEST ETA', 'FDEST ATA']]
        df3 = df3[df3['House B/L No'].str.startswith('PLI')]
        df3 = df3[df3['FDEST ATA'] == '']

        self.text_info = f'FTV total {total_data} \nSeastock: {seas_cnts} // Err: {errs}'
        threading.Thread(target=self.label_func, args=(self.text_info,)).start()

        output_file = f'{folder1}FTV Original {current_date()[0]} Edited_p.xlsx'

        threading.Thread(target=self.status_func, args=('| FTV Saving ...',)).start()
        threading.Thread(target=fns_log_file, args=(f'FTV Total {total_data + seas_cnts} Ftv: {total_data} Seastock: {seas_cnts}',)).start()
        with pd.ExcelWriter(output_file) as writer:
            df.to_excel(writer, sheet_name='Contents', index=None)
            df2.to_excel(writer, sheet_name='CY1ATD', index=None)
            df3.to_excel(writer, sheet_name='FDETA', index=None)
        exec_time = time.time() - start_t
        threading.Thread(target=self.label_func, args=(f'Saved | Time cons: {min_sec(exec_time)} \n{self.text_info}',)).start()
        threading.Thread(target=self.status_func, args=('|',)).start()

    def ftv_seast_error(self, files, folders):
        threading.Thread(target=self.status_func, args=(f'| Err/Seastock ...',)).start()
        e_file = files[0]
        e_folder = folders[0]
        s_file = files[1]
        s_folder=folders[1]

        dfe = pd.read_excel(f'{e_folder}{e_file}', na_filter=False)
        dfe = dfe[['Mode', 'Shipper', 'Consignee', 'Division', 'P/O No', 'S/A No', 'House B/L No', 'Invoice No',
                 'Container No',
                 'Item', 'Master B/L No', 'Container Type', 'Incoterms', 'Carrier', 'Route', 'HOT Cntr', 'Diversion',
                 'Buyer', 'Terminal', 'Current Status', 'Current Port', 'Current Date', 'Current Vessel', 'Exception',
                 'Exception Status', 'EXF Port', 'EXF ATD', 'POL Mode', 'POL Port', 'POL Vessel', 'POL Initial ETD',
                 'POL ETD', 'POL ATD', 'TS1 Port', 'TS1 Vessel', 'TS1 ETA', 'TS1 ATA', 'TS1 ETD', 'TS1 ATD', 'TS2 Port',
                 'TS2 Vessel', 'TS2 ETA', 'TS2 ATA', 'TS2 ETD', 'TS2 ATD', 'TS3 Port', 'TS3 Vessel', 'TS3 ETA',
                 'TS3 ATA',
                 'TS3 ETD', 'TS3 ATD', 'POD Mode', 'POD Port', 'POD Carrier ETA', 'POD ETA', 'POD ATA', 'CY1 Port',
                 'CY1 ETA',
                 'CY1 ATA', 'CY1 Mode', 'CY1 ETD', 'CY1 ATD', 'CY2 Port', 'CY2 ETA', 'CY2 ATA', 'CY2 Mode', 'CY2 ETD',
                 'CY2 ATD', 'CY3 Port', 'CY3 ETA', 'CY3 ATA', 'CY3 Mode', 'CY3 ETD', 'CY3 ATD', 'Import Declaration',
                 'FDEST Mode', 'FDEST Port', 'FDEST Initial ETA', 'FDEST ETA', 'FDEST ATA', 'Remark']]
        dfs = pd.read_excel(f'{s_folder}{s_file}', na_filter=False)
        dfs = dfs[['CNTR#', 'House BL No']]

        dfs_na = dfs[~dfs['CNTR#'].isin(dfe['Container No'])]
        na_conts = len(dfs_na.index)

        dfe=dfe[dfe['Container No'].isin(dfs['CNTR#'])]
        dfe.replace({'Current Vessel': vessel_names}, inplace=True, regex=True)
        dfe.replace({'POL Vessel': vessel_names}, inplace=True, regex=True)
        dfe['Current Vessel'] = dfe['Current Vessel'].str.strip()

        dfe = dfe.drop_duplicates(subset=['Container No'])

        dfe['FDEST ETA'] = pd.to_datetime(dfe['FDEST ETA'], format='%Y-%m-%d')
        dfe['FDEST ATA'] = pd.to_datetime(dfe['FDEST ATA'], format='%Y-%m-%d')

        fnd_conts = len(dfe.index)

        self.text_info = f'Fnd conts: {fnd_conts} || NA conts: {na_conts}'

        threading.Thread(target=self.label_func, args=(f'Fnd conts: {fnd_conts} || NA conts: {na_conts}',)).start()
        threading.Thread(target=self.status_func, args=('| Saving ...',)).start()

        dfe.to_excel(f'{e_folder}{e_file[:-5]}_found_p.xlsx', index=None)

        with pd.ExcelWriter(f'{s_folder}{s_file}') as writer:
            dfs.to_excel(writer, sheet_name='Contents', index=None)
            dfs_na.to_excel(writer, sheet_name='NA_CNTR', index=None)

        threading.Thread(target=self.status_func, args=('||  ',)).start()

    def exc_concat_only2(self,files, folders):
        threading.Thread(target=self.status_func, args=('| Cncting 2 ...',)).start()
        file1 = files[0]
        file2 = files[1]
        folder1 = folders[0]
        folder2 = folders[1]
        df1 = pd.read_excel(f'{folder1}{file1}', na_filter=False)
        tt_1 = len(df1.index)
        df2 = pd.read_excel(f'{folder2}{file2}', na_filter=False)
        tt_2 = len(df2.index)
        df3 = pd.concat([df1, df2])
        tt_3 = len(df3.index)
        threading.Thread(target=self.label_func, args=(f'Total: {tt_3} / F1: {tt_1} / F2: {tt_2}',)).start()
        threading.Thread(target=self.status_func, args=('| Saving ... ',)).start()
        df3.to_excel(f'{folder1}{file1[:-5]}_cncted.xlsx', sheet_name='Contents',index=None)
        threading.Thread(target=self.status_func, args=('|| ',)).start()



if __name__ == '__main__':
    app = App()
    app.mainloop()