import tkinter as tk
import time
import os
from subprocess import call
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webtrack.Vetracker import vetrack

window = tk.Tk()
window.configure(background="#e6e6e6")
window.title("FNS: Container Tracking")
window.geometry("408x188")
p1 = tk.PhotoImage(file ='pics/cont.png')
window.iconphoto(False, p1)

label3 = tk.Label(
    text="Container No", bg='#e6e6e6', fg = '#595959', width=10, height=1)
label2 = tk.Label(
    text="Carrier", bg='#e6e6e6', fg='#595959', width = 10, height=1)

text_t = tk.Text(window, bg='#cccccc', fg='black', width = 50, height=7,)
container = tk.Entry(bd=1, bg='#d9d9d9', width='40')
carr = tk.Entry(bd=1, width='10', bg = '#d9d9d9',)


def text_out(info):
    text_t.delete(1.0,'end')
    text_t.insert('1.0', f'\n{info}')

def notes():
    pdf_f = 'pics/notes.txt'
    try:
        call(["open", pdf_f])
    except:
        path = os.path._getfullpathname(pdf_f)
        os.system(f"explorer {path}")

init=  ' ap (CMA CGM), on (ONE),     sd (HamburgSud), ' \
     '\n ma (Maersk),  mt (Matson),  ww (Westwood),' \
     '\n cs (Cosco),   sm (SM Line), wn (Wanhai)' \
     '\n hp (Hapag),   ec (ECUWorld) eg (Evergreen)'

text_out(init)

