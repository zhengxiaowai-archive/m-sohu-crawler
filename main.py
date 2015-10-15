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

import os
import re
import sys
import time
import logging
import requests

from docopt import docopt
from time import strftime


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
        
        if not os.path.exists(self.output):
            os.mkdir(self.output)
    
    def _mkdir(self):
        #创建js、css、images文件夹
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
        #从url中下载
        ret = requests.get(url)
        FileFullPath = os.path.join(path, os.path.basename(url))
        with open(FileFullPath, 'wb') as f:
            f.write(ret.content)
    
    def _ajax(self, ajaxUrl):
        #获取ajax的返回的json
        #http://m.sohu.com/api/house/
        ret = requests.get(ajaxUrl)
        self.response = ret.json()
    
    def _fixAjaxHtml(self, htmlSouceCode):
        #由于网页的部分是用ajax加载的，源码中并没有这部分，需要手动修复这部分
        fomatHtml = '''      
          <section class="cnl" id="jiaodian"> 
           <h3 class="h ht1"> 
            <aside class="rightTip"> 
             <p class="siteTip btns"><a href="javascript:;" class="btn btn2"><i class="home_i i01"></i><b>GPS定位</b></a></p> 
            </aside> <em><a href="http://m.sohu.com/f/jiaodian2/?_once_=000025_xiaodaohang_jiaodian_1v3">房产</a></em> </h3> 
           <div class="it"> 
            <section class="pl pl_c2"> 
             <a href="http://m.focus.cn/hrb/zixun/10454542?channelId=363" class="h4"> <i class="img"><img src="{picUrl1}" original="{picUrl1}" width="146" height="124" data-lazy-load-completed="1" style="opacity: 1;" /></i> <p>{picDesc1}</p> </a> 
             <a href="http://m.focus.cn/hrb/zixun/10454573?channelId=363" class="h4"> <i class="img"><img src="{picUrl2}" original="{picUrl2}" width="146" height="124" data-lazy-load-completed="1" style="opacity: 1;" /></i> <p>{picDesc2}</p> </a> 
            </section> 
           </div> 
           <section class="ls"> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl0}" class="h4">{dataInfoTitle0}</a>
             </div>
            </div> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl1}" class="h4">{dataInfoTitle1}</a>
             </div>
            </div> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl2}" class="h4">{dataInfoTitle2}</a>
             </div>
            </div> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl3}" class="h4">{dataInfoTitle3}</a>
             </div>
            </div> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl4}" class="h4">{dataInfoTitle4}</a>
             </div>
            </div> 
            <div class="it">
             <div class="h4WP">
              <a href="{dataInfoUrl5}" class="h4">{dataInfoTitle5}</a>
             </div>
            </div> 
           </section> 
           <div class="btns cnlPopBtn"> 
            <div class="cnlPopBtnWrap"> 
             <a href="http://m.sohu.com/f/jiaodian3/?_once_=000088_jiaodian" class="btn"><b>进入房产频道</b></a> 
            </div> 
           </div>
          </section>
        '''.format(picUrl1          = self.response['data']['data']['picUrl1'],
                   picDesc1         = self.response['data']['data']['picDesc1'],
                   picUrl2          = self.response['data']['data']['picUrl2'],
                   picDesc2         = self.response['data']['data']['picDesc2'],
                   dataInfoUrl0     = self.response['data']['data']['dataInfo'][0]['url'],
                   dataInfoTitle0   = self.response['data']['data']['dataInfo'][0]['title'],
                   dataInfoUrl1     = self.response['data']['data']['dataInfo'][1]['url'],
                   dataInfoTitle1   = self.response['data']['data']['dataInfo'][1]['title'],
                   dataInfoUrl2     = self.response['data']['data']['dataInfo'][2]['url'],
                   dataInfoTitle2   = self.response['data']['data']['dataInfo'][2]['title'],
                   dataInfoUrl3     = self.response['data']['data']['dataInfo'][3]['url'],
                   dataInfoTitle3   = self.response['data']['data']['dataInfo'][3]['title'],
                   dataInfoUrl4     = self.response['data']['data']['dataInfo'][4]['url'],
                   dataInfoTitle4   = self.response['data']['data']['dataInfo'][4]['title'],
                   dataInfoUrl5     = self.response['data']['data']['dataInfo'][5]['url'],
                   dataInfoTitle5   = self.response['data']['data']['dataInfo'][5]['title'],
                    )
        return htmlSouceCode.replace('<section class="cnl" id="jiaodian"></section>', fomatHtml)
        
    def getHtmlSourceCode(self):
        #获取网页源代码，写入index.heml
        self._ajax('http://m.sohu.com/api/house/')
        #站点有反爬虫机制，需要重新设置头部
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
                f.write(self._fixAjaxHtml(sourceCode)) 
            return sourceCode
    
    def imgOriginal(self, htmlSouceCode):
        #保存Original的图片
        original = re.compile(r'''<img src=.*? original="(.*?)".*?/>''')
        imgUrls = original.findall(htmlSouceCode,re.S)
        for url in imgUrls:
            self._save(url, self.dirImgPath)
    
    def imgAlt(self, htmlSouceCode):
        #alt
        alt = re.compile(r'''<img src="(.*?)" alt=".*?".*?>''')
        imgUrls = alt.findall(htmlSouceCode,re.S)
        for url in imgUrls:
            self._save(url, self.dirImgPath)
    
    def imgLoading(self):
        #所有的loading图片都是同一张
        url = 'http://s1.rr.itc.cn/p/images/imgloading.jpg'
        self._save(url, self.dirImgPath)
    
    def imgLeftRight(self):
        #保存左右箭头的图片，同样都是一样的
        urlLeft = 'http://s8.rr.itc.cn/org/wapChange/20156_2_15/b84mvp4105546836266.png'
        self._save(urlLeft, self.dirImgPath)
        
        urlRight = 'http://s9.rr.itc.cn/org/wapChange/20156_2_15/a81j1i5977584219487.png'
        self._save(urlRight, self.dirImgPath)
    
    def imgAjax(self):
        #保存有ajax加载的图片，只有两张
        self._save(self.response['data']['data']['picUrl1'], self.dirImgPath)
        self._save(self.response['data']['data']['picUrl2'], self.dirImgPath)
        
    def saveJs(self, htmlSouceCode):
        #保存js
        pattern = re.compile(r'''<script type="text/javascript" src="(.*?)"></script>''')
        jsUrls = pattern.findall(htmlSouceCode,re.S)
        for url in jsUrls:
            self._save(url, self.dirJsPath)
        self.log.infoMsg("save js successfully")
    
    def saveCss(self, htmlSouceCode):
        #保存css
        pattern = re.compile(r'''<link rel="stylesheet" type="text/css" href="(.*?)" media="all">''')
        cssUrls = pattern.findall(htmlSouceCode,re.S)
        for url in cssUrls:
            self._save(url, self.dirCssPath)
        self.log.infoMsg("save css successfully")
    
    def saveImg(self, htmlSouceCode):
        #标签中original的图片
        self.imgOriginal(htmlSouceCode)
         
        #标签中有alt的图片
        self.imgAlt(htmlSouceCode)

        #loading图片
        self.imgLoading()
        
        #左右箭头图片
        self.imgLeftRight()
        
        #ajax中的图片
        self.imgAjax()
        
        self.log.infoMsg("save img successfully")
    
    def start(self):
        while True:
            try:
                html = self.getHtmlSourceCode()
                self.saveJs(html)
                self.saveCss(html)
                self.saveImg(html)
            except Exception, e:
                self.log.criticalMsg(str(e))
            
            #睡眠
            time.sleep(int(self.interval))

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
    reload(sys)
    sys.setdefaultencoding('utf-8')
    arguments = docopt(__doc__, version = "0.1.0")
    if arguments['-d'] and arguments['-u'] and arguments['-o']:
        interval = arguments['<sec>']
        url = arguments['<url>']
        output = arguments['<output>']
        s = SavePage(interval, url, output)
        s.start()
        
    
    
    
    
    
    
    
    
    
