from x import xx
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import string
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
import traceback

start = 1000
end = 1000
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
##chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
##chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
###针对UA请求头的操作，防止因为没有添加请求头导致的访问被栏截了
chrome_options.add_argument(
    'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) >AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/87.0.664.57'
)
##chrome_options.add_argument('--no-sandbox')
##chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
##chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度

chrome_options.add_argument("window-size=720,620")
chrome_options.add_experimental_option("excludeSwitches",
                                       ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)
#规避检查
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument", {
        "source":
        """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
    })
with open(r'C:\stealth.min.js', 'r') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
decide = "yes"
Total = []
raw = []  ##原始数据初始化为空
dict = {'new': [], 'old': []}
try:
    f = open("asin.json", 'r')
    data = f.read()
    dict = json.loads(data)
    print(type(dict))
    f.close()
    print("初始dict['new']:" + str(dict['new']))
    print("初始dict['old']:" + str(dict['old']))
    if (dict['new'] != []):
        raw.extend(dict["new"])  ##raw 获取原始数据
        while True:
            try:
                decide = input("请输入yes/no,您是否要把NEW的数据存入Old？\n")
                if (decide == "yes") or (decide == "no"):
                    break
                else:
                    print("你没有输入yes/no，请重新输入")
                    continue
            except:
                print("输入错误，请重新输入")
    if (dict['old'] != []):
        raw.extend(dict["old"])
    print("raw:" + str(raw))
except:
    print("没有文件")
    traceback.format_exc()
    traceback.print_exc(file=open('error.txt', 'a+'))

wait = WebDriverWait(driver, 1)
##登录亚马逊
logurl = 'https://www.baidu.com'
message = ""
##设置匹配规则
pattern = re.compile(r'dp/(.*?)/')
driver.get(logurl)
time.sleep(random.random())
i = 1


def getAsin(kword):
    global Total
    print(kword)
    crid = '1' + ''.join(
        random.sample(string.ascii_uppercase + string.digits, 12))
    for num in range(1, 11):
        print(f"num:{num}")
        url = f"https://www.amazon.co.jp/s?k={kword}&__mk_ja_JP=カタカナ&crid={crid}&page={num}"
        driver.get(url)
        time.sleep(random.random())
        r = driver.page_source
        print(r)
        result = pattern.findall(r)
        ##        print(result)
        if (result != []):
            ##            print(set(result))##每次读取的Asin写入数组，数组去重
            Total.extend(set(result))
            time.sleep(2)
##            print("Total:" + str(Total))
            ##去重Total节省空间
            Total = list(set(Total))
##            print("Total:" + str(Total))
        else:
            continue


##    dict['new']=set(Total)##set对象不能被序列化

try:
    getAsin("anker")
#    xx.lines(getAsin, "key.csv")  #读取关键词
except Exception:
    print(traceback.format_exc())
    traceback.print_exc(file=open('error.txt', 'a+'))
finally:
    if (decide == "yes"):
        dict['new'] = list(set(Total).difference(set(raw)))
        dict['old'] = list(
            set(raw))  ##如果没有asin文件raw默认为空，有asin文件 raw为之前的new+之前的old
    elif (decide == "no"):  ##为no不写入  new在自己的基础上进行更新,old不更新
        print("新加入的asin为：" +str(list(set(Total).difference(set(dict['new'])))))
        dict['new'].extend(set(Total).difference(set(dict['new'])))

    print("现在dict['new']:" + str(dict['new']))
    print("现在dict['old']:" + str(dict['old']))
    data = json.dumps(dict)
    file = open('asin.json', 'w')
    file.write(data)
    file.close()
