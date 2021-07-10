import urllib
import requests
import time
import json
import random
import re
from urllib import parse
import urllib3
import sys
urllib3.disable_warnings()
import os
#活动地址
#https://wbbny.m.jd.com/babelDiy/Zeus/2rtpffK8wqNyPBH6wyUDuBKoAbCt/index.html#

print('欢迎使用jd脚本，有问题可以咨询作者QQ：1811881314\n')
print('原创教程：https://www.yqhd8.com/hd/3587 \n')
#循环任务次数，可以多跑几次没事
task_times = 3
#间隔时间，默认在任务所需的基础上加，一般设置2s左右就成，看自己
sleep_times = 2


Cookies = []
try:
    with open('ck.txt','r', encoding='utf-8') as ef:
        for i in ef:
            i = i.strip('\r\n')
            Cookies.append(i)
except:
    print('看看有ck.txt文件没，看看放cookie没')
    time.sleep(5)
    sys.exit()
if Cookies:
    pass
else:
    print('看看放cookie没')
    time.sleep(5)
    sys.exit()

print('软件放了作者的助力，不想助力的直接输入n 回车即可\n')
#获取joytoken
def get_joytoken(headers):
    url = 'https://bh.m.jd.com/gettoken'
    data = 'content={"appname":"50085","whwswswws":"icmdZhjZCcDg56Vxkah2W0Q==","jdkey":"a","body":{"platform":"1"}}'
    
    try:
        res = requests.post(url,headers=headers,data=data,verify=False).json()
        joytoken = res.get('joyytoken')
        return joytoken
    except:
        return None

#逛店
def guangdian(taskId,taskToken,itemId,buttonid,headers):
    randomnum = random.randint(12345678,99999999)
    url = 'https://api.m.jd.com/client.action?advId=olympicgames_doTaskDetail'
    data = 'functionId=olympicgames_doTaskDetail&body={"taskId":%s,"taskToken":"%s","ss":"{\\"extraData\\":{\\"log\\":\\"-1\\",\\"sceneid\\":\\"OY217hPageh5\\"},\\"random\\":\\"%s\\"}","actionType":1}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act' % (taskId,taskToken,randomnum)
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('进店成功')
            return res
        else:
            print(res.get('data').get('bizMsg'))
    except:
        print('其他')

#领取
def lingqu(taskToken,headers):
    url = 'https://api.m.jd.com/client.action?functionId=qryViewkitCallbackResult&client=wh5&clientVersion=1.0.0'
    body = {
        'dataSource': "newshortAward",
        'method': "getTaskAward",
        'reqParams': "{\"taskToken\":\"%s\"}" % taskToken,
    }
    bodys = json.dumps(body)
    data = {
        'body':bodys,
        'joycious':73,
        "sdkVersion":"1.0.0",
        "clientLanguage":"zh"
    }
    try:
        response = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if response.get('code') == '0':
            print(response.get('toast').get('subTitle'))
        else:
            print('其他')
    except:
        print('其他')

def getFeedDetail(taskId,headers):
    url = 'https://api.m.jd.com/client.action?functionId=olympicgames_getFeedDetail'
    data = 'functionId=olympicgames_getFeedDetail&body={"taskId":"%s"}&client=wh5&clientVersion=1.0.0&uuid=ef746bc0663f7ca06cdd1fa724c15451900039cf&appid=o2_act' % taskId
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        productInfoVos = res.get('data').get('result').get('addProductVos')[0].get('productInfoVos')
        return productInfoVos
    except:
        print('其他')

#任务列表
def task_list(headers,data):
    url = "https://api.m.jd.com/client.action?functionId=olympicgames_getTaskDetail"
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if res.get('code') == 0:
            taskVos = res.get('data').get('result').get('taskVos')
            return taskVos
        else:
            print(res.get('msg'))
    except:
        print('其他')
