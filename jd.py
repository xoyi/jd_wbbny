import urllib
import requests
import time
import json
import random
import re
from urllib import parse
import urllib3
urllib3.disable_warnings()

#活动地址
#https://wbbny.m.jd.com/babelDiy/Zeus/2s7hhSTbhMgxpGoa9JDnbDzJTaBB/index.html#/home

#欢迎使用jd脚本，有问题可以咨询作者QQ：1811881314

#循环任务次数，可以多跑几次没事
task_times = 3
#间隔时间，默认在任务所需的基础上加，一般设置2s左右就成，看自己
sleep_times = 2

Cookies = []
with open('ck.txt','r', encoding='utf-8') as ef:
    for i in ef:
        i = i.strip('\r\n')
        Cookies.append(i)
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
#获取任务列表
def task_list(headers):
    url = "https://api.m.jd.com/client.action?functionId=zoo_getTaskDetail"
    data = 'functionId=zoo_getTaskDetail&body={}&client=wh5&clientVersion=1.0.0'
    try:
        res = requests.post(url,headers=headers,data=data,verify=False).json()
        if res.get('code') == 0:
            datas = res.get('data').get('result').get('taskVos')
            lists = []
            for i in datas:
                taskId = i.get('taskId')
                status = i.get('status')
                taskTitle = i.get('taskName')
                if status == 1 and taskId != 2 and taskId != 14 and taskId != 16 and taskId != 17:
                    s = (taskId,taskTitle)
                    lists.append(s)
                if status == 3:
                    print(taskTitle + '任务已完成')
            return lists
        else:
            print(res.get('msg'))
    except:
        print('其他')

def get_taskVos(taskId,headers):
    url = 'https://api.m.jd.com/client.action?functionId=zoo_getTaskDetail'
    data = 'functionId=zoo_getTaskDetail&body={"taskId":%s}&client=wh5&clientVersion=1.0.0' % taskId
    try:
        res = requests.post(url,headers=headers,data=data,verify=False).json()
        if res.get('code') == 0:
            taskVos = res.get('data').get('result').get('taskVos')[0]
            return taskVos
        else:
            print(res.get('msg'))
    except:
        print('其他')
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

#逛店
def guangdian(taskId,taskToken,itemId,buttonid,headers):
    randomnum = random.randint(1000000,9999999)
    secretp = get_secretp(headers)
    url = 'https://api.m.jd.com/client.action?functionId=zoo_collectScore'
    body = {
        "taskId":taskId,
        "actionType":1,
        "taskToken":taskToken,
        "ss":"{\"extraData\":{\"log\":\"-1\",\"sceneid\":\"QD216hPageh5\"},\"secretp\":\"%s\",\"random\":\"%s\"}" % (secretp,randomnum),
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
        # print(productInfoVos)
        return productInfoVos
    except:
        print('其他')
# getFeedDetail()
#任务列表内容
def renwu(headers):
    lists = task_list(headers)
    for list1 in lists:
        taskId,taskTitle = list1
        print(taskId,taskTitle)
        taskVos = get_taskVos(taskId,headers)
        if taskId == 1 or taskId ==4 or taskId == 5 or taskId == 6 or taskId == 8 or taskId == 3:
            print('>>>>>开始进行%s任务' % taskTitle)
            buttonid = 'jmdd-react-smash_73'
            waitDuration=taskVos.get('waitDuration')
            shoppingActivityVos = taskVos.get('shoppingActivityVos')
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
        if taskId == 9:
            print('>>>>>开始进行%s任务' % taskTitle)
            waitDuration=taskVos.get('waitDuration')
            buttonid = 'jmdd-react-smash_73'
            browseShopVos = taskVos.get('browseShopVo')
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
            buttonid = 'jmdd-react-smash_73'
            browseShopVos = taskVos.get('browseShopVo')
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
        if taskId == 15 or taskId == 7:
            print('>>>>>开始进行%s任务' % taskTitle)
            buttonid = 'jmdd-react-smash_73'
            shoppingActivityVos = taskVos.get('shoppingActivityVos')
            for shop in shoppingActivityVos:
                shopstatus = shop.get('status')
                taskToken = shop.get('taskToken')
                shoptitle = shop.get('title')
                itemId = shop.get('itemId')
                if shopstatus == 1:
                    print('任务“%s”' % shoptitle)
                    guangdian(taskId,taskToken,itemId,buttonid,headers)
                    print('等待%s秒' % sleep_times)
                    time.sleep(sleep_times)
        if taskId == 10 or taskId == 13 or taskId == 11 or taskId == 12:
            print('>>>>>开始进行%s任务' % taskTitle)
            buttonid = 'jmdd-react-smash_73'
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
            
        else:
            pass
    print('任务已跑完，如发现还有任务未完成，可以修改times设置多次轮询跑')
for Cookie in Cookies:
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'jdapp;Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
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
    sign(headers)
    i = 1
    while i < task_times:
        renwu(headers)
        print('等待5s后重新获取任务')
        time.sleep(5)
        i+=1

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))))
