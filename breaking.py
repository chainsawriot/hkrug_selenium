import os, sys
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def breaking(govurl, rname_txt , remail_txt, rep = 10):
    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox()
    wait = ui.WebDriverWait(driver,10)
    for _ in range(rep):
        print _
        try:
            driver.get(govurl)
        except:
            driver.get(govurl)
        html_source = driver.page_source
        bs_html = BeautifulSoup(html_source, "html5lib")
        ans = bs_html.find(name = 'input', attrs = {'name': 'capt_code_html'}).get('value')
        sendername = driver.find_element_by_xpath("//input[@name='s_name']")
        sendername.clear()
        sendername.send_keys("CY Leung")
        semail = driver.find_element_by_xpath("//input[@name='s_email']")
        semail.clear()
        semail.send_keys("ceo@ceo.gov.hk")
        rname = driver.find_element_by_xpath("//input[@name='r_name']")
        rname.clear()
        rname.send_keys(rname_txt)
        remail = driver.find_element_by_xpath("//input[@name='r_email']")
        remail.clear()
        remail.send_keys(remail_txt)
        captcha = driver.find_element_by_xpath("//input[@name='number']")
        captcha.clear()
        captcha.send_keys(ans)
        driver.find_element_by_xpath("//input[@name='Submit']").click()
    driver.close()

breaking("http://www.worldfestival.gov.hk/2011/php/fd_form2.php", "yourname", "youremail@xyz.com")
