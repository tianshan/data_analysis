#! /usr/bin/env python
# -*- coding=utf-8 -*- 
#author: tianshan

import urllib2
import BeautifulSoup
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import csv
import codecs
import re

def getWebPage(url, i):
    url_i = url+'%s'%i
    request = urllib2.Request(url_i, headers={'User-Agent':'Magic Browser'})
    thePage = urllib2.urlopen(request)
    data = thePage.read()
    return data

def getContent(data):
    i = data.find('"')
    if i==-1:
        print 'data format error, left'
    data = data[i+1:]
    j = data.find('"')
    if j==-1:
        print 'data format error, left'
    return data[:j].decode('gbk')

def parseIndexData(data):
    values = []
    pattern = re.compile('records:([\\d]+)')
    mather = re.search(pattern, data)
    values += [int(mather.group(1))]
    pattern = re.compile('pages:([\\d]+)')
    mather = re.search(pattern, data)
    values += [int(mather.group(1))]
    return values


def parseData(data):
    soup = BeautifulSoup(data)
    trList = soup.tbody.findAll('tr')
    values = []
    for i in range(len(trList)):
        line = []
        tdList = trList[i].findAll('td')
        for j in range(5):
            if j==2:
                line += [tdList[j].next[:-1]]
            else:
                line += [tdList[j].next]
        values += [line]
    return values

def writeToCsv(fileName, values, isAdd):
    if isAdd:
        cFile = file(fileName, 'wb')
        cFile.write(codecs.BOM_UTF8)
        csvFile = csv.writer(cFile)
        title = ['净值日期','每万份收益','7日年化收益率','申购状态','赎回状态','分红配送']
        csvFile.writerow(title)
    else:
        cFile = file(fileName, 'ab')
        csvFile = csv.writer(cFile)
        csvFile.writerow(values)
    

if __name__=="__main__":
    perPage = 20
    code = 213009
    fileName = 'test.csv'

    url='http://fund.eastmoney.com/f10/F10DataApi.aspx?'+\
        'type=lsjz&code=%s&per=%s&rt=0.5903290933929384&page='%(code,perPage)
    data = getWebPage(url, 1)
    indexData = parseIndexData(data)
    writeToCsv(fileName, None, True)
    
    for i in range(1, indexData[1]+1):
        print 'page %s'%i
        data = getWebPage(url, i)
        data = getContent(data)
        values = parseData(data)
        writeToCsv(fileName, values, False)
