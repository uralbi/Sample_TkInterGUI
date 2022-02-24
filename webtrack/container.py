import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def one_track(cont):
    dr = webdriver.Chrome()
    dr.minimize_window()
    one = 'https://ecomm.one-line.com/ecom/CUP_HOM_3301.do?sessLocale=en'
    dr.get(one)
    WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.ID, 'searchType')))
    dr.find_element_by_id('searchType').send_keys('Container No.')
    dr.find_element_by_id('searchName').send_keys(cont)
    dr.find_element_by_id('btnSearch').click()
    eta = eta_t = text = ''
    i = 1
    while True:
        try:
            path_i = f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i}]/td[2]'
            WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, path_i)))
            status = dr.find_element_by_xpath(path_i).text
            if 'Arrival at Port of Discharging' in status:
                eta = dr.find_element_by_xpath(
                    f'/html/body/div[3]/div[2]/div/form/div[8]/table/tbody/tr[{i + 1}]/td[4]').text
                break
            else:
                i += 1
        except:
            eta, eta_t = '--', '--'
            break
    dr.quit()
    if '--' not in eta_t:
        if 'Actual' in eta:
            eta_t = 'ATA'
        else:
            eta_t = 'ETA'
        eta = eta.replace('Estimate', '').replace('Actual', '').strip()[:10]
        # pod = pod.replace('UNITED STATES', '')
        # stat_idx = status.find('POD Berthing')
        # status = status[:stat_idx].replace("'", '')
        # text = eta_t + ': ' + eta + '\n' + pod + '\n' + 'Vessel: ' + status
    return eta_t, eta


def cosco_mbl_track(cont):
    dr = webdriver.Chrome()
    web = 'https://elines.coscoshipping.com/ebusiness/'
    dr.get(web)
    dr.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button').click()
    info_text = []
    if len(cont) != 14:
        dr.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/ul/li[3]').click()  # choose container
        dr.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/form/div/div/div[1]/input').send_keys(
            cont)
        time.sleep(0.5)
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
        eta2, eta_a, vessel = '-', '-', '-'
        try:
            path_1 = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]'
            '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[2]'
            WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_1)))
            eta = dr.find_element_by_xpath(path_1).text
            eta = eta.replace('\n', ' ')[:14]
            eta1 = eta[4:]
        except:
            eta1 = 'No data'

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
                    eta = dr.find_element_by_xpath(row_02).text
                if 'ATA' in col_1:
                    eta = dr.find_element_by_xpath(row_02).text
                if 'Vessel' in col_1:
                    break
                i += 1
        except:
            eta = 'No data'
            eta_a = '--'

        eta = eta1 if 'No' not in eta else eta
        if len(eta_a) > 4:
            eta = eta_a[:10]
            ea = 'ATA'
        else:
            eta = eta[:10]
            ea = 'ETA'
        return ea, eta
    else:
        eta_path = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div[3]/div[3]'
        WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, eta_path)))
        eta = dr.find_element_by_xpath(eta_path).text

        eta2_path = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div[4]/div[3]'
        WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, eta2_path)))
        eta2 = dr.find_element_by_xpath(eta2_path).text
        if eta.find('Last POD') >= 0:
            info_text.append(eta.replace('\n', ' '))
        index_ = eta2.find('Last POD')
        if index_ >= 0:
            info_text.append(eta2.replace('\n', ' '))
        dr.quit()
        eta_info = info_text[0]
        end_ = eta_info.find('ETA')
        ea = 'ETA'
        if end_ < 0:
            end_ = eta_info.find('ATA')
            ea = 'ATA'
        eta_info = eta_info[end_+4:end_+14]

        return ea, eta_info


