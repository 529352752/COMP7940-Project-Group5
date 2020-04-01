import requests
from bs4 import BeautifulSoup
from selenium import  webdriver 
import time
from selenium.webdriver.chrome.webdriver import RemoteWebDriver # 从selenium库中调用RemoteWebDriver模块
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('--headless')
url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=dxy&source=&link=&share='
driver = RemoteWebDriver("服务器地址", chrome_options.to_capabilities())
driver.get(url)
time.sleep(4)
pageSource = driver.page_source
dxy = BeautifulSoup(pageSource, 'html.parser')
ssbb = dxy.find_all('div',class_="block___wqUAz")
list_all = []
print('世界疫情资讯实施播报')
for i in ssbb:
    timing = i.find('span',class_="leftTime___2zf53").text
    title = i.find('p',class_="topicTitle___2ovVO").text
    content=i.find('p',class_="topicContent___1KVfy").text
    source = i.find('p',class_="topicFrom___3xlna").text
    list_all.append([timing,title,content,source])
    print('发布时间:'+timing,'\n标题:'+title+'\n内容摘要:'+content,'\n'+source+'\n')


driver.close()

