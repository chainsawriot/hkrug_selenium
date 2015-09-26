from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

import feedparser
feed = feedparser.parse('http://news.mingpao.com/rss/pns/s00001.xml')
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.loadImages"] = False

driver = webdriver.PhantomJS(desired_capabilities=cap)

wait = ui.WebDriverWait(driver,10)

res = []
for entry in feed['entries']:
    print entry['link']
    driver.get(entry['link'])
    html_source = driver.page_source
    mingpao_s = BeautifulSoup(html_source, "html5lib")
    res.append(" ".join([p.get_text() for p in mingpao_s.find_all('p')]))
driver.close()

for article in res:
    print article
