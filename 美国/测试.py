import re
import yaml
import shutil
res=shutil.rmtree('./auto')


num=lnum=0
# with open("./config/config.yaml",'r' ) as stream: 
#     config = yaml.safe_load(stream) 
# config['anum']=10
# with open('./config/config.yaml', 'w') as f: 
#     data = yaml.dump(config, f)
# a=list(['13'])
import csv

# 引用csv模块。
csv_file = open('movie.csv', 'a', newline='', encoding='gbk')
# 调用open()函数打开csv文件，传入参数：文件名“demo.csv”、写入模式“w”、newline=''、encoding='gbk'
writer = csv.writer(csv_file)
# 用csv.writer()函数创建一个writer对象。
writer.writerow(['电影', '豆瓣评分'])
# 调用writer对象的writerow()方法，可以在csv文件里写入一行文字 “电影”和“豆瓣评分”。
writer.writerow(['喜羊羊与灰太狼', '9.9'])
# 在csv文件里写入一行文字 “喜羊羊与灰太狼”和“9.9”
writer.writerow(['熊出没之夺宝熊兵', '10.0'])
# 在csv文件里写入一行文字 “熊出没之夺宝熊兵”和“10.0”
csv_file.close()
# # 关闭文件

# csv_file = open('movie.csv', 'r', newline='', encoding='gbk')#编码方式与写入文件时相同
# reader = csv.reader(csv_file)
# for row in reader:
#     print(row)
    
 
with open('movie.csv', 'r', newline='', encoding='gbk') as csvfile:
    reader = csv.DictReader(csvfile)
    column = [row for row in reader]   # weight 同列的数据
print(column)
    
ids={
    'x':[1,23,4],
     'j':[5,6,7],
     'k':[8,9]
     }#设置数据格式


with open('user.html','r',encoding='utf-8') as f:
    userdata=f.read()