class Tracking:

    def __init__(self):
        timer = datetime.date.today()
        exp_d = datetime.date(2022,5,10)
        if timer < exp_d:
            cont = container.get().strip()
            carrier = carr.get().strip().lower()
            if carrier == 'sm':
                self.sm_track(cont)
            elif carrier == 'on':
                self.one_track(cont)
            elif carrier == 'ap':
                self.apl_track(cont)
            elif carrier == 'ma':
                self.mae_track(cont)
            elif carrier == 'cs':
                self.cosco_mbl_track(cont)
            elif carrier == 'mt':
                self.mat_track(cont)
            elif carrier == 'ww':
                self.ww_track(cont)
            elif carrier == 'sd':
                self.sud_track(cont)
            elif carrier == 'wn':
                self.wan_track(cont)
            elif carrier == 'hp':
                self.hap_track(cont)
            elif carrier == 'md':
                self.med_track(cont)
            elif carrier == 'ec':
                self.ecu_track(cont)
            elif carrier == 'eg':
                self.evg_track(cont)
            elif carrier == 'ves':
                text_out(vetrack(cont))
            else:
                info = 'Please enter valid values'
                text_out(info)
        else:
            text_out('Program is expired')

    @staticmethod
    def cosco_mbl_track(cont):
        dr = webdriver.Chrome()
        web = 'https://elines.coscoshipping.com/ebusiness/'
        dr.get(web)
        dr.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button').click()
        info_text = []
        if len(cont) != 14:
            dr.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/ul/li[3]').click()
            dr.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/form/div/div/div[1]/input').send_keys(
                cont)
        else:
            dr.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/ul/li[2]').click()
            dr.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/form/div/div/div[1]/input').send_keys(
                cont[4:])
        dr.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/a').click()
        time.sleep(1)
        if len(cont) != 14:
            pod, eta2, eta_a, vessel = '-', '-', '-', '-'
            try:
                path_1 = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]'
                '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]'
                WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_1)))
                eta = dr.find_element_by_xpath(path_1).text
                eta = eta.replace('\n', ' ')[:14]
                eta = eta[4:]
            except:
                eta = 'No data'

            try:
                vessel_btn = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/ul/li[2]/div[3]/div/div[4]/div/div/div/div[1]/div/div'
                dr.find_element_by_xpath(vessel_btn).click()
                row = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/ul/li[2]/div[3]/div/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/'
                row_01 = f'{row}div[1]/div[1]'
                i = 1
                while i > 0:
                    row_01 = f'{row}div[{i}]/div[1]'
                    row_02 = f'{row}div[{i}]/div[2]'
                    try:
                        WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, row_01)))
                        col_1 = dr.find_element_by_xpath(row_01).text
                    except:
                        break
                    if 'ETA' in col_1:
                        eta2 = dr.find_element_by_xpath(row_02).text
                    if 'ATA' in col_1:
                        eta_a = dr.find_element_by_xpath(row_02).text
                    if 'POD' in col_1:
                        pod = dr.find_element_by_xpath(row_02).text
                    if 'Vessel' in col_1:
                        vessel = dr.find_element_by_xpath(row_02).text
                        break
                    i += 1
            except:
                eta2 = 'No data'
                vessel = '--'
                eta_a = '--'
            dr.quit()
            eta = eta2 if 'No' not in eta2 else eta
            if len(eta_a) > 4:
                info_text.append(f'ATA: {eta_a[:10]}')
            else:
                info_text.append(f'ETA: {eta[:10]}')
            info_text.append(f'POD: {pod}')
            info_text.append(f'Vessel: {vessel}')
            text_info = ''
            for i in info_text:
                text_info += i +'\n'
            text_out(text_info)

        else:
            time.sleep(1)
            try:
                term = dr.find_element_by_xpath(
                    '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[3]/div[4]').text
            except:
                term = '-'
            try:
                vessel = dr.find_element_by_xpath(
                    '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[4]/div[2]').text
                vessel.find('/')
                vessel = vessel[:vessel.find('/')]
            except:
                vessel = '-'

            try:
                firms_code = dr.find_element_by_xpath(
                    '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div[5]/div[4]').text
            except:
                firms_code = '(not found)'
            try:
                try:
                    pod_vessel = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[2]/td[1]').text
                    pod_port = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[2]/td[6]').text
                    eta_ata = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[2]/td[7]').text
                except:
                    pod_vessel = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[1]/td[1]').text
                    pod_port = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[1]/td[6]').text
                    eta_ata = dr.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div[2]/table/tbody/tr[1]/td[7]').text
                eta_ata.replace('\n', ' ')
                ata_x = eta_ata.find('actual')
                eta_ = eta_ata[:19].replace('expected:', '')
                ata_ = eta_ata[ata_x:].replace('actual:', '')[:10]

                if len(ata_) > 2:
                    info_text.append(f'{pod_port} ATA: {ata_}')
                else:
                    info_text.append(f'{pod_port} ETA: {eta_}')

                info_text.append(f'POL Vessel: {vessel} \nPOD Vessel: {pod_vessel}')
                term = term.replace(f'{pod_port}', '').replace('-', '').strip()
                info_text.append(f'Term: {term} | {firms_code}')
            except:
                info_text = 'No data'
            dr.quit()

            if 'No data' not in info_text:
                text_info = ''
                for i in info_text:
                    text_info += i +'\n'
                text_out(text_info)
            else:
                text_out(info_text)

    @staticmethod
    def sm_track(cont):
        dr = webdriver.Chrome()
        web = 'https://esvc.smlines.com/smline/CUP_HOM_3301.do?sessLocale=en'
        dr.get(web)
        dr.find_element_by_id('searchType').send_keys('Container No.')
        dr.find_element_by_id('searchName').send_keys(cont)
        dr.find_element_by_id('btnSearch').click()
        status, loc_, e_ata, e_date, ea = '', '', '', '', '',

        try:
            path_1 = '/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[1]/td[2]'
            WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_1)))
            for i in range(1, 11):
                status = dr.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[2]').text
                e_date = dr.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[4]').text
                e_ata = dr.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[4]/img').get_attribute('alt')
                loc_ = dr.find_element_by_xpath(
                    f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[3]').text
                berth = status.find('Berthing ')
                if berth >= 0:
                    break
            if e_ata.find('Actual') >= 0:
                ea = 'ATA'
            else:
                ea = 'ETA'
            st_inx = status.find('POD Berthing')
            status = status[:st_inx]
            loc_ = loc_.replace('UNITED STATES', '')
            info_all = ea + ' ' + e_date[:10] + ' ' + loc_ + '\nVessel: ' + status
        except:
            info_all = 'No data. Check container No or Carrier'
        dr.quit()
        text_out(info_all)

    @staticmethod
    def one_track(cont):
        dr = webdriver.Chrome()
        dr.minimize_window()
        one = 'https://ecomm.one-line.com/ecom/CUP_HOM_3301.do?sessLocale=en'
        dr.get(one)
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.ID, 'searchType')))
        dr.find_element_by_id('searchType').send_keys('Container No.')
        dr.find_element_by_id('searchName').send_keys(cont)
        dr.find_element_by_id('btnSearch').click()
        eta = eta_t = text = ''
        i = 1
        l_vsl = []
        pod = status = ''
        while True:
            try:
                path_i = f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i}]/td[2]'
                WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, path_i)))
                status = dr.find_element_by_xpath(path_i).text
                if 'Loaded on' in status:
                    l_vsl.append(status)
                if 'Arrival at Port of Discharging' in status:
                    status = dr.find_element_by_xpath(
                        f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i + 1}]/td[2]').text
                    pod = dr.find_element_by_xpath(
                        f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i + 1}]/td[3]').text
                    eta = dr.find_element_by_xpath(
                        f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i + 1}]/td[4]').text
                    break
                else:
                    i += 1
            except:
                text = 'No data'
                break
        dr.quit()

        if 'No data' not in text:
            pol_vsl = l_vsl[0].replace('\n', ' ')
            l_x = pol_vsl.find("'")
            pol_vsl = pol_vsl[l_x + 1:]
            sl_x = pol_vsl.find("'")
            pol_vsl = pol_vsl[:sl_x]
            pol_vsl = pol_vsl[:-4]

            if 'Actual' in eta:
                eta_t = 'ATA'
            else:
                eta_t = 'ETA'
            eta = eta.replace('Estimate', '').replace('Actual', '').strip()[:10]
            pod = pod.replace('UNITED STATES', '')
            stat_idx = status.find('POD Berthing')
            status = status[:stat_idx].replace("'", '')
            text = eta_t + ': ' + eta + '\n' + pod + '\n' + 'Vessel : ' + status[:-5] + '\n' + 'POL Vsl: ' + pol_vsl
        text_out(text)

    @staticmethod
    def apl_track(cont):
        dr = webdriver.Chrome()
        dr.minimize_window()
        apl = 'https://www.apl.com/ebusiness/tracking'
        dr.get(apl)
        dr.find_element_by_id('Reference').send_keys(cont)
        dr.find_element_by_id('btnTracking').click()
        text = eadate = pod = vessel = ''
        ea = 'ETA'
        base_path = '/html/body/div[2]/main/section[2]/div/div/div[2]/table/tbody/'
        WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, f'{base_path}tr[1]')))
        try:
            i = 1
            while True:
                moves = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[2]').text
                if moves == "DISCHARGED":
                    ea = 'ATA'
                    break
                elif moves == "ARRIVAL FINAL PORT OF DISCHARGE":
                    break
                i += 1
            eadate = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[1]').text
            pod = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[3]').text
            vessel = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[4]').text
            podx = pod.find(',')
            if podx > 0:
                pod = pod[:podx]
            inx = eadate.find(',')
            eadate = eadate[inx + 2:-5]
            text = f' {ea} : {eadate} \n {pod} : {vessel}'
        except:
            text = 'No results found'
        dr.quit()
        text_out(text)

    @staticmethod
    def mae_track(cont):
        pod = ('Los Angeles', 'Long Beach', 'Oakland', 'Savannah', 'Mobile', 'Houston', 'Wilmington', 'Prince Rupert',
               'Charleston', 'Norfolk', 'Miami', 'New Orleans', 'Jacksonville', 'Newark', 'Tampa', 'Vancouver',
               'Baltimore', 'Seattle', 'Charleston North')
        dr = webdriver.Chrome()
        maersk = f'https://www.maersk.com/tracking/{cont}'
        dr.get(maersk)
        e_ata = disc_date = pod_loc = vessel = ''
        try:
            btn_path = '/html/body/div[1]/div/div/div[1]/div[2]/button[3]'
            WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, btn_path)))
            dr.find_element_by_xpath(btn_path).click()
        except:
            pass
        info1 = ''
        try:
            # WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'button__text')))
            # dr.find_element_by_class_name('button__text').click()
            path_info = '/html/body/main/div/div/div[3]/div/div[1]/div[1]'
            WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_info)))
            div_num = 0
            for i in range(1, 14):
                div_num = i
                pod_loc = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[1]').text
                disc_date = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[3]').text
                e_ata = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[2]').get_attribute(
                    "class")
                d_inx = disc_date.find('\n')
                disc_date = disc_date[d_inx + 1:d_inx + 12]
                if 'icon-completed' in e_ata:
                    e_ata = 'ATA'
                else:
                    e_ata = 'ETA'
                inx = pod_loc.find('\n')
                pod_loc = pod_loc.replace('\n', ' ')
                if pod_loc[:inx] in pod:
                    break
            if div_num < 3:
                vessel = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{div_num - 1}]/div[3]').text
            else:
                vessel = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{div_num - 1}]/div[2]').text
                if 'Load on' not in vessel:
                    vessel = dr.find_element_by_xpath(
                        f'/html/body/main/div/div/div[3]/div/div[{div_num - 2}]/div[3]').text
            v_inx = vessel.find('/')
            vessel = vessel[:v_inx].replace('Load on', '').strip()
        except:
            info1 = 'No data, please check Container No or Carrier'
        if info1.find('No data') >= 0:
            info1 = info1
        else:
            info1 = e_ata + ': ' + disc_date + '\n' + pod_loc + '\nVessel: ' + vessel
        dr.quit()
        text_out(info1)

    @staticmethod
    def mat_track(cont):
        dr = webdriver.Chrome()
        dr.minimize_window()
        mats = 'https://www.matson.com/shipment-tracking.html'
        dr.get(mats)
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.ID, 'track-number-top')))
        dr.find_element_by_id('track-number-top').send_keys(cont)
        dr.find_element_by_id('track-submit-top').click()
        ea, eta, table = '-', '-', '-'
        path_1 = '/html/body/div[1]/div[3]/div[2]/main/div/article/div/div[4]/div/div[3]/table/tbody/tr[2]/td/table/tbody[1]/tr[2]/td/table/tbody/tr[1]'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_1)))
        for i in range(1, 10):
            try:
                table = dr.find_element_by_xpath(
                    f'/html/body/div[1]/div[3]/div[2]/main/div/article/div/div[4]/div/div[3]/table/tbody/tr[2]/td/table/tbody[1]/tr[2]/td/table/tbody/tr[{i}]'
                ).text
                indx = table.find('DISCHARGE FROM VESSEL')
                if indx >= 0:
                    ea = 'ATA'
                    eta = table[:indx]
                    break
            except:
                table = '-'
        if table == '-':
            info = dr.find_element_by_id('shipmentTrackingDetails').text
            eta_ind = info.find('VESSEL ETA')
            eta = info[eta_ind:eta_ind + 22].replace('  ', ' ').replace('  ', ' ')
            end_ = eta.find('ETA')
            ea = 'ETA'
            eta = eta[end_ + 4:].replace(' ', '')
        dr.quit()
        i_info = ea +': '+ eta
        text_out(i_info)

    @staticmethod
    def ww_track(cont):
        dr = webdriver.Chrome()
        # dr.minimize_window()
        webs = 'https://www.wsl.com/Tracking/Public'
        dr.get(webs)
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.ID, 'txContainerNumbers')))
        dr.find_element_by_id('txContainerNumbers').send_keys(cont)
        dr.find_element_by_xpath('/html/body/div[2]/main/form/div/div/div[1]/div/div[2]/div/button').click()
        tab_path = '/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[1]/td[3]'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, tab_path)))
        try:
            i = 1
            while True:
                info1 = dr.find_element_by_xpath(
                    f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[3]').text
                if ('Estimated arrival' in info1) or ('Arrived at POD' in info1):
                    break
                elif i == 10:
                    break
                i += 1
            event = dr.find_element_by_xpath(
                f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[3]').text
            date = dr.find_element_by_xpath(
                f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[4]').text
            pod = dr.find_element_by_xpath(
                f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[2]').text
            event = event.replace('Estimated arrival at POD', '\n ETA')
            event = event.replace('Arrived at POD', '\n ATA')
            info1 = f'{event}: {date} | {pod}'
        except:
            info1 = 'No data'
        dr.quit()
        text_out(info1)

    @staticmethod
    def sud_track(cont):
        info_text = []
        dr = webdriver.Chrome()
        dr.minimize_window()
        webs = 'https://www.hamburgsud-line.com/linerportal/pages/hsdg/tnt.xhtml?lang=en'
        dr.get(webs)
        send_path = '/html/body/main/div/div/form/div[2]/div[1]/div[1]/div[2]/textarea'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, send_path)))
        dr.find_element_by_xpath('/html/body/main/div/div/form/div[2]/div[1]/div[1]/div[2]/textarea').send_keys(cont)
        dr.find_element_by_xpath('/html/body/main/div/div/form/div[2]/div[1]/div[2]/div[2]/button').click()
        path_info = '/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[1]/td[3]'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_info)))
        try:
            for i in range(1, 6):
                info1 = dr.find_element_by_xpath(
                    f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[3]').text
                eta = dr.find_element_by_xpath(
                    f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[1]').text
                pod = dr.find_element_by_xpath(
                    f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[2]').text
                vessel = dr.find_element_by_xpath(
                    f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[4]').text
                vessel = vessel.replace('\n', ' ')

                indx = info1.find('Estimated vessel arrival')
                indx2 = info1.find('Discharged from vessel')
                if indx >= 0:
                    info1 = info1.replace('Estimated vessel arrival', 'ETA: ')
                    eta = info1 + eta[:11]
                    info_text.append(eta)
                    info_text.append(f'POD: {pod}')
                    info_text.append(f'Vessel: {vessel}')
                    break
                elif indx2 >= 0:
                    info1 = info1.replace('Discharged from vessel', 'ATA: ')
                    eta = info1 + eta[:11]
                    info_text.append(eta)
                    info_text.append(f'POD: {pod}')
                    info_text.append(f'Vessel: {vessel}')
                    break
                else:
                    info_1 = dr.find_element_by_xpath(
                        f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[1]/td[3]').text
                    info_text.append(info_1)
        except:
            info_text.append('No data, please check Container No or Carrier')
        dr.quit()
        i_info =''
        for i in info_text:
            i_info += i + '\n'
        text_out(i_info)

    @staticmethod
    def wan_track(cont):
        dr2 = webdriver.Chrome()
        webs = 'https://www.wanhai.com/views/cargoTrack/CargoTrack.xhtml?file_num=65580&parent_id=64738&top_file_num=64735'
        dr2.get(webs)
        WebDriverWait(dr2, 5).until(EC.presence_of_element_located((By.ID, 'Query')))
        dr2.find_element_by_id('q_ref_no1').send_keys(cont)
        dr2.find_element_by_id('Query').click()
        dr2.switch_to.window(dr2.window_handles[1])
        more_d = '/html/body/div[2]/div[1]/div/form/table/tbody/tr[2]/td[1]/u'
        try:
            WebDriverWait(dr2, 5).until(EC.presence_of_element_located((By.XPATH, more_d)))
        except:
            dr2.quit()
            info = 'No data'
            text_out(info)
            return
        dr2.find_element_by_xpath(more_d).click()
        dr2.switch_to.window(dr2.window_handles[2])
        pod_path = '/html/body/div[2]/div[1]/div/form/table[3]/tbody/tr[3]/td[1]'
        vess_path = '/html/body/div[2]/div[1]/div/form/table[3]/tbody/tr[3]/td[2]'
        WebDriverWait(dr2, 5).until(EC.presence_of_element_located((By.XPATH, vess_path)))

        arr_eta = '/html/body/div[2]/div[1]/div/form/table[3]/tbody/tr[3]/td[3]'
        ar_eta = dr2.find_element_by_xpath(arr_eta).text
        pod = dr2.find_element_by_xpath(pod_path).text
        vessel = dr2.find_element_by_xpath(vess_path).text
        v_idx = vessel.find('/')
        vessel = vessel[:v_idx]
        arrival_date, tod_ = '', ''
        if len(ar_eta) > 4:
            c_year = int(ar_eta[:4])
            c_month = int(ar_eta[5:7])
            c_day = int(ar_eta[-2:])
            tod_ = datetime.date.today()
            arrival_date = datetime.date(c_year,c_month,c_day)

        if len(ar_eta) > 4 and arrival_date > tod_:
            info = f' {pod}: {ar_eta} \n Vessel: {vessel}'
            text_out(info)
            dr2.quit()
            return
        else:
            vess_link = '/html/body/div[2]/div[1]/div/form/table[4]/tbody/tr[3]/td[5]/u'
            dr2.find_element_by_xpath(vess_link).click()
            dr2.switch_to.window(dr2.window_handles[3])
            time.sleep(1)
            etb_path = '/html/body/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[6]'
            eta_p = '/html/body/div[2]/div[1]/div/table[2]/tbody/tr[4]/td[4]'
            try:
                WebDriverWait(dr2, 5).until(EC.presence_of_element_located((By.XPATH, etb_path)))
                eta = dr2.find_element_by_xpath(eta_p).text
                etb = dr2.find_element_by_xpath(etb_path).text
            except:
                info = f' {pod}: {ar_eta} \n Vessel: {vessel}'
                text_out(info)
                dr2.quit()
                return
            if len(etb) > 4:
                eta = f'ETB {etb}'
            else:
                eta = f'ETA {eta}'
            # 2021/10/03
            info = f' {pod}: {eta} \n Vessel: {vessel}'
            dr2.quit()
            text_out(info)

    @staticmethod
    def hap_track(cont):
        dr = webdriver.Chrome()
        webs = 'https://www.hapag-lloyd.com/en/online-business/track/track-by-container-solution.html'
        dr.get(webs)
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.ID, 'accept-recommended-btn-handler')))
        dr.find_element_by_id('accept-recommended-btn-handler').click()
        dr.find_element_by_xpath(
            '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'
        ).clear()
        dr.find_element_by_xpath(
            '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'
        ).send_keys(cont)
        dr.find_element_by_xpath(
            '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[4]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/button'
        ).click()
        pol_v = []
        try:
            info_path = '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table'
            WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, info_path)))
            i = 1
            path_t = '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/'
            while True:
                status = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[1]').text
                place = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[2]').text
                if 'Loaded' in status:
                    pol_vsl = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[5]').text
                    pol_v.append(pol_vsl)
                if 'Vessel arrival' in status and ',' in place:
                    break
                elif 'Vessel arrived' in status and ',' in place:
                    break
                elif i == 20:
                    break
                i += 1
            pod = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[2]').text
            pod = pod[:pod.find(',')]
            pod_vl = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[5]').text
            date = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[3]').text
            eta = 'ETA' if 'Vessel arrival' in status else 'ATA'
            info = f'{pod} | {eta} {date} \nPOD VSL: {pod_vl} \nPOL VSL: {pol_v[0]}'
        except:
            info = 'No data, please check Container No or Carrier'
        dr.quit()
        text_out(info)

    @staticmethod
    def med_track(cont):
        web = 'https://www.msc.com/track-a-shipment'
        dr = webdriver.Chrome()
        # dr.minimize_window()
        dr.get(web)
        us_btn = '/html/body/div[1]/div/a[1]'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, us_btn)))
        dr.find_element_by_xpath(us_btn).click()

        cnt_inp = '/html/body/form/div[4]/div/div[3]/main/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div[2]/input'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, cnt_inp)))
        dr.find_element_by_xpath(cnt_inp).send_keys(cont)
        search_btn = '/html/body/form/div[4]/div/div[3]/main/div/div[1]/div/div/div[1]/div/div/div/div[3]/a'
        dr.find_element_by_xpath(search_btn).click()

        row_tb = '/html/body/form/div[4]/div/div[3]/main/div/div[2]/div/div/div[2]/dl/dd/div/dl/dd/div/table[2]/tbody'
        WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, row_tb)))

        i = 1
        while True:
            try:
                descr = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[2]').text
                if 'Estimated' in descr:
                    break
                elif 'Discharged' in descr:
                    break
                elif i == 5:
                    break
            except:
                descr = 'No data'
                dr.quit()
                break
            i += 1
        if "No data" not in descr:
            pod = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[1]').text
            eta_d = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[3]').text
            vessel = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[4]').text
            ea = 'ETA' if 'Estimated' in descr else 'ATA'
            info = f'{pod} {ea} {eta_d} \nVessel: {vessel}'
        else:
            info = descr
        dr.quit()
        text_out(info)

    @staticmethod
    def ecu_track(cont):
        dr = webdriver.Chrome()
        web = 'https://tnt.ecuworldwide.com/#/maindashBoard'
        dr.get(web)

        search_inp = '/html/body/section/div/div/div/div[1]/div/div[1]/div[2]/div[1]/input'
        WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, search_inp)))
        dr.find_element_by_xpath(search_inp).send_keys(cont)

        search_btn = '/html/body/section/div/div/div/div[1]/div/div[1]/div[2]/div[2]/button'
        dr.find_element_by_xpath(search_btn).click()

        try:
            last_evnt = '/html/body/section/div/div/div/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/ul/li[1]/div'
            WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, last_evnt)))
            last_event = dr.find_element_by_xpath(last_evnt).text
        except:
            text_out('No data')
            dr.quit()
            return

        detail_li = '/html/body/section/div/div/div/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/ul/'
        i = 1
        while True:
            pol_vs = dr.find_element_by_xpath(f'{detail_li}li[{i}]').text
            if 'DEP Vessel' in pol_vs:
                break
            i += 1
        pol_vs = pol_vs.replace('\n', ': ')
        info = last_event +'\n'+ pol_vs
        dr.quit()
        text_out(info)

    @staticmethod
    def evg_track(cont):
        if len(cont) == 11:
            check_cont = '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[1]'
        else:
            cont = cont[4:]

        web = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
        dr = webdriver.Chrome()
        dr.get(web)
        dr.minimize_window()
        inp_con = '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]'
        WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, inp_con)))
        dr.find_element_by_xpath(inp_con).send_keys(cont)
        sub_btn = '/html/body/div[4]/center/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]'
        if len(cont) == 11:
            WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, check_cont)))
            dr.find_element_by_xpath(check_cont).click()
        dr.find_element_by_xpath(sub_btn).click()
        info = ''
        time.sleep(0.2)

        if len(cont) == 11:
            vess_path = '/html/body/div[5]/center/table[2]/tbody/tr/td/table[1]/tbody/tr/td[3]'
            try:
                vessel = dr.find_element_by_xpath(vess_path).text
                v_idx = vessel.find('-')
                vessel = vessel[:v_idx]
                date_path = '/html/body/div[5]/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td'
                date = dr.find_element_by_xpath(date_path).text
                date = date.replace('\n', '').replace('Estimated Date of Arrival :', '')
                info = f'ETA: {date}\nVESSEL: {vessel}'
                dr.quit()
            except:
                info = 'No Data'
                dr.quit()
        else:
            try:
                table = '/html/body/div[5]/center/table[2]/tbody/tr/td/table[6]/tbody'
                t_info = dr.find_element_by_xpath(table).text.split('\n')[-1]
                t_info1 = t_info.split(' ')
                info1 = [i.strip() for i in t_info1 if len(i) > 2]
                inx1 = t_info.find(')')
                inx2 = t_info[::-1].find(' ')
                vess = t_info[inx1+1:-inx2].strip()
                eta, pod = info1[0], info1[1].replace(',', '')
                dr.quit()
                info = f'{pod} ETA: {eta} \nVessel: {vess}'
            except:
                cont_link = '/html/body/div[5]/center/table[2]/tbody/tr/td/table[3]/tbody/tr[3]/td[1]/a'
                dr.find_element_by_xpath(cont_link).click()
                dr.switch_to.window(dr.window_handles[1])
        text_out(info)

button = tk.Button(
    text='Search', height=1, width=22, bg='#cccccc', fg='black', command=Tracking)

button2 = tk.Button(
    text='Note',border=0, height=1, bg='#e6e6e6', fg='#737373', command=notes)
button2.place(x=355, y=10)

container.place(x=100, y=11)
label3.place(x=10, y=10)

carr.place(x=100, y=41)
label2.place(x=10, y=40)

button.place(x=180, y=37)
text_t.place(x=2, y=70)



window.mainloop()
