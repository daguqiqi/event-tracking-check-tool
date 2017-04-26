#-*- coding: UTF-8 -*-

from other_packages.Tkinter import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from other_packages import platform
from other_packages import string
import os


def btn_click():
    if platform.system() == "Windows":
        f = open(os.path.split(os.path.realpath(__file__))[0]+'\EventTrackCheckResult.txt', 'w')
        chromedriver = "chromedriver.exe"
    else:
        chromedriver = "driver/chromedriver"
        f = open(os.path.split(os.path.realpath(__file__))[0]+'/EventTrackCheckResult.txt', 'w')
    driver = webdriver.Chrome(chromedriver)

    url = e1.get()
    expect_site_psa = e2.get()
    expect_page_psa = e3.get()

    driver.get(url)
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locator = (By.NAME, 'description')))

    print>> f, "\n测试URL：", url,"\n"
    psa_js = ""
    actual_site_psa = ""
    actual_page_psa = ""
    zone_psa = ""
    url_list = []
    psaid_list = []
    no_psa_list = []

    scriptlist = driver.find_elements_by_tag_name("script")
    for script in scriptlist:
        if script.get_attribute("src") != None and "dopsa.js" in script.get_attribute("src"):
            psa_js = script.get_attribute("src")
            break
    if psa_js != "":
        print>> f, "dopsa.js已经加载！\n"
    else:
        print>> f, "dopsa.js没有加载！\n"

    metalist = driver.find_elements_by_tag_name("meta")
    for meta in metalist:
        if meta.get_attribute("psa") != None:
            actual_site_psa = meta.get_attribute("psa")
            break
    if actual_site_psa == "":
        inputlist = driver.find_elements_by_tag_name("input")
        for input in inputlist:
            if input.get_attribute("site-id") != None:
                actual_site_psa = input.get_attribute("site-id")
            if input.get_attribute("page-id") != None:
                actual_page_psa = input.get_attribute("page-id")
    else:
        actual_page_psa = driver.find_element_by_tag_name("body").get_attribute("psa")

    if expect_site_psa == actual_site_psa:
        print>> f, "站点PSA码正确！\n"
    else:
        print>> f, "站点PSA码错误！期望：", expect_site_psa, " 实际：", actual_site_psa, "\n"
    if expect_page_psa == actual_page_psa:
        print>> f, "页面PSA码正确！\n"
    else:
        print>> f, "页面PSA码错误！期望：", expect_page_psa, " 实际：", actual_page_psa, "\n"

    alist = driver.find_elements_by_tag_name("a")
    for a in alist:
        if a.get_attribute("psa-id") != None:
            url_list.append(a.get_attribute("href"))
            psaid_list.append(a.get_attribute("psa-id"))
        else:
            if a.get_attribute("href") != None and a.get_attribute("href") != "javascript:;":
                no_psa_list.append(a.get_attribute("href"))

    for k, v in zip(url_list, psaid_list):
        if string.find(v, expect_site_psa + "." + expect_page_psa) != -1:
            if zone_psa != v.split(".")[2]:
                zone_psa = v.split(".")[2]
                print>> f, "-------------------- 区域PSA：", zone_psa, "--------------------"
            print>> f, v, "\n", k, "\n"
        else:
            print>> f, "\nPSA错误!!!!!", k, v

    if no_psa_list != []:
        print>> f, "\n!!!以下链接没有PSA码，请手动检查是否错误!!!"
        for no_psa in no_psa_list:
            print>> f, no_psa

    driver.quit()
    f.close()

    str = "测试结束！"
    if platform.system() == "Windows":
        dir = os.path.split(os.path.realpath(__file__))[0] + '/EventTrackCheckResult.txt'
        print str.decode('UTF-8').encode('GBK')
    else:
        dir = "open " + os.path.split(os.path.realpath(__file__))[0] + '/EventTrackCheckResult.txt'
        print str
    os.system(dir)

root = Tk()
root.title("埋点测试小公举")
root.geometry("400x200")

Label(root, text="   请输入测试数据", font=("Arial",20)).pack()
Label(root, text="   如：https://bxg.wuage.com W8 a54\n",  font=("Arial",15)).pack()
frm = Frame(root)

frm1 = Frame(frm)
Label(frm1, text="测试URL",  font=("Arial",15)).pack(side=LEFT)
e1 = Entry(frm1)
e1.pack()
frm1.pack()

frm2 = Frame(frm)
Label(frm2, text="站点PSA",  font=("Arial",15)).pack(side=LEFT)
e2 = Entry(frm2)
e2.pack()
frm2.pack()

frm3 = Frame(frm)
Label(frm3, text="页面PSA",  font=("Arial",15)).pack(side=LEFT)
var = Variable()
e3 = Entry(frm3)
e3.pack()
frm3.pack()


b = Button(frm, text = '开始测试', command=btn_click)
b.pack()

frm.pack()

root.mainloop()

