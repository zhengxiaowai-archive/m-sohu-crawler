#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Usage:
    main.py -d <sec> -u <url> -o <output>
Options:
    -d     time(seconds)
    -u     the url for web
    -o     output dir
'''

import requests

from docopt import docopt
from time import strftime
import logging
import os
import re

#获取当前时间，格式为：年月日时分
nowDate =lambda: strftime('%Y%m%d%H%M') 


class SavePage(object):
    def __init__(self, interval, url, output):
        self.log = Log()
        self.interval = interval
        self.log.infoMsg('interval: {interval}'.format(interval = self.interval))
        self.url = url
        self.log.infoMsg('url: {url}'.format(url = self.url))
        self.output = output
        self.log.infoMsg('output: {output}'.format(output = self.output))
    
    def _mkdir(self):
        dirName = nowDate()
        self.dirPath = os.path.join(self.output, dirName)
        self.dirCssPath =  os.path.join(self.dirPath, 'css')
        self.dirJsPath =  os.path.join(self.dirPath, 'js')
        self.dirImgPath = os.path.join(self.dirPath, 'images')
        if not os.path.exists(self.dirPath):
            os.mkdir(self.dirPath)
            os.mkdir(self.dirCssPath)
            os.mkdir(self.dirJsPath)
            os.mkdir(self.dirImgPath)
    
    def _save(self, url, path):
        ret = requests.get(url)
        FileFullPath = os.path.join(path, os.path.basename(url))
        with open(FileFullPath, 'wb') as f:
            f.write(ret.content)
        
    
    def getHtmlSourceCode(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'Cache-Control':'max-age=0',
                   'Connection':'keep-alive',
                   'Host':'m.sohu.com',
                   'If-None-Match':'"a1a6eb0c70895e20336a6c48b65dd009703c9ba6"',
                   'Upgrade-Insecure-Requests':'1',
                   'Cookie':'vjuids=-ea7a06d5.15041c7d5be.0.4fc15ef5; IPLOC=CN2300; SUV=1510072039220698; ppinf=2|1444300951|1445510551|bG9naW5pZDowOnx1c2VyaWQ6NDQ6RDhBRjZFMUVCNzE0QjM4OUVEMjgyRDMyN0NFQ0IwNkFAcXEuc29odS5jb218c2VydmljZXVzZTozMDowMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB8Y3J0OjA6fGVtdDoxOjB8YXBwaWQ6NDoxMDc0fHRydXN0OjE6MXxwYXJ0bmVyaWQ6MTowfHJlbGF0aW9uOjA6fHV1aWQ6MTY6NzgxOTI2ZDQ2NDE1NDA0eHx1aWQ6MTY6NzgxOTI2ZDQ2NDE1NDA0eHx1bmlxbmFtZToyODp6JUU2JUFEJUEzJUU1JUIwJThGJUU2JUFEJUFBfHJlZnVzZXJpZDozMjpEOEFGNkUxRUI3MTRCMzg5RUQyODJEMzI3Q0VDQjA2QXxyZWZuaWNrOjQ6euato-Wwj-atqnw; pprdig=qQszFsZYZWPjFf-ocfvG8DYAoiJVm4BUElFodgfkeWtXw-SpxDeHLyU3gFSIonOLsm1epsMQ0fuSlh6qx8ANeQ8efSBAasOSaokwIOuUHBvdKydSzNRGC--vrjI0uq_ATFJLlc3P4YxFcRtAoJ8wZdynfgYhPc7JTussyWHHpUI; vjlast=1444212627.1444564211.11; _smuid=1FQx1G2kc7AWijDhdJ9acM; nickname=; ip_city=%E5%93%88%E5%B0%94%E6%BB%A8; _xsrf=22094c749a304558bd370f0fc76ed372; indexSelect=1; sid=Uo5O4wiyfebdwFdDZ3yKo; adaptor_version=3; position=8; page_version=3; home_infoflow_ad_turn=126; indexWin=1; home_banner_ad_turn=127; hide_ad=0'}
        ret = requests.get(self.url, headers = headers)
        self._mkdir()
        if ret.status_code != 200:
            self.log.errorMsg('status_code: {code}'.format(code = ret.status_code)) 
            return False
        else:
            sourceCode = ret.content
            indexHtml = os.path.join(self.dirPath, 'index.html')
            with open(indexHtml, 'w') as f:
                f.write(sourceCode) 
            return sourceCode
    
    def imgOriginal(self, htmlSouceCode):
        original = re.compile(r'''<img src=.*? original="(.*?)".*?/>''')
        imgUrls = original.findall(htmlSouceCode,re.S)
        for url in imgUrls:
            self._save(url, self.dirImgPath)
    
    def imgAlt(self, htmlSouceCode):
        alt = re.compile(r'''<img src="(.*?)" alt=".*?".*?>''')
        imgUrls = alt.findall(htmlSouceCode,re.S)
        for url in imgUrls:
            self._save(url, self.dirImgPath)
    
    def imgLoading(self, htmlSouceCode):
        url = 'http://s1.rr.itc.cn/p/images/imgloading.jpg'
        self._save(url, self.dirImgPath)
    
    def imgLeftRight(self, htmlSouceCode):
        urlLeft = 'http://s8.rr.itc.cn/org/wapChange/20156_2_15/b84mvp4105546836266.png'
        self._save(urlLeft, self.dirImgPath)
        
        urlRight = 'http://s9.rr.itc.cn/org/wapChange/20156_2_15/a81j1i5977584219487.png'
        self._save(urlRight, self.dirImgPath)
    
    
    def saveJs(self, htmlSouceCode):
        pattern = re.compile(r'''<script type="text/javascript" src="(.*?)"></script>''')
        jsUrls = pattern.findall(htmlSouceCode,re.S)
        for url in jsUrls:
            self._save(url, self.dirJsPath)
    
    def saveCss(self, htmlSouceCode):
        pattern = re.compile(r'''<link rel="stylesheet" type="text/css" href="(.*?)" media="all">''')
        cssUrls = pattern.findall(htmlSouceCode,re.S)
        for url in cssUrls:
            self._save(url, self.dirCssPath)
    
    def saveImg(self, htmlSouceCode):
        #标签中original的图片
        self.imgOriginal(htmlSouceCode)
         
        #标签中有alt的图片
        self.imgAlt(htmlSouceCode)

        #loading图片
        self.imgLoading(htmlSouceCode)
        
        #左右箭头图片
        self.imgLeftRight(htmlSouceCode)
    
    def start(self):
        pass

class Log(object):
    def __init__(self, logFilePath = './log'):
        logging.basicConfig(level = logging.INFO,
                            format = '%(asctime)s %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=logFilePath,
                            filemode='a')
        
    def  warningMsg(self, msg):
        logging.warning(msg)
    
    def  errorMsg(self, msg):
        logging.error(msg)
        
    def criticalMsg(self, msg):
        logging.critical(msg)
    
    def infoMsg(self, msg):
        logging.info(msg)

if __name__ == '__main__':
    s = SavePage(60, 'http://m.sohu.com/', './')
    html = s.getHtmlSourceCode()
#     s.saveJs(html)
#     s.saveCss(html)
    s.saveImg(html)
    print 'OK'
    
    
    
    
    
    
    
    
    
    