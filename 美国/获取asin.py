import keepa
import tokens,json,fanyi
f=open("asins.json","r",encoding="utf-8")
# global asins
asins=json.load(f)
f.close()
alist={}
domain='US'
cid='172282'
api = keepa.Keepa(tokens.keepakey)
# list=api.category_lookup('0',domain='US')
# print(list)
caname=api.category_lookup(cid,domain=domain)[cid]["name"]
name=fanyi.baidu(caname+""+domain)
asinslist=api.best_sellers_query(cid,domain=domain)#得到卖的好的asin列表
asins[cid]={name:asinslist}
f=open("asins.json","w",encoding="utf-8")
json.dump(asins,f,ensure_ascii=False)
f.close()
print(f"保存分类{name}BestASIN成功")