def sm_track(cont):
    dr = webdriver.Chrome()
    dr.minimize_window()
    web = 'https://esvc.smlines.com/smline/CUP_HOM_3301.do?sessLocale=en'
    dr.get(web)
    dr.find_element_by_id('searchType').send_keys('Container No.')
    dr.find_element_by_id('searchName').send_keys(cont)
    dr.find_element_by_id('btnSearch').click()
    # time.sleep(1.5)
    status, loc_, e_ata, e_date, ea = '', '', '', '', '',

    path_1 = '/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[1]/td[2]'
    WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, path_1)))

    for i in range(1, 11):
        status = dr.find_element_by_xpath(
            f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[2]').text
        e_date = dr.find_element_by_xpath(
            f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[4]').text
        e_ata = dr.find_element_by_xpath(
            f'/html/body/div[1]/div/div[2]/div[2]/form/div[7]/table/tbody/tr[{i}]/td[4]/img').get_attribute('alt')
        berth = status.find('Berthing ')
        if berth >= 0:
            break
    dr.quit()
    ata_ind = e_ata.find('Actual')
    if ata_ind >= 0:
        ea = 'ATA'
    else:
        ea = 'ETA'
    e_date = e_date[:10]
    return ea, e_date


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
        # pod = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[3]').text
        # vessel = dr.find_element_by_xpath(f'{base_path}tr[{i}]/td[4]').text
        # podx = pod.find(',')
        # if podx > 0:
        #     pod = pod[:podx]
        inx = eadate.find(',')
        eadate = eadate[inx + 2:-5]
    except:
        eadate = '--'
    dr.quit()
    return ea, eadate


def mae_track(cont):
    pod = ('Los Angeles', 'Long Beach', 'Oakland', 'Savannah', 'Mobile', 'Houston', 'Wilmington', 'Prince Rupert',
           'Charleston', 'Norfolk', 'Miami', 'New Orleans', 'Jacksonville', 'Newark', 'Tampa', 'Vancouver',
           'Baltimore','Seattle', 'Charleston North')
    dr = webdriver.Chrome()
    maersk = f'https://www.maersk.com/tracking/{cont}'

    dr.get(maersk)
    try:
        btn_path = '/html/body/div[1]/div/div/div[1]/div[2]/button[3]'
        WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, btn_path)))
        dr.find_element_by_xpath(btn_path).click()
    except:
        pass
    info1 = ''
    e_ata, eta = '-', '-'
    try:
        # WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'button__text')))
        # dr.find_element_by_class_name('button__text').click()
        path_info = '/html/body/main/div/div/div[3]/div/div[1]/div[1]'
        WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.XPATH, path_info)))
        for i in range(1, 14):
            pod_loc = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[1]').text
            disc_date = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[3]').text
            e_ata = dr.find_element_by_xpath(f'/html/body/main/div/div/div[3]/div/div[{i}]/div[2]').get_attribute(
                "class")
            d_inx = disc_date.find('\n')
            eta = disc_date[d_inx + 1:d_inx + 12]
            if 'icon-completed' in e_ata:
                e_ata = 'ATA'
            else:
                e_ata = 'ETA'
            inx = pod_loc.find('\n')
            pod_loc = pod_loc.replace('\n', ' ')
            if pod_loc[:inx] in pod:
                break
    except:
        e_ata, eta = '--', '--'
    dr.quit()
    if info1.find('No data') >= 0:
        e_ata, eta = '--', '--'
    return e_ata, eta