# print(type(userdata))
url_s = re.compile(r'"url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])","iconUrl"')#匹配网站规定url地址
url_o = re.compile(r'"raw":"(\b(?!null)\S+)","no')#匹配个人url地址
pattern=url_s.pattern+'|'+url_o.pattern
pinterest=re.compile(r'"pinterest","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#缤趣匹配
twitter=re.compile(r'"twitter","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#推特匹配
instagram=re.compile(r'"instagram","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#ins匹配
youtube=re.compile(r'"youtube","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#油管匹配
facebook=re.compile(r'"facebook","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#脸书匹配
rank=re.compile(r'"rank":"(\b(?!null)\S+)","decoratedRank"')#排名匹配



[ids[i]+[i] for i in ids.keys()] #要写入的数据类型

pattern1 = re.compile(r'"list":\[(.*?)\],')











# import json
# with open("uids.json",'r',encoding="utf-8") as f:
#     uids=json.load(f)
# with open("uid.json",'r',encoding="utf-8") as f:
#     uid=json.load(f)
# Total=[]
# Total.extend(uids['new'])
# Total.extend(uid['new'])
# Total.extend(uid['old'])
# Total=list(set(Total))
# uids['new']=Total

# with open('uids.json','w',encoding="utf-8") as f:
#     json.dump(uids,f,ensure_ascii=False)
#     print('写入成功')

# print("暂停")



# import time
# while 1:
#     time.sleep(3)
#     print('111')


'''实现进程池'''

from multiprocessing import Pool,Lock,Manager,Array,Value#脑抽了居然使用进程池去管理全局变量，生成的多个进程不会共享的只能每次都保存一下
# import time
import os
# dict={}


def init(l,d):
    global lock
    global dic
    dic=d
    lock = l


# mutex = threading.Lock()#线程锁

# print(len(list))
def  action(name):
    print(name,' --当前进程：',os.getpid())
    # mutex.acquire()  # 上锁
    
    lock.acquire()
    dic[name]=True
    lock.release()
    # mutex.release()  # 解锁
    # time.sleep(1)
        # if name==5099:
    #     try:
    #         raise BaseException
    #     except BaseException:
    #         print("我抓住了错误")
    
    
if __name__ == '__main__':
    list=[i for i in range(1,101)]
    # num= Value("d",10.0)  # 共享数值：d表示数值,
    # num= Array("i",[1,2,3,4,5])  # 共享数组
    dic= Manager().dict()  # 共享字典
    mylist= Manager().list(range(1))  # 共享 list

    #创建包含 4 条进程的进程池
    lock = Lock()
    with Pool(processes=10,initializer=init,initargs=(lock,dic,)) as pool:
        pool.map(action,list)
    print(str(dic),file=open('test.txt','w'))
    print('完成')























import asyncio, time
from pyppeteer import launch
import deal_img

imagepath='toutiao.jpg'
class A:
    status=500
    ok=False

async def lookhome(page,res):#访问主页观察是否
    while not res.ok : # 响应状态码
        try:
            res=await page.goto("file:///C:/Users/Administrator/Desktop/test.html") # 访问主页                
        # resp_headers = res.headers  # 响应头
        # resp_status = res.status    # 响应状态
        # resp_url = res.url          # 请求地址
        except BaseException:
            await page.browser.close()
            res=A()
            page=await create_page()


async def create_page(width=2,height=2):#创建一个浏览器和页面
    browser = await launch(headless=False, dumpio=True, 
                           args=[ f'--window-size={width},{height}', '--disable-infobars',"--user-data-dir=E:/pyppeteer/AutomationProfile"])# 进入有头模式 headless=False
    page = await browser.newPage()
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.setViewport({'width': width, 'height': height})      # 页面大小一致
    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    return  page



async def yanzhenma(page):
     # await page.browser.close()
    print(f"被识别到爬虫，运行次数")
    await page.browser.close() 
    page=await create_page(1920,1080)
    res=A()
    await lookhome(page,res)
    button=await page.xpath('//form//span/button')
    img=await page.xpath('//form//img')
    if button !=[] and img!=[]:
        await img[0].screenshot({'path': imagepath})
        img_str=deal_img.deal(imagepath)
        if img_str!='验证码错误' and img_str!='':
            print("图片获取成功")
            print(img_str)
            await page.type("#captchacharacters",img_str)
            await button[0].click()
            page.goto("https://amazon.com")
            page.browser.close()
            page=await create_page()
            page.goto("https://amazon.com")
        elif img_str=='':
            print("图片识别到为空")
            
    else:
        print("新开页面未被识别到爬虫")
    return page





async def main():
    page = await create_page(1020,1020)
    browser=page.browser
    page1 = await browser.newPage()           # 打开新的标签页
    page2=await browser.newPage()
    
    # page1=await browser.newPage()
    # page2=await browser.newPage()
    
    # url = 'https://www.amazon.com/'
    # step_2 发起请求获取响应对象                                                               
    # step_3 获取响应数据
    res=A()                                                              
    await lookhome(page,res)
    # await lookhome(page1,res)
    # await lookhome(page2,res)
    # await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    # print('图片爬取成功')
    # res=await page.goto(url) # 访问主页
    # button=await page.xpath('//form//span/button')
    # img=await page.xpath('//form//img')
    # ret=await img[0].screenshot({'path': 'toutiao.jpg'})   
    # img_str=deal_img.deal('toutiao.jpg')
    
    result = await page.xpath('//*[@id="cm_cr-review_list"]/div//a[@class="a-profile"]/@href')
    result=[await (await rst.getProperty('textContent')).jsonValue() for rst in result]
    status=await page.xpath('//div[@class="a-section"]//form/@action')
    if status!=[]:
        while await page.xpath('//div[@class="a-section"]//form/@action')!=[]:
                       page= await yanzhenma(page)
                        
    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    
    # await page.screenshot({'path': './1.jpg'})   # 截图保存路径
    res=A()
    print(res.status)
    page_text = await page.content()   # 获取网页源码
    print(page_text)
    time.sleep(1)
    # await page.close()
    print('已关机')
asyncio.get_event_loop().run_until_complete(main()) #调用



'''随机数获取'''
# import random
# import string
# import json
# import re

# t=random.uniform(1,2)
# a=[]
# b=[]


####for i in range(1,5):
####    crid = '1'+''.join(random.sample(string.ascii_uppercase + string.digits, 12))
####    a.append(crid)
####    print(crid)
##for i in range(5):
##    crid = '1'+''.join(random.sample(string.ascii_uppercase + string.digits, 12))
##    RID = ''.join(random.sample(string.ascii_uppercase + string.digits, 20))
##    
##    b.append(crid)
##    print(RID)
##    print(i)
####print(a)
####print(b)
####print("合并之前a中有而b中没有的")
####print(list(set(a).difference(set(b))))
####
####b.extend(a)
####
####print("合并之后a中有而b中没有的")
####if list(set(a).difference(set(b)))==[]:
####    print("无")
####
####print(list(set(a).difference(set(b))))
##
##f=open('asin.txt','r')
##list1=f.read()
##print(list1)


# 列表写入文件
# 测试list
##risk_list =  [{'123':'111','456':222},{'123':'111','456':222}]
# 将数据写入文件
##
##for i in risk_list:
##    json_i = json.dumps(i)
##    file.write(json_i+'\n')
##file.close()

# 从文件中读取数据
##risk_result = []
##with open('asin.json','r') as f:
##    # 读取数据并分割。 最后一个为空，所以去除
##    risk_new_list = set(f.read().split('\n')[:-1])
##    for x in risk_new_list:
##        json_x = x
##        risk_result.append(json_x)
##f.close()
##data=json.dumps(risk_result)
##file = open('risk.json', 'w')
##file.write(data)
##file.close()
##with open('risk.json','r') as f:
##    xx=f.read()
##    
####print("原始数据是：", risk_list)
##print("结果数据是：", risk_result)
##print("xx:"+xx)
##
##print(type(json.loads(xx)))  ##用了json dumps 和 loads 就可以保证写入文件不改变格式

##data={'old':'','new':''}
##risk_list =  ['123','4567','8','9','10']
##data['old']=risk_list
##list1=['11','12','13']
##list2=[]
##data['old'].extend(list1)


##dict={'new':[],'old':[]}
##dict['new']=list(set(list1))
##data=json.dumps(dict)
##


##测试读取asin
##raw=[]
##try:
##    f=open("asin.json",'r')
##    data=f.read()
##    dict=json.loads(data)
##    print(dict)
##    f.close()
##    print("dict['old']:")
##    print(dict["old"])
##    raw.extend(dict["new"])
##    if(dict['old']!= []):
##        raw.extend(dict["old"])
##    print(raw)
##        
##except:
##    print("没有文件")
##
##raw=[]
##def getAsin(url):
##    pass
##from x import xx
##xx.lines(getAsin,"key.csv")#读取关键词

##n=None

######测试读取uid

# from lxml import etree
# import traceback
# e=''
# ##import re
# ##pattern = re.compile(r'account.(.*?)/')
# try:
#     f=open("new.txt",'r',encoding='utf-8')
#     txt=f.read()
#     print(txt)
#     html = etree.HTML(txt)
#     result = html.xpath('//pre/text()')
#     print(result)
#     if result !=[] :
#         e='q'
#     print(e)
#     if e=='q':
#         print("识别为机器人，退出")
# ##    result=pattern.findall(str(result))
# except:
#     print(traceback.format_exc())
#     print("没有文件")


# n=15000
# f=open("uid.json",'r')
# data=f.read()
# asins=json.loads(data)
# print(type(asins))
# f.close()
# if n<len(asins['new']):
#     print(len(asins['new']))
#     for i in range(n-1,len(asins['new'])):
#         if asins['new'][i]=='AHY6ROD5NYNGLKX4FUETFKG22NEQ' or asins['new'][i]=='AGVDYUCLWQFGNH5E7SOITHHJRRRA'or asins['new'][i]=='AEAALCNTWVQJXJHKINOULK6A2EEQ' or  asins['new'][i]=='AECNRE6R2BGBU4N5UZSVHZ6YQPFQ'  :
            
#             print(i+1)
        

####  匹配以前爬过的asin加入old

##f=open("10000.txt",'r')
##data=f.read()
####print(data)
##pattern = re.compile(r'.account.(.*?)/')
##result=pattern.findall(data)
##print(len(result))
##
####result=list(set(result))
####print(len(result))
##f.close()
##dict={'new':[],'old':[]}
##dict['old']=result
##data=json.dumps(dict)
##file = open('uid.json', 'w')
##file.write(data)
##file.close()

##for num in range(10000):
##    print(num)
