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
import execjs

#活动地址
#https://wbbny.m.jd.com/babelDiy/Zeus/2s7hhSTbhMgxpGoa9JDnbDzJTaBB/index.html#/home

#欢迎使用jd脚本，有问题可以咨询作者QQ：1811881314

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
    sys.exit()

#初始化
def get_secretp(headers):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_getHomeData'
    data = 'functionId=zoo_getHomeData&body={}&client=wh5&clientVersion=1.0.0'
    res = requests.post(url,data=data,headers=headers,verify=False,timeout=5).json()
    if res.get('data').get('bizCode') == 0:
        return res.get('data').get('result').get('homeMainInfo').get('secretp')
    else:
        print('初始化失败')
        return None
#签到
def sign(headers):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_sign'
    data = 'functionId=zoo_sign&body={}&client=wh5&clientVersion=1.0.0'
    try:
        res = requests.post(url,headers=headers,data=data,verify=False).json()
        if res.get('code') == 0:
            if res.get('data').get('bizCode') == 0:
                redPacketValue = res.get('data').get('result').get('redPacketValue')
                print('签到成功，获得%s元红包' % redPacketValue)
            else:
                print(res.get('data').get('bizMsg'))
        else:
            print(res.get('msg'))
    except:
        print('其他')

def get_ss(secretp):
    js = open('jiami.js','r',encoding='utf-8')
    
    ctx = execjs.compile(js.read())
    ss = ctx.call('enString',secretp)
    return ss

#逛店
def guangdian(taskId,taskToken,itemId,buttonid,headers):
    ss = get_ss(secretp)
    url = 'https://api.m.jd.com/client.action?functionId=zoo_collectScore'
    body = {
        "taskId":taskId,
        "actionType":1,
        "taskToken":taskToken,
        "ss":ss,
        }
    bodys = json.dumps(body)
    data = 'functionId=zoo_collectScore&body=%s&client=wh5&clientVersion=1.0.0' % bodys
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
    url = 'https://api.m.jd.com/client.action?client=wh5&clientVersion=1.0.0&functionId=qryViewkitCallbackResult&body='
    body = {
        'dataSource': "newshortAward",
        'method': "getTaskAward",
        'reqParams': "{\"taskToken\":\"%s\"}" % taskToken,
        'sdkVersion': "1.0.0",
        'clientLanguage': "zh"
    }
    bodys = json.dumps(body)
    uri = url + bodys
    try:
        response = requests.get(uri,headers=headers,verify=False,timeout=5).json()
        if response.get('code') == '0':
            print(response.get('toast').get('subTitle'))
        else:
            print('其他')
    except:
        print('其他')
def getFeedDetail(taskId,headers):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_getFeedDetail'
    data = 'functionId=zoo_getFeedDetail&body={"taskId":"%s"}&client=wh5&clientVersion=1.0.0' % taskId
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
        productInfoVos = res.get('data').get('result').get('addProductVos')[0].get('productInfoVos')
        return productInfoVos
    except:
        print('其他')

#任务列表
def task_list(headers,data):
    url = "https://api.m.jd.com/client.action?functionId=zoo_getTaskDetail"
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
            if taskId in [1,3,4,5,6,8,19,20,23]:
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
            if taskId in [7,15,21]:
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
            if taskId == 9:
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
            if taskId == 22:
                print('>>>>>开始进行%s任务' % taskTitle)
                for browseShop in browseShopVos:
                    browsestatus = browseShop.get('status')
                    browsetaskToken = browseShop.get('taskToken')
                    shopName = browseShop.get('shopName')
                    shopId = browseShop.get('shopId')
                    if browsestatus == 1:
                        print('任务“%s”' % shopName)
                        guangdian(taskId,browsetaskToken,shopId,buttonid,headers)
                        print('等待%s秒' % sleep_times)
                        time.sleep(sleep_times)
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
            if taskId == 24:
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
#动物图鉴-----------------------------------------------------------
def tujian(headers,types,data):
    url = 'https://api.m.jd.com/client.action?functionId=%s' % types
    res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
    return res

#分享任务
def zoo_getWelfareScore(headers,currentScence):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_getWelfareScore'
    body = {"type": 2,"currentScence":currentScence,"ss":get_ss(secretp)}
    bodys = json.dumps(body)
    data = 'functionId=zoo_getWelfareScore&body=%s&client=wh5&clientVersion=1.0.0' % bodys
    res = requests.post(url,headers=headers,data=data,verify=False,timeout=5).json()
    return res

#完成图鉴逛店任务
def zoo_bdCollectScore(headers,taskId,taskToken,shopSign):
    body = {"taskId": taskId,"actionType":1,"taskToken":taskToken,"ss":get_ss(secretp),"shopSign":shopSign}
    bodys = json.dumps(body)
    data = 'functionId=zoo_bdCollectScore&body=%s&client=wh5&clientVersion=1.0.0' % bodys
    res = tujian(headers, 'zoo_bdCollectScore', data)
    return res