def vxtask_list(headers,data):    
    try:
        taskVos = task_list(headers,data)
        lists = []
        for i in taskVos:
            taskId = i.get('taskId')
            status = i.get('status')
            taskTitle = i.get('taskName')
            if status == 1:
                waitDuration = i.get('waitDuration')
                shoppingActivityVos = i.get('shoppingActivityVos','')
                browseShopVos = i.get('browseShopVo','')
                buttonid = 'jmdd-react-smash_73'
                #  2、14、26过滤 
                if taskId in [1,3,4,5,6,8,19,20,23,24,25]:  #
                    print('>>>>>开始进行%s任务' % taskTitle)
                    for shop in shoppingActivityVos:
                        shopstatus = shop.get('status')
                        taskToken = shop.get('taskToken')
                        shoptitle = shop.get('title')
                        itemId = shop.get('itemId')
                        if shopstatus == 1:
                            print('任务“%s”' % shoptitle)
                            guangdian(taskId,taskToken,itemId,buttonid,headers)
                            print('等待%s秒' %  (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                            lingqu(taskToken,headers)
                if taskId in [7,15,18,21]:
                    print('>>>>>开始进行%s任务' % taskTitle)
                    for shop in shoppingActivityVos:
                        shopstatus = shop.get('status')
                        taskToken = shop.get('taskToken')
                        shoptitle = shop.get('title')
                        itemId = shop.get('itemId')
                        if shopstatus == 1:
                            print('任务“%s”' % shoptitle)
                            guangdian(taskId,taskToken,itemId,buttonid,headers)
                            print('等待%s秒' %  (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                if taskId in [9,22]:
                    print('>>>>>开始进行%s任务' % taskTitle)
                    for browseShop in browseShopVos:
                        browsestatus = browseShop.get('status')
                        browsetaskToken = browseShop.get('taskToken')
                        shopName = browseShop.get('shopName')
                        shopId = browseShop.get('shopId')
                        if browsestatus == 1:
                            print('任务“%s”' % shopName)
                            guangdian(taskId,browsetaskToken,shopId,buttonid,headers)
                            print('等待%s秒' %  (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                            lingqu(browsetaskToken,headers)
                # if taskId == 22:
                #     print('>>>>>开始进行%s任务' % taskTitle)
                #     for browseShop in browseShopVos:
                #         browsestatus = browseShop.get('status')
                #         browsetaskToken = browseShop.get('taskToken')
                #         shopName = browseShop.get('shopName')
                #         shopId = browseShop.get('shopId')
                #         if browsestatus == 1:
                #             print('任务“%s”' % shopName)
                #             guangdian(taskId,browsetaskToken,shopId,buttonid,headers)
                #             print('等待%s秒' % sleep_times)
                #             time.sleep(sleep_times)
                #加购
                if taskId in [10,11,12,13]:
                    print('>>>>>开始进行%s任务' % taskTitle)
                    productInfoVos = getFeedDetail(taskId,headers)
                    for productInfoVo in productInfoVos:
                        itemId = productInfoVo.get('itemId')
                        taskToken = productInfoVo.get('taskToken')
                        skuName = productInfoVo.get('skuName')
                        status = productInfoVo.get('status')
                        if status == 1:
                            print('开始加购“%s”' % skuName)
                            ress = guangdian(taskId,taskToken,itemId,buttonid,headers)
                            times = ress.get('data').get('result').get('times')
                            if times == 5:
                                break
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
                if taskId == 17:
                    print('>>>>>开始进行%s任务' % taskTitle)
                    productInfoVos = i.get('productInfoVos')
                    for productInfoVo in productInfoVos:
                        itemId = productInfoVo.get('itemId')
                        taskToken = productInfoVo.get('taskToken')
                        skuName = productInfoVo.get('skuName')
                        status = productInfoVo.get('status')
                        if status == 1:
                            print('开始逛店“%s”' % skuName)
                            ress = guangdian(taskId,taskToken,itemId,buttonid,headers)
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
            if status == 2:
                print(taskTitle + '任务已完成')
    except Exception as e:
        print(e)
#助力
def jd_zhuli(inviteId,headers):
    randomnum = random.randint(12345678,99999999)
    url = 'https://api.m.jd.com/client.action?functionId=olympicgames_assist'
    body = {
        "ss":'{\\"extraData\\":{\\"log\\":\\"-1\\",\\"sceneid\\":\\"OY217hPageh5\\"},\\"random\\":\\"%s\\"}' % randomnum,
        "inviteId":inviteId
        }
    bodys = json.dumps(body)
    data = 'functionId=olympicgames_assist&body=%s&client=wh5&clientVersion=1.0.0&uuid=ef746bc0663f7ca06cdd1fa724c15451900039cf&appid=o2_act' % bodys
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('进店成功')
            return res
        else:
            print(res.get('data').get('bizMsg'))
    except:
        print('其他')
inviteIds = ['HcmphIzxA1z2LcfLRIF_mmWd2D8sqX8IqY_Kb-hdNW34hvAuqwFy3-1dpHWE6LUy4fQ',\
    'HcmphLbwLg2kKoDMQdA11hEgurvh1T_hRkHRo0VMiHf6BZ4sHxC8zHF2AL8mIb6qcHtPp0HLZu_0yF2qbAjOPw',\
    'HcmphLbwLgzyK4OTH4A7h-USOGiJlZWENw9UwewEvlIB4uhw84MNmENKYNoIv7ai_nzBPxTH9os1-S5IHLGNSA',\
    'HcmphLr4EE7nK8HWW5hX1o-qmFtwyUwmOHsnpBJo5X12i-qlglms0UGEhw']
def get(functionId,headers):
    url = 'https://api.m.jd.com/client.action?advId=%s' % functionId

    body = {
        "type":2,
        "ss":"{\"extraData\":{\"log\":\"-1\",\"sceneid\":\"OY217hPageh5\"},\"random\":\"66697357\"}",
        }
    bodys = json.dumps(body)
    data = 'functionId={0}&body={1}&client=wh5&clientVersion=1.0.0&uuid=ef746bc0663f7ca06cdd1fa724c15451900039cf&appid=o2_act'.format(functionId,bodys)
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print(res.get('data').get('result'))
        else:
            print(res.get('data').get('bizMsg'))
    except:
        print('其他')

#-----------------------------------------------------------
def tujian(headers,types,data):
    url = 'https://api.m.jd.com/client.action?functionId=%s' % types
    res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
    return res

#任务
def bdDoTask(headers,taskId,taskToken,shopSign):
    randomnum = random.randint(12345678,99999999)
    data = 'functionId=olympicgames_doTaskDetail&body={"taskId":%s,"taskToken":"%s","ss":"{\\"extraData\\":{\\"log\\":\\"-1\\",\\"sceneid\\":\\"OY217hPageh5\\"},\\"random\\":\\"%s\\"}","shopSign":"%s","actionType":1}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act' % (taskId,taskToken,randomnum,shopSign)
    res = tujian(headers, 'olympicgames_bdDoTask', data)
    return res

#拆盲盒子
def chai(headers,shopSign):
    url = 'https://api.m.jd.com/client.action?functionId=olympicgames_boxShopLottery'
    data = 'functionId=olympicgames_boxShopLottery&body={"shopSign":"%s"}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act' % shopSign
    try:
        response = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        if response.get('code') == 0:
            if response.get('data').get('bizCode') == 0:
                print(response.get('data').get('result'))
            else:
                print(response.get('data').get('bizMsg'))
        else:
            print(response.get('msg'))
    except Exception as e:
        print(e)

#做任务
def shop_task(headers,shopid,shopname):
    data = 'functionId=olympicgames_shopLotteryInfo&body={"channelSign":"1","shopSign":"%s"}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act' % shopid
    try:
        response = tujian(headers,'olympicgames_shopLotteryInfo',data)
        if response.get('code') == 0:
            taskVos = response.get('data').get('result').get('taskVos')
            for task in taskVos:
                taskId = task.get('taskId')
                status = task.get('status')
                waitDuration = task.get('waitDuration')
                taskName=task.get('taskName')
                if status == 1:
                    if taskId == 1:
                        taskToken = task.get('simpleRecordInfoVo').get('taskToken')
                        s = bdDoTask(headers,taskId,taskToken,shopid)
                        if s.get('code') == 0:
                            if s.get('data').get('bizCode') == 0:
                                acquiredScore = s.get('data').get('result').get('acquiredScore')
                                print('签到成功，获得%s个金币' % acquiredScore)
                            else:
                                print(s.get('data').get('bizMsg'))
                        else:
                            print(s.get('msg'))
                    # if taskId in [4,5]:
                    #     shoppingActivityVos = task.get('shoppingActivityVos')
                    #     for shoppingActivity in shoppingActivityVos:
                    #         taskToken = shoppingActivity.get('taskToken')
                    #         print('任务“%s”' % taskName)
                    #         bdDoTask(headers,taskId,taskToken,shopid)
                    #         print('等待%s秒' %  (waitDuration + sleep_times))
                    #         time.sleep(int(waitDuration + sleep_times))
                    #         lingqu(taskToken,headers)
                    if taskId in [4,5]:
                        browseShopVos = task.get('browseShopVo')
                        for browseShopVo in browseShopVos:
                            taskToken = browseShopVo.get('taskToken')
                            print('任务“%s”' % taskName)
                            s = bdDoTask(headers,taskId,taskToken,shopid)
                            if s.get('data').get('bizCode') == 0:
                                print('进店成功，获得%s金币' % s.get('data').get('result').get('acquiredScore'))
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
                    if taskId == 6:
                        shoppingActivityVos = task.get('shoppingActivityVos')
                        for shoppingActivityVo in shoppingActivityVos:
                            taskToken = shoppingActivityVo.get('taskToken')
                            print('任务“%s”' % taskName)
                            s = bdDoTask(headers,taskId,taskToken,shopid)
                            if s.get('data').get('bizCode') == 0:
                                print('进店成功，获得%s金币' % s.get('data').get('result').get('acquiredScore'))
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
            boxLotteryNum = response.get('data').get('result').get('boxLotteryNum')
            if shopname:
                print('%s还有%s次盲盒抽奖机会' % (shopname,boxLotteryNum))
            else:
                print('ID:%s还有%s次盲盒抽奖机会' % (shopid,boxLotteryNum))
            sss = 0
            while sss<boxLotteryNum:
                chai(headers,shopid)
                time.sleep(sleep_times)
                sss += 1
        else:
            print(response.get('msg'))
    except Exception as e:
        print(e)
#店铺任务
def dianpu_renwu(headers):
    body = {"qryParam":"[{\"type\":\"advertGroup\",\"id\":\"05371960\",\"mapTo\":\"dataList\",\"next\":[{\"type\":\"productGroup\",\"mapKey\":\"extension.progId\",\"mapTo\":\"productList\"}]},{\"type\":\"advertGroup\",\"id\":\"05397406\",\"mapTo\":\"dataExtra\"}]","openid":-1,"applyKey":"big_promotion"}
    bodys = json.dumps(body)
    data = 'functionId=qryCompositeMaterials&body=%s&client=wh5&clientVersion=1.0.0&uuid=network/wifi' % bodys
    try:
        response = tujian(headers,'qryCompositeMaterials',data)
        if response.get('code') == '0':
            lists = response.get('data').get('dataList').get('list')
            for shop in lists:
                shopid = shop.get('extension').get('shopId')
                shopname = shop.get('name','')
                shop_task(headers,shopid,shopname)
                time.sleep(sleep_times)
        else:
            print(response.get('code'))
    except Exception as e:
        print(e)

print('是否愿意为作者助力：y/n')
content = input()

for Cookie in Cookies:
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent':'jdapp;iphone;android;8.3.0;10;network/wifi;model/MI 6;addressid/541286672;aid/d41d8cd98f00b204',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://wbbny.m.jd.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://wbbny.m.jd.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie':Cookie
    }
    joyToken = get_joytoken(headers)
    Cookie =  Cookie + ';joyytoken=50085' + joyToken
    headers['Cookie'] = Cookie
    i = 0
    while i < task_times:
        #京东app任务
        jddata = 'functionId=olympicgames_getTaskDetail&body={"taskId":"","appSign":"1"}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act'
        vxtask_list(headers,jddata)
        #微信任务
        wxdata = 'functionId=olympicgames_getTaskDetail&body={"taskId":"","appSign":"2"}&client=wh5&clientVersion=1.0.0&uuid=73a07746ec2192f3c44fa31f25c800e2a79bcbb8&appid=o2_act'
        vxtask_list(headers,wxdata)
        #运动
        get('olympicgames_startTraining',headers)
        #加速
        get('olympicgames_speedTraining',headers)
        #领
        get('olympicgames_collectCurrency',headers)
        dianpu_renwu(headers)
        time.sleep(5)
        i+=1

    if content != 'n':
        for inviteId in inviteIds:
            jd_zhuli(inviteId, headers)
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))))
print('输入任意键结束：')
input()