def mat_track(cont):
    dr = webdriver.Chrome()
    dr.minimize_window()
    mats = 'https://www.matson.com/shipment-tracking.html'
    dr.get(mats)
    WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.ID, 'track-number-top')))
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
                eta = table[:11].replace(' ', '')
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
    return ea, eta


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
            i += 1
        event = dr.find_element_by_xpath(
            f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[3]').text
        date = dr.find_element_by_xpath(
            f'/html/body/div[2]/main/div[3]/div/div[1]/div/table/tbody/tr[{i}]/td[4]').text
        event = event.replace('Estimated arrival at POD', 'ETA')
        event = event.replace('Arrived at POD', 'ATA')
    except:
        event, date = '--'
    dr.quit()
    return event, date


def sud_track(cont):
    dr = webdriver.Chrome()
    dr.minimize_window()
    webs = 'https://www.hamburgsud-line.com/linerportal/pages/hsdg/tnt.xhtml?lang=en'
    dr.get(webs)

    send_path = '/html/body/main/div/div/form/div[2]/div[1]/div[1]/div[2]/textarea'
    WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, send_path)))
    dr.find_element_by_xpath(send_path).send_keys(cont)
    dr.find_element_by_xpath('/html/body/main/div/div/form/div[2]/div[1]/div[2]/div[2]/button').click()

    ea, eta = '-', '-'
    path_info = '/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[1]/td[3]'
    WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, path_info)))
    for i in range(1,6):
        info1 = dr.find_element_by_xpath(
        f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[3]').text
        eta = dr.find_element_by_xpath(
           f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[{i}]/td[1]').text
        indx = info1.find('Estimated vessel arrival')
        indx2 = info1.find('Vessel arrived')
        if indx >= 0:
            ea = 'ETA'
            break
        elif indx2 >= 0:
            ea = 'ATA'
            break
        else:
            ea = dr.find_element_by_xpath(
                f'/html/body/main/div/div/form/div[3]/div/div/div[5]/div[1]/div/table/tbody/tr[1]/td[3]').text
    dr.quit()
    eta = eta[:11]
    return ea, eta


def hap_track(cont):
    # TGBU6166545
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
    info_path = '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table'
    WebDriverWait(dr, 5).until(EC.presence_of_element_located((By.XPATH, info_path)))
    try:
        i = 1
        path_t = '/html/body/div[5]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/form/div[5]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/'
        while True:
            status = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[1]').text
            place = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[2]').text
            if 'Vessel arrival' in status and ',' in place:
                break
            elif 'Vessel arrived' in status and ',' in place:
                break
            elif i == 20:
                break
            i += 1
        date = dr.find_element_by_xpath(f'{path_t}tr[{i}]/td[3]').text
        eta = 'ETA' if 'Vessel arrival' in status else 'ATA'
        ea = eta
        info2 = date
    except:
        ea = info2 = '--'
    return ea, info2


def wan_track(cont):
    # WHSU5831702
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
        return '--', '--'
    dr2.find_element_by_xpath(more_d).click()
    dr2.switch_to.window(dr2.window_handles[2])

    vess_path = '/html/body/div[2]/div[1]/div/form/table[3]/tbody/tr[3]/td[2]'
    WebDriverWait(dr2, 5).until(EC.presence_of_element_located((By.XPATH, vess_path)))

    arr_eta = '/html/body/div[2]/div[1]/div/form/table[3]/tbody/tr[3]/td[3]'
    ar_eta = dr2.find_element_by_xpath(arr_eta).text

    ea = 'ETA'
    arrival_date, tod_ = '', ''
    if len(ar_eta) > 4:
        c_year = int(ar_eta[:4])
        c_month = int(ar_eta[5:7])
        c_day = int(ar_eta[-2:])
        tod_ = datetime.date.today()
        arrival_date = datetime.date(c_year, c_month, c_day)

    if len(ar_eta) > 4 and arrival_date > tod_:
        eta = arrival_date
        dr2.quit()
        return ea, eta
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
            eta = arrival_date
            dr2.quit()
            return ea, eta
        if len(etb) > 4:
            eta = etb
        else:
            eta = eta
        dr2.quit()
        return ea, eta


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
    ea = 'ETA'
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
        # pod = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[1]').text
        eta_d = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[3]').text
        # vessel = dr.find_element_by_xpath(f'{row_tb}/tr[{i}]/td[4]').text
        ea = 'ETA' if 'Estimated' in descr else 'ATA'
        # info = f'{pod} {ea} {eta_d} \nVessel: {vessel}'
    else:
        eta_d = '--'
        # info = descr
    dr.quit()
    eta = eta_d.split('/')
    eta = eta[1] +'/'+ eta[0] +'/'+ eta[2]
    return ea, eta


def evg_track(cont):
    web = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
    dr = webdriver.Chrome()
    dr.minimize_window()
    dr.get(web)
    ea = 'ETA'
    e_date = ''
    if len(cont) == 11:
        check_cont = '/html/body/div[4]/div[4]/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[1]'
        dr.find_element_by_xpath(check_cont).click()

        inp_cont = '/html/body/div[4]/div[4]/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]'
        dr.find_element_by_xpath(inp_cont).send_keys(cont)

        sub_btn = '/html/body/div[4]/div[4]/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]'
        dr.find_element_by_xpath(sub_btn).click()

        vessel_path = '/html/body/div[5]/div[4]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[3]'
        vessel = dr.find_element_by_xpath(vessel_path).text

        eta_path = '/html/body/div[5]/div[4]/table[2]/tbody/tr/td/table[2]/tbody/tr/td'
        date = dr.find_element_by_xpath(eta_path).text
        date = date.replace('\n', '').replace('Estimated Date of Arrival :', '')
        e_date = date
    else:
        cont = cont[4:]

        inp_cont = '/html/body/div[4]/div[4]/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[1]'
        dr.find_element_by_xpath(inp_cont).send_keys(cont)

        sub_btn = '/html/body/div[4]/div[4]/table[2]/tbody/tr/td/form/span[2]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]'
        dr.find_element_by_xpath(sub_btn).click()

        try:
            row_path = '/html/body/div[5]/div[4]/table[2]/tbody/tr/td/table[6]/tbody/tr[3]/'
            # WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, row_path)))
            eta = dr.find_element_by_xpath(f'{row_path}td[1]').text
            e_date = eta
        except:
            rows = '/html/body/div[5]/div[4]/table[2]/tbody/tr/td/table[3]/tbody/'
            i = 3
            while True:
                status = dr.find_element_by_xpath(f'{rows}tr[{i}]/td[8]').text
                if 'Discharged' in status:
                    break
                elif i == 11:
                    break
                i += 1
            date = dr.find_element_by_xpath(f'{rows}tr[{i}]/td[9]').text
            ea = 'ATA'
            e_date = date
    return ea, e_date