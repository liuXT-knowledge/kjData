'''
抓取微信小程序会计网题库中的题目，微信版本为8.0.30
必须先在微信中打开如下网址
debugxweb.qq.com/?inspector=true
'''

import time
import threading
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

desired_caps = {
    "platformName": "Android",
    "deviceName": "e6e00908",
    "appPackage": "com.tencent.mm",
    "appActivity": ".ui.LauncherUI",
    "noReset": True,
    "unicodeKeyboard":True,
    "resetKeyboard":True,
    "chromedriverExecutable":r"D:\Program Files\chromedriver_win32\chromedriver.exe"
}

zj = int(input('输入抓取的章节：')) - 1
bookName = 'jjf'
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(30)

width = driver.get_window_size()['width']/3
height = driver.get_window_size()['height']/3



##进入小程序
driver.find_element(AppiumBy.XPATH,"//*[@text='发现']").click()
driver.implicitly_wait(5)

driver.swipe(width*0.5,height*0.9,width*0.5,height*0.5,1000)
driver.implicitly_wait(5)

driver.find_element(AppiumBy.XPATH,"//*[@text='小程序']").click()
driver.implicitly_wait(5)
driver.find_element(AppiumBy.XPATH,"//*[@text='会计网题库']").click()
driver.implicitly_wait(5)
time.sleep(8)

##切换webview
driver.switch_to.context("WEBVIEW_com.tencent.mm:appbrand0")
#点击图书扩展
for window in driver.window_handles:
    driver.switch_to.window(window)
    if "pages/index" in driver.title and "VISIBLE" in driver.title:
        break
if("pages/index" in driver.title):
    item = driver.find_elements(AppiumBy.XPATH,"//wx-view[@class='t_sw_item']")[-1]
    item.click()
    driver.implicitly_wait(5)
    time.sleep(5)

#点击经典题解
for window in driver.window_handles:
    driver.switch_to.window(window)
    if "books" in driver.title and "VISIBLE" in driver.title:
        break
if("books" in driver.title):
    classicTiku = driver.find_elements(AppiumBy.XPATH,"//wx-view[@class='title']")[2]
    classicTiku.click()
    driver.implicitly_wait(5)
    time.sleep(5)

#点击每一章练习
for window in driver.window_handles:
    driver.switch_to.window(window)
    if "bookdata" in driver.title and "VISIBLE" in driver.title:
        break
if("bookdata" in driver.title):
    paper1 = driver.find_elements(AppiumBy.XPATH,"//wx-view[@class='title']")[zj]
    paper1.click()
    driver.implicitly_wait(5)
    time.sleep(5)

#点击题目
result = []
exec = 0
for window in driver.window_handles:
    driver.switch_to.window(window)
    if "papers" in driver.title and "VISIBLE" in driver.title:
        break
papersCount = driver.find_element(AppiumBy.XPATH,"//wx-view[@class='questionItem-index--papers-index']").text.strip()

exec_count = int(papersCount.split(' ')[1])
def task():
    global result
    try:
        tableTemp = driver.find_element(AppiumBy.XPATH,"//wx-view[@class='questionItem-index--view-input']")
        tableHtml = ''
        if( tableTemp is not None and tableTemp.text.strip() == '请输入答案（选填）'):
            tableHtml = driver.find_element(AppiumBy.XPATH,"//table").get_property('outerHTML')
            print(tableHtml)
            #with open(rf'E:\Projects\vscode\python\kj\wx\{bookName}\txt\{zj+10}.txt','w',encoding='utf-8') as file:
            #    file.write(''.join(tableHtml))
    except :
        pass
    driver.swipe(width*0.9,height*0.5,width*0.1,height*0.5,1000)
    driver.implicitly_wait(5)
    return
    answer = driver.find_elements(AppiumBy.XPATH,"//wx-view[@class='pagers-bar-icon']")[1]
    answer.click()
    driver.implicitly_wait(5)
    time.sleep(2)
    swiper = driver.find_element(AppiumBy.XPATH,"//wx-swiper[@class='papers-swiper']")
    curID = swiper.get_attribute('current')
    curItem = swiper.find_element(AppiumBy.XPATH,f"//wx-swiper-item[@data-index={curID}]").text
    if(tableHtml == ''):
        return
    else :
        curItem += tableHtml
    result.append(curItem + "\n------------------\n")
    driver.swipe(width*0.9,height*0.5,width*0.1,height*0.5,1000)
    driver.implicitly_wait(5)

def start_task():
    global exec,exec_count,zj   
    exec += 1
    if exec <= exec_count:
        task()
        threading.Timer(6,start_task).start()
    #else:
    #    with open(rf'E:\Projects\vscode\python\kj\wx\{bookName}\txt\{zj+1}.txt','w',encoding='utf-8') as file:
    #        file.write(''.join(result))
start_task()