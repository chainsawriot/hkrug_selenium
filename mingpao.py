import urllib2
from bs4 import BeautifulSoup

url = 'http://news.mingpao.com/pns/%E9%99%B3%E4%BD%90%E6%B4%B1%EF%B9%95%E5%85%A7%E8%80%97%E5%9B%A0%E7%84%A1%E4%BE%9D%E6%B3%95%E5%8E%BB%E6%AE%96%20%20%E8%AD%9A%E5%BF%97%E6%BA%90%E7%B1%B2%E4%BA%AC%E5%A4%9A%E4%BF%A1%E6%B8%AF%E4%BA%BA%20%E6%9B%BE%E9%88%BA%E6%88%90%EF%BC%9A%E4%B8%8D%E7%9F%A5%E4%BE%9D%E4%BB%80%E9%BA%BC%E6%B3%95/web_tc/article/20150921/s00001/1442771796938'

mingpao = BeautifulSoup(urllib2.urlopen(url).read())

print mingpao.find_all('p')
print mingpao.find_all('title')

# selenium

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

firefox_profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,10)

driver.get(url)
html_source = driver.page_source

mingpao_s = BeautifulSoup(html_source)

print mingpao_s.find_all('p')

print " ".join([p.get_text() for p in mingpao_s.find_all('p')])
driver.close()

# even extreme example

import feedparser
feed = feedparser.parse('http://news.mingpao.com/rss/pns/s00001.xml')
print feed.keys()

feed['entries']

feed['entries'][0]['link']

firefox_profile = webdriver.FirefoxProfile()
#firefox_profile.set_preference('permissions.default.stylesheet', 2)
#firefox_profile.set_preference('permissions.default.image', 2)
#firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

driver = webdriver.Firefox(firefox_profile)
wait = ui.WebDriverWait(driver,10)

res = []
for entry in feed['entries']:
    driver.get(entry['link'])
    html_source = driver.page_source
    mingpao_s = BeautifulSoup(html_source)
    res.append(" ".join([p.get_text() for p in mingpao_s.find_all('p')]))
driver.close()

for article in res:
    print article
