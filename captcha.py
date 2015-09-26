import os, sys
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import urllib2
url = "http://www.worldfestival.gov.hk/2011/php/fd_form2.php"

htmlbs = BeautifulSoup(urllib2.urlopen(url).read(), "html5lib")
htmlbs.find_all('input') #'capt_code_html is not here and you have no way to interactive with the form

firefox_profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,10)
driver.get("http://www.worldfestival.gov.hk/2011/php/fd_form2.php")
html_source = driver.page_source
bs_html = BeautifulSoup(html_source, "html5lib")
ans = bs_html.find(name = 'input', attrs = {'name': 'capt_code_html'}).get('value')
captcha = driver.find_element_by_xpath("//input[@name='number']")
captcha.clear()
captcha.send_keys(ans)
driver.find_element_by_xpath("//input[@name='Submit']").click()
#driver.close()
