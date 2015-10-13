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
        import os
        dirName = nowDate()
        dirPath = os.path.join(self.output, dirName)
        dirCssPath =  os.path.join(dirPath, 'css')
        dirJsPath =  os.path.join(dirPath, 'js')
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
            os.mkdir(dirCssPath)
            os.mkdir(dirJsPath)
        return dirPath, dirCssPath, dirJsPath
        
    
    def getHtmlSourceCode(self):
        import os
        ret = requests.get(self.url)
        dirPath, dirCssPath, dirJsPath = self._mkdir()
        if ret.status_code != 200:
            self.log.errorMsg('status_code: {code}'.format(code = ret.status_code)) 
            return False
        else:
            sourceCode = ret.content
            indexHtml = os.path.join(dirPath, 'index.html')
            with open(indexHtml, 'w') as f:
                f.write(sourceCode) 
            return sourceCode
    
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
    s = SavePage(60, 'http://m.sohu.com/', '/tmp/backup/')
    print s.getHtmlSourceCode()
    
    
    
    
    
    
    
    
    
    