import re
import os
from bs4 import BeautifulSoup
import urllib
import xlwt
import sqlite3
import urllib.request
import urllib.error
import time
import xlsxwriter
from urllib import request
import random

def main():
    try:
        os.mkdir("icon")
    except:
        print("已存在文件夹icon")
    url="https://www.taptap.com/app/"
    data=getdata(url)
    savedata(data)
    dbpath="taptap.db"
    savedatadb(dbpath,data)


def checkarr(arr):
    if len(arr)==0:
        item=0
    else:
        item=arr[0]
    return item

    
def getdata(url): 
    data=[]
    t0=0
    t1=0
    findicon=re.compile(r'src="(.*)?imageMogr2')
    findname=re.compile(r'title="(.*)"/>')
    finddownloads=re.compile(r'<span class="count-stats">(.*?) 人安装')    
    findfollowers=re.compile(r'.*<span class="count-stats">(.*) 人关注')
    findscore=re.compile(r'<span class="app-rating-score" itemprop="ratingValue">(.*)</span>')
    for i in range(2000,4000):
        url2=url+str(i)
        html=geturl(url2)
        t0=t0+1
        if (t0==5):
            time.sleep(random.uniform(1,2))
            t0=0
        t1=t1+1
        if (t1==100)
            time.sleep(8)
            t1=0
        analysis=BeautifulSoup(html,"html.parser")
        results=analysis.find_all(class_="nav-sidebar-main")
        for item in results:
            item=str(item)
            datalist=[]
            icon=re.findall(findicon,item)[0]
            name=checkarr(re.findall(findname,item))
            downloads=checkarr(re.findall(finddownloads,item))
            followers=checkarr(re.findall(findfollowers,item))
            score=checkarr(re.findall(findscore,item))
            datalist.append(name)
            datalist.append(downloads)
            datalist.append(followers)
            datalist.append(score)
            datalist.append(0)
            iconname=name+'.png'
            iconname=iconname.replace('/','  ')
            iconname=iconname.replace('?','  ')
            iconname=iconname.replace('？','  ')
            iconpath='icon/'+iconname
            datalist.append(iconpath)
            data.append(datalist)             
            request.urlretrieve(icon,iconpath)
    for i in range(0,len(data)):
        data[i][4]=0.1*int(data[i][2])+800000*float(data[i][3])
    return data

def savedata(data):
    workbook=xlsxwriter.Workbook('data.xlsx')
    datasheet=workbook.add_worksheet("游戏信息")
    datasheet.set_default_row(40)
    datasheet.set_column("A:A",30)
    lbinfo=("游戏名","安装数","关注数","评分","指数")
    for i in range(0,5):
        datasheet.write(0,i,lbinfo[i])
    for i in range(0,len(data)):
        datalist=data[i]
        datasheet.insert_image(i+1,0, data[i][5],{'x_scale': 0.1, 'y_scale': 0.1})
        for j in range(0,5):
            datasheet.write(i+1,j,datalist[j])
    workbook.close()
    pass


def geturl(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        }
    requesturl=urllib.request.Request(url,headers=headers)
    html=""
    try:
        data=urllib.request.urlopen(requesturl)
        html=data.read()
    except urllib.error.HTTPError:
        print("游戏已下架");
    time.sleep(random.uniform(0.5,1))
    return html


def savedatadb(dbpath,data):
    try:
        sqlint(dbpath)
    except:
        print("数据库文件已存在")       
    database=sqlite3.connect(dbpath)
    dboperate=database.cursor()
    for i in range(0,len(data)):
        sql=' insert or ignore into taptap values(?,?,?,?,?,?) '
        item = tuple(data[i])
        dboperate.execute(sql,item)
    database.commit()
    database.close()

    
def sqlint(path):
    database=sqlite3.connect(path)
    dboperate=database.cursor()
    sql=''' create table taptap
            (游戏名 text primary key not null,
             安装数 numeric,
             关注数 numeric,
             评分 numeric,
             指数 numeric,
             图标地址 varchar(255));    '''
    dboperate.execute(sql)
    database.commit()
    database.close()

if 1:
    main()  
