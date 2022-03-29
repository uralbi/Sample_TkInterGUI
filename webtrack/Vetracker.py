import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def vetrack(vessel):
    dr = webdriver.Chrome()
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
    info_path2 = '/html/body/div[1]/div/main/div/section[2]/div/div[2]/div[1]'
    info = dr.find_element_by_xpath(info_path).text
    time.sleep(0.5)
    info2 = dr.find_element_by_xpath(info_path2).text
    info = info.split('\n')
    info2 = info2.split('\n')
    dr.quit()
    def commaseparator(text):
        inx = text.find(',')
        return text[:inx]
    pod1 = commaseparator(info[0])
    pod2 = commaseparator(info2[0])
    eta1 = commaseparator(info[1])
    pol = commaseparator(info[12])
    atd = commaseparator(info[13])
    ata2 = commaseparator(info2[2])
    nav = info[6].replace('Navigation ', '').replace('Status', 'Status:')
    info_all = f'-> {pod1} | {eta1} | {nav}\n<- {pol} | {atd} | Ata: {ata2}'
    return info_all
