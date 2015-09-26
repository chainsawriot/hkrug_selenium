import os, sys
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
import datetime
import weibopass
import csv

username = weibopass.username
password = weibopass.password

browser = 'firefox'

# Login from the mobile interface

if browser == 'firefox':
    firefox_profile = webdriver.FirefoxProfile()
    #firefox_profile.set_preference('permissions.default.stylesheet', 2)
    #firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
    driver = webdriver.Firefox(firefox_profile = firefox_profile)
else:
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(desired_capabilities=cap)

wait = ui.WebDriverWait(driver, 20)
driver.get("http://weibo.cn/")
x = BeautifulSoup(driver.page_source, "html.parser")
driver.get(x.find(name = "div", attrs = {'class': 'ut'}).find('a').get('href')) #go to the login page
user = driver.find_element_by_xpath("//input[@name='mobile']")
user.clear()
user.send_keys(username)
pwname = BeautifulSoup(driver.page_source, 'html.parser').find(name = "input", attrs = {'type': 'password'}).get('name')
pwdfield = driver.find_element_by_xpath("//input[@name='"+pwname+"']")
pwdfield.clear()
pwdfield.send_keys(password)
driver.find_element_by_xpath("//input[@name='submit']").click()
#sleep(randint(5,10))


res = []
csvfile = open('weibousers.csv', 'w')
fieldnames = ['screenname', 'link', 'uid', 'info']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

driver.get("http://s.weibo.com/user/&region=custom:81:1000")
while True:
    while True:
        current_url = driver.current_url
        try:
            wait.until(lambda driver: driver.find_elements_by_xpath("//div[@class='person_list_feed clearfix']"))
            break
        except:
            driver.get(current_url)    
    weibobs = BeautifulSoup(driver.page_source, "html5lib")
    userbox = weibobs.find_all(name = 'div', attrs = {'class':'list_person clearfix'})
    for box in userbox:
        screenname = box.find(name = 'a', attrs = {'class': 'W_texta W_fb'}).get_text().strip()
        link = box.find(name = 'a', attrs = {'class': 'W_texta W_fb'}).get('href')
        uid = box.find(name = 'a', attrs = {'class': 'W_texta W_fb'}).get('uid')
        try:
            info = box.find(name = 'p', attrs = {'class': 'person_card'}).get_text().strip()
        except:
            info = ""
        print(screenname)
        print(link)
        print(uid)
        print(info)
        writer.writerow({'screenname': screenname, 'link': link, 'uid': uid, 'info': info})
    try:
        link = driver.find_element_by_link_text("下一页")
        link.click()
        sleep(0)
    except NoSuchElementException:
        break

csvfile.close()
driver.close()
