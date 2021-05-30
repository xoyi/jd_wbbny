#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import json
import urllib3
import _thread
import re
import hashlib
import execjs




urllib3.disable_warnings()
session = requests.Session()
Cookies = []
with open('ck.txt','r', encoding='utf-8') as ef:
    for i in ef:
        i = i.strip('\r\n')
        Cookies.append(i)
## 星推官
##
class Jd_xtg(object):
    def __init__(self, key):
        self.session = requests.Session()
        self.cookie = key
        self.tuan = {}
        self.starId = ''
        self.js ='''
            function getBody(t, e, a) {
                var n = "",
                    i = a.split("?")[1] || "";
                if (t) {
                    if ("string" == typeof t) n = t + i;
                    else if ("object" == ka(t)) {
                    var s = [];
                    for (var r in t) s.push(r + "=" + t[r]);
                    n = s.length ? s.join("&") + i : i;
                    }
                } else n = i;
                if (n) {
                    var o = n.split("&").sort().join("");
                    return o + e
                }
                return e;
                }

        '''

    def runPost(self,method,key1,key2):
        strtime = str(round(time.time()*1000))
        o = "07035cabb557f096" + strtime
        s1 = execjs.compile(self.js).call('getBody',key2,o,key1)
        str_md5 = hashlib.md5(s1.encode(encoding='utf-8')).hexdigest()

        url = 'https://guardianstarjd.m.jd.com/star/'+method
               
        headers = {
            'Host': 'guardianstarjd.m.jd.com',
            'User-Agent': 'jdapp;Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
            'Accept': 'application/json,text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection':'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://bunearth.m.jd.com',
            'Referer': 'https://guardianstarjd.m.jd.com/',
            'Cookie':self.cookie,
            'timestamp':strtime,
            'sign':str_md5
        }
        data = key2
        response = self.session.post(url,data=data,headers=headers,verify=False).json()
        return response

    def starRanking(self):
        strtime = str(round(time.time()*1000))
        print(strtime)
        o = "07035cabb557f096" + strtime
        a = 'starId=bl-gongjun'
        t = 'starRanking'
        s1 = a+o
        str_md5 = hashlib.md5(s1.encode(encoding='utf-8')).hexdigest()
        url = 'https://guardianstarjd.m.jd.com/star/task/starRanking'
               
        headers = {
            'Host': 'guardianstarjd.m.jd.com',
            'User-Agent': 'jdapp;Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
            'Accept': 'application/json,text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection':'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://bunearth.m.jd.com',
            'Referer': 'https://guardianstarjd.m.jd.com/',
            'Cookie':self.cookie,
            'timestamp':strtime,
            'sign':str_md5
        }
        data = 'starId=bl-gongjun'

        response = self.session.post(url,data=data,headers=headers,verify=False).json()
        self.stars = response.get('data','')
        print("获取成功")

    def dotask(self):
        for i in self.stars:
            starId = i['starId']
            self.starId = starId
            print('开始星推官:'+starId)
            dayTask = self.getHomePage(starId).get('dayTask','')
            for i in dayTask:
                if i['type']=='sku' and i['finishCount']!=i['count']:
                    print('浏览'+i['name']+'等待6秒...')
                    self.runTask(i['type'],i['id'])
                elif i['type']=='meeting' and i['finishCount']!=i['count']:
                    print('浏览会场'+i['name']+'等待6秒...')
                    self.runTask(i['type'],i['id'])
                elif i['type']=='followShop' and i['finishCount']!=i['count']:
                    print('关注店铺'+i['name']+'...')
                    self.runTask2(i['type'],i['id'])
    
    def runTask(self,types,id):
        reponse = self.runPost('task/doBrowse','doBrowse','starId='+self.starId+'&id='+id+'&type='+types)
        time.sleep(6)
        resp2 = self.runPost('task/getBrowsePrize','getBrowsePrize','starId='+self.starId+'&browseId='+reponse.get('data',''))
        print('获得守护星%s个，京豆%s个' % (resp2.get('data','')['integral'],resp2.get('data','')['jingBean']))

        # break

    def runTask2(self,types,id):
        reponse = self.runPost('task/followShop','followShop','starId='+self.starId+'&id='+id+'&type='+types)
        if reponse.get('code') == 200:
            integral = reponse.get('data').get('integral')
            jingBean = reponse.get('data').get('jingBean')
            print('获得守护星%s个，京豆%s个' % (integral,jingBean))
        else:
            print(reponse.get('msg'))
        time.sleep(2)

    def getHomePage(self,starId):
        strtime = str(round(time.time()*1000))
        print(strtime)
        o = "07035cabb557f096" + strtime
        a = 'starId='+starId
        # t = 'starRanking'
        s1 = a+o
        str_md5 = hashlib.md5(s1.encode(encoding='utf-8')).hexdigest()
        # print(str_md5)

        url = 'https://guardianstarjd.m.jd.com/star/task/getList'
               
        headers = {
            'Host': 'guardianstarjd.m.jd.com',
            'User-Agent': 'jdapp;Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
            'Accept': 'application/json,text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection':'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://bunearth.m.jd.com',
            'Referer': 'https://guardianstarjd.m.jd.com/',
            'Cookie':self.cookie,
            'timestamp':strtime,
            'sign':str_md5
        }
        data = a

        response = self.session.post(url,data=data,headers=headers,verify=False).json()
        return response.get('data','')


    
if __name__ == '__main__':
    for cookie in Cookies:
    #填写自己cookie
        plus = Jd_xtg(cookie)
        plus.starRanking()
        plus.dotask()

    print('星推官任务已做完...')
