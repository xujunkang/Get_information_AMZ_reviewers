import json
def and_file():
    new_uids=[]
    old_uids=[]
    
    with open("uids.json",'r',encoding="utf-8") as f:
        dic=json.load(f)
        new_uids.extend(dic['new'])
    
    with open("./config/uids.json",'r',encoding='utf-8' ) as f: #读取用户数据文件
        uids =json.load(f)
        uids['new']=list(set(uids['new']).difference(set(uids['old'])))#old与new去重合并
        n=len(uids['new'])
        
        olist=uids['old']+uids['new']
        old_uids.extend(olist)
        
    uids['new'].extend(list(set(new_uids).difference(set(old_uids))))
    if len(uids['new'])>n:
        with open('./config/uids.json','w',encoding="utf-8") as f:
            json.dump(uids,f,ensure_ascii=False)
            print('合并成功')
    elif len(uids['new'])==n:
        print('文件读取成功,但是大小一样')
    
