import asyncio, time,subprocess,re,json,traceback,deal_img,shutil,os
import fileand
from pyppeteer import launcher,launch
import csv
##设置匹配规则
url_s = re.compile(r'"url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])","iconUrl"')#匹配网站规定url地址
url_o = re.compile(r'"raw":"(\b(?!null)\S+)","no')#匹配个人url地址
pattern=url_s.pattern+'|'+url_o.pattern#匹配出有网址的
pinterest=re.compile(r'"pinterest","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#缤趣匹配
twitter=re.compile(r'"twitter","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#推特匹配
instagram=re.compile(r'"instagram","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#ins匹配
youtube=re.compile(r'"youtube","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#油管匹配
facebook=re.compile(r'"facebook","url":"(https?:[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])",')#脸书匹配
rank=re.compile(r'"rank":"(\b(?!null)\S+)","decoratedRank"')#排名匹配
n=0#记录爬虫运行次数
ws=''
imagepath='验证码2.jpg'
bro_data_path='E:/pyppeteer/AutomationProfile'#浏览器数据保存路径，目标文件
sou_data_path='E:/pyppeteer/AutomationProfile1'


url1='https://www.amazon.com/profilewidget/bio/amzn1.account.AHBWYXLAUDL7IAR3UFYDQIY6NRCQ?view=visitor'


csv_file = open('./config/user.csv', 'r', newline='', encoding='utf-8')#编码方式与写入文件时相同
reader_csv = csv.reader(csv_file)

udata={}#定义全局变量用户数据

class A:#用来实现res的状态
    ok=False
    status=500
raw=[]##原始数据初始化为空
with open("./config/uids.json",'r',encoding='utf-8' ) as f: #读取用户数据文件
    uids =json.load(f)
    raw.extend(uids["old"])##raw 获取原始数据

newlist=uids['new']
oldlist=uids['old']#也是全局变量

async def yanzhenma(page):#识别验证码
     # await page.browser.close()
        try:
            print(f"被识别到爬虫，运行次数{n}")
            await page.browser.close() 
            page=await create_page(1920,1080)#截图验证码要更换窗体大小，以截图准确
            res=A()
            page=await lookhome(page,res)
            button=await page.xpath('//form//span/button')
            img=await page.xpath('//form//img')
            while button !=[] and img!=[]:
                await img[0].screenshot({'path': imagepath})
                img_str=deal_img.deal(imagepath)
                if img_str!='验证码错误' and img_str!='':
                    print("图片获取成功")
                    print(img_str)
                    await page.type("#captchacharacters",img_str)
                    await button[0].click()
                    time.sleep(5)
                elif img_str=='':
                    print("图片识别到为空")
                    await button[0].click()
                page=await create_page()
                page=await lookhome(page,res)
                button=await page.xpath('//form//span/button')
                img=await page.xpath('//form//img')
            return page
        except BaseException:
            print(traceback.format_exc())
            traceback.print_exc(file=open('error.txt','a+'))
            print('被识别为机器人，清除数据重来')
            await page.browser.close()
            time.sleep(5)
            cls()
            time.sleep(5)
            page =await create_page()
            res=A()
            page=await lookhome(page,res)
            save()
            return page
            



async def lookhome(page,res):#访问主页观察是否正常,返回正常主页
    while not res.ok or res.status!=200: # 响应状态码
        try:
            res=await page.goto("https://amazon.com") # 访问主页                
        # resp_headers = res.headers  # 响应头
        # resp_status = res.status    # 响应状态
        # resp_url = res.url          # 请求地址
        except BaseException:
            wh = await page.evaluate('''() => {
        return [document.documentElement.clientWidth,document.documentElement.clientHeight,
        ]  }''')
            await page.browser.close()
            print(wh)
            res=A()
            page=await create_page(wh[0],wh[1])
    return page
async def visithost(page,uid):#访问卖家主页获取信息
    url=f"https://www.amazon.com/gp/profile/amzn1.account.{uid}/ref=cm_cr_arp_d_gw_rgt?ie=UTF8"
    try:
        res=await page.goto(url)
    except BaseException:
        await page.browser.close()
        res=A()
        page=await create_page()
    return page,res

def save():#保存配置文件
    global udata
    global oldlist
    global newlist
    global uids
    saveuser(udata)#先保存用户数据
    oldlist=set(oldlist)
    # print(oldlist)
    # print(raw)
    print(f'新读取的数量{len(oldlist.difference(set(raw)))}')
    newlist=list(set(newlist).difference(oldlist))#新数据去重
    uids['new']=newlist
    uids['old']=list(oldlist)
    with open('./config/uids.json','w',encoding="utf-8") as f:
        json.dump(uids,f,ensure_ascii=False)
        print('写入成功')
    try:
        fileand.and_file()
    except BaseException:
        print('文件合并失败未知错误')
        
def cls(sou_data_path=sou_data_path,tar_data_path=bro_data_path):#清除浏览器文件夹或者说还原
    source_path = os.path.abspath(sou_data_path)#原文件
    target_path = os.path.abspath(tar_data_path)#浏览器现在保留文件

    if not os.path.exists(source_path):
        # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(source_path)

    if os.path.exists(target_path):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)
    print('清除复制文件成功')
        

    
    
def saveuser(udata):#保存用户数据
    print(f'现在的用户数据：{udata}')
    if reader_csv.line_num==0:#判断有无数据
         with open('./config/user.csv', 'a', newline='', encoding='utf-8') as csvf:
            write=csv.writer(csvf)
            title=['facebook网址','twitter网址','instagram网址','youtube网址','pinterest网址','个人主页展示网址(可能是无效的)','亚马逊评论者排名','亚马逊个人主页网址']
            write.writerow(title)#写入标题
            
    if len(udata.keys())>0:#判断已保存的数据更大
        with open('./config/user.csv', 'a', newline='', encoding='utf-8') as csvf:#追加写入吧
            write=csv.writer(csvf)
            for i in udata.keys():
                write.writerow(udata[i]+[f'https://www.amazon.com/gp/profile/amzn1.account.{i}/ref=cm_cr_arp_d_gw_rgt?ie=UTF8'])
            print('写入用户数据文件成功')
    elif n<10:
        print('数据有误，不退出重来')
    else :
        print('数据有误退出重来')
        cls()



async def create_page(width=2,height=2):#创建一个浏览器页面->浏览器可以通过页面获取
    global ws
    try:
        browser = await launch(headless=False, dumpio=True, 
                           args=[ f'--window-size={width},{height}', '--disable-infobars',f"--user-data-dir={bro_data_path}"])# 进入有头模式 headless=False
        
        ws = browser.wsEndpoint
        page = await browser.newPage()
    except BaseException:
        print(traceback.format_exc())
        traceback.print_exc(file=open('error.txt','a+'))
        browser=await launcher.connect({'browserWSEndpoint':ws})
        page=await browser.newPage()

       
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.setViewport({'width': width, 'height': height})      # 页面大小一致
    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    return page

def shuju(page_text,ulist):
    f=facebook.findall(page_text)
    t=twitter.findall(page_text)
    i=instagram.findall(page_text)
    y=youtube.findall(page_text)
    p=pinterest.findall(page_text)
    u=url_o.findall(page_text)
    r=rank.findall(page_text)
    
    if f!=[]:
        ulist.append(f[0])
    else:
        ulist.append('')
    if t!=[]:
        ulist.append(t[0])
    else:
        ulist.append('')
    if i!=[]:
        ulist.append(i[0])
    else:
        ulist.append('')
    if y!=[]:
        ulist.append(y[0])
    else:
        ulist.append('')
    if p!=[]:
        ulist.append(p[0])
    else:
        ulist.append('')
    if u!=[]:
        ulist.append(u[0])
    else:
        ulist.append('')
    if r!=[]:
        ulist.append(r[0])
    else:
        ulist.append('')

    
    
    return ulist

async def main():
    global udata
    global oldlist
    global newlist
    global n
    global ws
    page = await  create_page()           # 打开新的标签页
    res=A()
    page=await lookhome(page,res)
    ws=page.browser.wsEndpoint

    for uid in newlist:
        # uid='AHHLX5PTP6KAUIRCSQIHMODICYWQ'#测试用
        page,res=await visithost(page,uid)
        while not res.ok or res.status!=200:  
            if res.status!=500 and res.status!=200:#亚马逊检测到异常行为被封号
                print(uid+'变狗了')
                page=await lookhome(page,res)
                break
            page,res=await visithost(page,uid)  
        status=await page.xpath('//div[@class="a-section"]//form/@action')#识别爬虫状态
        while status!=[]:
                page= await yanzhenma(page)
                page,res=await visithost(page,uid)
                status=await page.xpath('//div[@class="a-section"]//form/@action')#识别爬虫状态
                
        page_text = await page.content()   # 获取网页源码
        
        if len(page_text)<200:#被识别为机器人
            print('被识别为机器人，清除数据重来')
            await page.browser.close()
            cls()
            page =await create_page()
        
        ulist=[]#临时变量列表保存写入udata
        # print(page_text)
        # with open('x.html','w',encoding='utf-8') as f:#测试时看抓取的页面是什么
        #     f.write(page_text)
        result=re.findall(pattern,page_text)#得到网页是否有网址的结果
        if result!=[]:
            ulist=shuju(page_text,ulist)#数据处理
            udata[uid]=ulist#格式化数据
        oldlist.append(uid)#读完的数据加入old
        n=n+1
        print(f'爬虫运行{n}次,这次爬取{uid}')
        time.sleep(1)
    save()#保存数据
    
    # print(page_text)
    
try:
    asyncio.get_event_loop().run_until_complete(main()) #调用
except BaseException:
    print(traceback.format_exc())
    traceback.print_exc(file=open('error.txt','a+'))
finally:
    save()

