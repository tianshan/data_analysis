#! /usr/bin/env python
# -*- coding=utf-8 -*- 
#author: tianshan

import urllib2

def getWebPage(url, i):
    url_i = url+'%s'%i
    request = urllib2.Request(url_i, headers={'User-Agent':'Magic Browser'})
    thePage = urllib2.urlopen(request)
    data = thePage.read()
    return data

if __name__=="__main__":
    url='http://fund.eastmoney.com/f10/F10DataApi.aspx?'+\
        'type=lsjz&code=213009&per=20&rt=0.5903290933929384&page='
    print getWebPage(url, 1)


