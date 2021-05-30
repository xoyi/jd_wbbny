# -*- coding: utf-8 -*-
# Written by xizhi

import sys
import time
try:
  import requests
except (ImportError,ModuleNotFoundError):
  print("请先安装 requests 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  import rsa
except (ImportError,ModuleNotFoundError):
  print("请先安装 rsa 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  import qrcode
except (ImportError,ModuleNotFoundError):
  print("请先安装 qrcode 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  from PIL import Image
except (ImportError,ModuleNotFoundError):
  print("请先安装 Pillow 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
import os
import re
import base64
import urllib
import random
import uuid
import ast
import psutil

def GetCookiesExit1():
  print("程序5秒后自动退出")
  time.sleep(5)
  sys.exit()

def kill_process():
  for proc in psutil.process_iter():
    try:
      s = proc.name()
      if s == 'photolaunch.exe':
        proc.kill()
      elif s:
        pass
      else:
        proc.kill()
    except:
      proc.kill()

class JDMobCookies():
  def JDMobLogin(self):
    jdheaders = {"User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
                 "Referer": "https://plogin.m.jd.com/login/login?appid=300"}
    jdgetstoken = requests.get("https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300",headers=jdheaders,timeout=5)
    stoken = jdgetstoken.json()["s_token"]
    jdsetcookiesd = requests.utils.dict_from_cookiejar(jdgetstoken.cookies)
    jdsetcookiesl = []
    for jdsetcookie in jdsetcookiesd:
        jdsetcookiesl.append(jdsetcookie+"="+jdsetcookiesd.get(jdsetcookie))
    jdsetcookies = ";".join(jdsetcookiesl)
    jdheaders["Cookie"] = jdsetcookies
    jdgettoken = requests.get("https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?lang=chs&appid=300&s_token=%s&remember=true"%(stoken),headers=jdheaders,timeout=5)
    token = jdgettoken.json()["token"]
    jdsetcookiesd = requests.utils.dict_from_cookiejar(jdgettoken.cookies)
    okltoken = jdsetcookiesd.get("okl_token")
    qrcodeb = qrcode.make("https://plogin.m.jd.com/cgi-bin/m/tmauth?appid=300&client_type=m&token=%s"%(token))
    qrcodeb.save("JDMobQRcode.png")
    print("\n二维码图片 JDMobQRcode.png 已生成到该目录下,请后台运行程序,电脑打开图片后用京东APP扫码登录")
    if sys.platform == "win32":
      im = Image.open('JDMobQRcode.png')
      im.show()
    elif sys.platform == "darwin":
        os.system('open "JDMobQRcode.png"')
    else:
        os.system('xdg-open "JDMobQRcode.png"')

    while True:
        jdcheckqrp = requests.get("https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?lang=chs&appid=300&returnurl=&token=%s&ou_state=0&okl_token=%s"%(token,okltoken),
                                headers=jdheaders,timeout=5)
        jdcheckqrj = jdcheckqrp.json()
        if jdcheckqrj["errcode"] == 176:
            print(jdcheckqrj["message"])
        elif jdcheckqrj["errcode"] == 0:
            print("\n登录成功,可以关闭京东APP了...\n")
            kill_process()
            os.remove('JDMobQRcode.png')
            return jdcheckqrp
        elif jdcheckqrj["errcode"] == 21:
            print("返回信息: %s\n是否重新获取二维码,手机端操作需要先完全关闭京东APP哦"%(jdcheckqrj["message"]))
            jdqrcask = input("是 直接按确定继续,否 输入 n 然后按确定退出:")
            if jdqrcask.lower() == "n":
                GetCookiesExit1()
            else:
                return self.JDMobLogin()
        else:
          print("返回信息: %s\n未遇到过的错误"%(jdcheckqrj["message"]))
        time.sleep(3)

  def JDMobLogined(self):
    jdcheckqrp = self.JDMobLogin()
    jdcookiesd = requests.utils.dict_from_cookiejar(jdcheckqrp.cookies)
    jdcookiesl = []
    for jdcookie in jdcookiesd:
        jdcookiesl.append(jdcookie+"="+jdcookiesd.get(jdcookie))
    jdstrcookies = ";".join(jdcookiesl)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .txt 文件(一般的打开文本类程序即可查看修改),获取成功后自动退出程序\n%s"\
          %(jdcookiesd["pt_pin"],jdstrcookies))
    with open("ck.txt", "a") as jdcookies:
        jdcookies.write(jdstrcookies + '\n')
    sys.exit()
JDMobCookies().JDMobLogined()
