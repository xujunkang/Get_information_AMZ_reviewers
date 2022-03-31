import asyncio,re,json,traceback,time,shutil
from pyppeteer import launch
import deal_img
import yaml
with open("./config/config.yaml",'r' ) as stream: #读取配置文件
    config = yaml.safe_load(stream)
    
bro_data_path='E:/selenum/AutomationProfile'#浏览器数据保存路径
pattern = re.compile(r'account.(.*?)/')
global Total
Total=[]
decide="yes"
raw=[]##原始数据初始化为空
dict={'new':[],'old':[]}
n=0
num=lnum=0
tus=True#跳过读取好的数据的条件
imagepath='验证码.jpg'
try:
    with open("uids.json",'r',encoding="utf-8") as f:
            dict=json.load(f)

    print(type(dict))
    # print("初始dict['new']:"+str(dict['new']))
    # print("初始dict['old']:"+str(dict['old']))
    if(dict['new']!= []):
        raw.extend(dict["new"])##raw 获取原始数据
        while True:
            try:
                # decide=input("请输入yes/no,您是否要把NEW的数据存入Old？\n")
                decide='no'#现在先直接pass
                if(decide == "yes")or(decide=="no"):
                    break
                else:
                    print("你没有输入yes/no，请重新输入")
                    continue
            except:
                print("输入错误，请重新输入")
    if(dict['old']!= []):
        raw.extend(dict["old"])
    # print("raw:"+str(raw))
    print('有原始数据')
except:
    with open('uids.json','w+') as f:
        f.read()
        dict={}
        dict['new']= []
        dict['old']= []
    print("没有文件")
    print(traceback.format_exc())
    traceback.print_exc(file=open('error.txt','a+'))

class A:#用来实现res的状态
    ok=False
    status=500
 
def save():#保存
    global Total
    global decide
    global num
    global config
    global n
    Total=set(Total)
    if(decide == "yes"):
        dict['new']=list(Total.difference(set(raw)))
        dict['old']=list(set(raw))##如果没有asin文件raw默认为空，有asin文件 raw为之前的new+之前的old
    elif(decide == "no"):##为no不写入  new在自己的基础上进行更新,old不更新
        print(f"新加入的uid为：{len(list(Total.difference(set(dict['new']))))}个")
        dict['new'].extend(Total.difference(set(dict['new'])))

    # print("现在dict['new']:"+str(dict['new']))
    # print("现在dict['old']:"+str(dict['old']))
    # print("最后执行")
    with open('uids.json','w',encoding="utf-8") as f:
        json.dump(dict,f,ensure_ascii=False)
        print('写入成功')
        print(f"已经成功爬取{n}次")
        n=0 
    if num>0 and num>lnum:
        with open('./config/config.yaml', 'w') as f: 
            data = yaml.dump(config, f)
        print('保存配置文件成功')
        n=0
        





async def create_page(width=2,height=2):#创建一个浏览器和页面
    browser = await launch(headless=False, dumpio=True, 
                           args=[ f'--window-size={width},{height}', '--disable-infobars',f"--user-data-dir={bro_data_path}"])# 进入有头模式 headless=False
    page = await browser.newPage()
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.setViewport({'width': width, 'height': height})      # 页面大小一致
    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    return  page


async def url_get_data(page, asin,i):#得到数据的
    global Total
    url = f'https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr?_encoding=UTF8&showViewpoints=1&filterByStar=positive&pageNumber={i}'
    try:
        res=await page.goto(url)
    except BaseException:
        await page.browser.close()
        res=A()
        save()
        page=await create_page()
    return page,res


async def lookhome(page,res):#访问主页观察是否
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
            print(wh)
            await page.browser.close()
            res=A()
            page=await create_page(wh[0],wh[1])
    return page
async def yanzhenma(page):#识别验证码
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
                button=await page.xpath('//form//span/button')
                img=await page.xpath('//form//img')
            return page
        except BaseException:
            print(traceback.format_exc())
            traceback.print_exc(file=open('error.txt','a+'))
            print('被识别为机器人，清除数据重来')
            await page.browser.close()
            time.sleep(5)
            shutil.rmtree(bro_data_path)
            time.sleep(5)
            page =await create_page()
            res=A()
            page=await lookhome(page,res)
            save()
            return page
async def main():
    global Total#记录去重数组
    global n#记录爬取次数
    global tus
    global num#代表记录的asin位置
    global lnum#记录asin保存前的位置
    global config
    page=await create_page()
    res=A()
    page=await lookhome(page,res)  
    try:
        with open("asins.json","r",encoding="utf-8") as f:
            asins=json.load(f)
        asinlist=list(asins[list(asins.keys())[1]].values())[0]#读取出asins数据的asin数组
        num=asinlist.index(config['asin'])
        lnum=num
        for l,asin in enumerate(asinlist):
            if l==num or config['asin']=='':
                tus=False
            if tus:
                continue#跳过之前循环
            
            for i in range(1,10000):
                if i<config['anum']:
                    continue
                n+=1
                page,res=await url_get_data(page, asin,i)
                while not res.ok or res.status!=200: 
                    page,res=await url_get_data(page, asin,i)
                    if res.status!=200 and res.status!=500:
                        print('页面状态异常')
                        break
                # page_text = await page.content()   # 获取网页源码
                # print(page_text)
                # with open("test.html",'w',encoding='utf-8') as f:#写入测试文件
                #     f.write(page_text)
                # html = etree.HTML(page_text)#试着直接调用await page.xpath
                result = await page.xpath('//*[@id="cm_cr-review_list"]/div//a[@class="a-profile"]/@href')
                result=[await (await rst.getProperty('textContent')).jsonValue() for rst in result]
                status=await page.xpath('//div[@class="a-section"]//form/@action')
                result=pattern.findall(str(result))
                
                while status!=[]:#被识别到爬虫
                    page= await yanzhenma(page)
                    page,res=await url_get_data(page, asin,i)
                    status=await page.xpath('//div[@class="a-section"]//form/@action')
                    if status==[]:
                        save()
                if len(result)<10:
                    print(f"该asin：{asin} 读取完毕")#这页评论数不正常时执行
                    config['anum']=0
                    num=num+1
                    break
                else:
                    Total=list(Total)
                    Total.extend(result)
                    ##去重Total节省空间
                    config['anum']=i
                    config['asin']=asin
                    print(i)
                    time.sleep(1)
                    continue
    except BaseException:
        print(traceback.format_exc())
        traceback.print_exc(file=open('error.txt','a+'))
    finally:
        save()

try:
    asyncio.get_event_loop().run_until_complete(main()) #调用
except BaseException:
    print(traceback.format_exc())
    traceback.print_exc(file=open('error.txt','a+'))
finally:
    save()