#完成分享任务
def tujian_share(headers):
    data = 'functionId=zoo_myMap&body={}&client=wh5&clientVersion=1.0.0&uuid=network/wifi'
    try:
        response = tujian(headers,'zoo_myMap',data)
        if response.get('code') == 0:
            sceneInfos = response.get('data').get('result').get('sceneMap').get('sceneInfo')
            #分享任务
            print('开始分享任务')
            times = len(sceneInfos)
            i = 1
            while i < times:
                welfare  = zoo_getWelfareScore(headers, i)
                if welfare.get('code') == 0:
                    if welfare.get('data').get('bizCode') == 0:
                        score = welfare.get('data').get('result').get('score')
                        print('分享获得%s个金币' % score)
                    else:
                        print(welfare.get('data').get('bizMsg'))
                else:
                    print(res.get('msg'))
                time.sleep(2)
                i += 1
        else:
            print(response.get('msg'))
    except Exception as e:
        print(e)
#拆盲盒子
def chai(headers,shopSign):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_boxShopLottery'
    data = 'functionId=zoo_boxShopLottery&body={"shopSign":"%s"}&client=wh5&clientVersion=1.0.0' % shopSign
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
def shop_task(headers,shopid):
    data = 'functionId=zoo_shopLotteryInfo&body={"shopSign":"%s"}&client=wh5&clientVersion=1.0.0&uuid=network/wifi' % shopid
    try:
        response = tujian(headers,'zoo_shopLotteryInfo',data)
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
                        s = zoo_bdCollectScore(headers,taskId,taskToken,shopid)
                        if s.get('code') == 0:
                            if s.get('data').get('bizCode') == 0:
                                acquiredScore = s.get('data').get('result').get('acquiredScore')
                                print('签到成功，获得%s个金币' % acquiredScore)
                            else:
                                print(s.get('data').get('bizMsg'))
                        else:
                            print(s.get('msg'))
                    if taskId in [4,5]:
                        shoppingActivityVos = task.get('shoppingActivityVos')
                        for shoppingActivity in shoppingActivityVos:
                            taskToken = shoppingActivity.get('taskToken')
                            print('任务“%s”' % taskName)
                            zoo_bdCollectScore(headers,taskId,taskToken,shopid)
                            print('等待%s秒' %  (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                            lingqu(taskToken,headers)
                    if taskId == 6:
                        shoppingActivityVos = task.get('shoppingActivityVos')
                        for shoppingActivity in shoppingActivityVos:
                            taskToken = shoppingActivity.get('taskToken')
                            print('任务“%s”' % taskName)
                            s = zoo_bdCollectScore(headers,taskId,taskToken,shopid)
                            if s.get('data').get('bizCode') == 0:
                                print('进店成功，获得%s金币' % s.get('data').get('result').get('acquiredScore'))
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
        else:
            print(response.get('msg'))
        boxLotteryNum = tujian(headers,'zoo_shopLotteryInfo',data).get('data').get('result').get('boxLotteryNum')
        print('还有%s次盲盒抽奖' % boxLotteryNum)
        sss = 0
        while sss<boxLotteryNum:
            chai(headers,shopid)
            time.sleep(sleep_times)
            sss += 1

    except Exception as e:
        print(e)
#获取shopid
def tujian_renwu(headers):
    body = {"qryParam":"[{\"type\":\"advertGroup\",\"mapTo\":\"resultData\",\"id\":\"05371960\"}]","activityId":"2s7hhSTbhMgxpGoa9JDnbDzJTaBB","pageId":"","reqSrc":"","applyKey":"jd_star"}
    bodys = json.dumps(body)
    data = 'functionId=qryCompositeMaterials&body=%s&client=wh5&clientVersion=1.0.0&uuid=network/wifi' % bodys
    try:
        response = tujian(headers,'qryCompositeMaterials',data)
        if response.get('code') == '0':
            lists = response.get('data').get('resultData').get('list')
            for shop in lists:
                shopid = shop.get('extension').get('shopId')
                shopname = shop.get('name','')
                shop_task(headers,shopid)
                time.sleep(sleep_times)
        else:
            print(response.get('code'))
    except Exception as e:
        print(e)

for Cookie in Cookies:
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'jdapp;Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
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
    secretp = get_secretp(headers)
    sign(headers)
    i = 1
    while i < task_times:
        vxdata = 'functionId=zoo_getTaskDetail&body={"appSign":"2","channel":1,"shopSign":""}&client=wh5&clientVersion=1.0.0'
        jddata = 'functionId=zoo_getTaskDetail&body={}&client=wh5&clientVersion=1.0.0'
        print('开始微信任务')
        vxtask_list(headers,vxdata)
        print('开始京东任务')
        vxtask_list(headers,jddata)
        print('开始图鉴任务')
        tujian_share(headers)
        tujian_renwu(headers)
        print('等待5s后重新获取任务')
        time.sleep(5)
        i+=1

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))))
