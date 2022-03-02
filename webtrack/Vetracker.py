import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def vetrack(vessel):
    dr = webdriver.Chrome()
    dr.minimize_window()
    webs = f'https://www.vesselfinder.com/vessels?name={vessel}&type=403'
    dr.get(webs)
    table = '/html/body/div/div/main/div/section/table/tbody'

    try:
        WebDriverWait(dr, 3).until(EC.presence_of_element_located((By.XPATH, table)))
    except:
        info_all = 'Not found'
        dr.quit()
        return info_all
    link1 = '/html/body/div/div/main/div/section/table/tbody/tr/td[2]/a'
    dr.find_element_by_xpath(link1).click()

    info_path = '/html/body/div[1]/div/main/div/section[1]/div/div[2]/div'
    info = dr.find_element_by_xpath(info_path).text
    dr.quit()
    indx01 = info.find('Predicted')
    indx02 = info.find('Position')
    indx001 = info.find('IMO / MMSI')
    indx002 = info.find("Beam")
    info_eta = info[:indx01].replace('\n', ' ').replace('United States ', '').replace('UTCARRIVED', '')
    info_2 = info[indx002:]
    indx03 = info_2.find('\n')
    info_atd = info_2[indx03:]
    info_upd = info[indx02:indx001]
    info_all =  'POD: '+ info_eta + info_atd + '\n' + info_upd
    return info_all
