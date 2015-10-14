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
        
    
    def getHtmlSourceCode(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
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
    
    def saveJs(self, htmlSouceCode):
        import re
        pattern = re.compile(r'''<script type="text/javascript" src="(.*?)"></script>''')
        jsUrls = pattern.findall(htmlSouceCode,re.S)
        for url in jsUrls:
            ret = requests.get(url)
            jsFileFullPath = os.path.join(self.dirJsPath, os.path.basename(url))
            with open(jsFileFullPath, 'w') as f:
                f.write(ret.content)
    
    def saveCss(self, htmlSouceCode):
        import re
        pattern = re.compile(r'''<link rel="stylesheet" type="text/css" href="(.*?)" media="all">''')
        cssUrls = pattern.findall(htmlSouceCode,re.S)
        for url in cssUrls:
            ret = requests.get(url)
            jsFileFullPath = os.path.join(self.dirCssPath, os.path.basename(url))
            with open(jsFileFullPath, 'w') as f:
                f.write(ret.content)
    
    def saveImg(self, htmlSouceCode):
        import re
        pattern = re.compile(r'''<img src=.*? original="(.*?)".*?/>''')
        imgUrls = pattern.findall(htmlSouceCode,re.S)
        print imgUrls
        for url in imgUrls:
            print url
            ret = requests.get(url)
            jsFileFullPath = os.path.join(self.dirImgPath, os.path.basename(url))
            with open(jsFileFullPath, 'wb') as f:
                f.write(ret.content)
        

    
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
    s.saveJs(html)
    s.saveCss(html)
    s.saveImg(html)
    
    
    
    
    
    
    
    
    
    