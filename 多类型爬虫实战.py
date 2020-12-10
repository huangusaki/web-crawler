#练习项目，上传到GiHub的自己用idle加了点备注啥的，可能会有什么错误（）

import requests
import re
import xlsxwriter
from selenium import webdriver
from urllib import request
from time import sleep

HEADERS={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

def dytt_spyder_cn():      #电影天堂国产电影资源爬虫，练习进度：初步学习了requests库使用和正则表达式，还有较多不够完善的地方
    information=[]
    url_temp=[]
    for i in range(1,int(input("需要爬取多少页："))):
            url="https://www.dytt8.net/html/gndy/china/list_4_"+str(i)+".html"
            rsp=requests.get(url,headers=HEADERS)
            url_temp.append(re.findall(re.compile(r'<a href="/(.*)" class="ulink"'),rsp.text))
    for list1 in url_temp:  #逐一解析爬取到的整个网页的子链接获取相关信息
        for item in list1:
            url="https://www.dytt8.net/"+item
            rsp=requests.get(url,headers=HEADERS)
            link=re.search(re.compile('magnet\S{54}|magnet\S{46}'),rsp.content.decode('gb2312','ignore'))[0]
            name=(re.search(re.compile('《(.*)》'),rsp.content.decode('gb2312','ignore'))).group()    #子网页的字体编码不是utf-8，直接用.text会使用到错误解码器解析不出中文
            try:
                score_numb=re.findall(re.compile('豆瓣评分.*from(.*)users'),rsp.content.decode('gb2312','ignore'))[0]
                score=re.findall(re.compile('豆瓣评分\u3000(.*)from'),rsp.content.decode('gb2312','ignore'))[0]
                score_info=str(score_numb)+"人进行评分"
            except:
                score_info="评分人数过少暂不统计"
                score="评分人数过少暂不统计"
            information.append([name,link,score_info,score])
    print("爬取完毕！\n程序1：国产电影爬虫")
    return information
            
def dytt_spyder_cn_save_data_byxlsx(info):
    movieInfo=xlsxwriter.Workbook('Moives Info.xlsx')
    sheet=movieInfo.add_worksheet('电影信息')
    detail=('电影名','磁力链接','豆瓣评分人数','评分')
    sheet.set_column("A:A",30).set_column("B:B",65).set_column("C:C",30).set_column("D:D",20)
    for i in range(0,4):
        sheet.write(0,i,detail[i])
    cow=0
    for item in info:
        cow+=1
        for i in range(0,4):
            sheet.write(cow,i,str(item[i]))
    movieInfo.close()
    
def Hatsune_club_spyder():          #练习进度：已完善至成品，进一步完善了正则提取的练习使用，以及尝试了爬取过程中会出现的意外情况
    url_temp1=[]
    Info=[]  
    url_choose={'1':'https://www.mikuclub.org/mofa/anime-3d/page/','2':'https://www.mikuclub.org/mofa/picture/page/','3':'https://www.mikuclub.org/mofa/video/page/','4':'https://www.mikuclub.org/mofa/acg-voice/page/','5':'https://www.mikuclub.org/mofa/dojinshi/page/','6':'https://www.mikuclub.org/mofa/h-fiction/page/'}
    type_of_spyder=input("1.3d动画\n2.cos图\n3.视频\n4.奥数魔刃\n5.漫画\n6.小说\n:选择想要爬取的资源类型的数字:")
    cookie={
         "cookie":input("输入初音社cookie：")
          }  
    for i in range(1,int(input("需要爬取多少页："))+1):
        url=url_choose[type_of_spyder]+str(i)
        rsp=requests.get(url,headers=HEADERS,cookies=cookie)
        url_temp1.append(re.findall(re.compile('href="(https://www.mikuclub.org/\d+)" title='),rsp.content.decode('utf-8'))[1::2])
    for item in url_temp1:
        print("正在爬取%s页"%(url_temp1.index(item)+1))
        for item2 in item:
            rsp=requests.get(item2,headers=HEADERS,cookies=cookie)
            title=re.findall(re.compile('<h4 class="article-title my-2">\n\t+(.*)</h4>'),rsp.content.decode('utf-8'))[0]
            try:
                link=re.findall(re.compile('(pan.baidu.com\S+)"'),rsp.content.decode('utf-8'))[0]
            except:
                try:
                    link="无网盘，蓝奏云："+re.findall(re.compile('(lanzous.com/\w+)'),rsp.content.decode('utf-8'))[0]+"。如需其他方式请自行前往目标网页"
                    link_password=" "
                except:
                    try:
                        link="无网盘，秒传："+re.findall(re.compile('all;">(.*)</div>'),rsp.content.decode('utf-8'))[0]+"。如需其他方式请自行前往目标网页"
                        link_password=" "
                    except:
                        link="无法找到下载链接，请自行前往网页查找："+item2
                        link_password=" "         
            try:
                unzip_password=re.findall(re.compile('password_unzip1".*value="(.*)" readonly'),rsp.content.decode('utf-8'))[0]
            except:
                unzip_password=" "
            try:
                link_password=re.findall(re.compile('password1".*value="(.*)" readonly'),rsp.content.decode('utf-8'))[0] 
            except:
                link_password=" "
            other_info_temp=re.findall(re.compile('class="count">(\d+)</span>'),rsp.content.decode('utf-8'))
            other_info="点赞数:"+other_info_temp[0]+"，收藏数："+other_info_temp[1]
            Info.append([title,link,link_password,unzip_password,other_info,item2])
    print("爬取完毕！\n程序2：初音社爬虫")
    return Info

def Hatsune_club_spyder_data_save(info):
    movieInfo=xlsxwriter.Workbook('初音社资源爬取.xlsx')
    sheet=movieInfo.add_worksheet('资源列表')
    detail=('资源名','下载链接','提取码','解压密码','资源信息','链接')
    sheet.set_column("A:B",72)
    sheet.set_column("C:C",8)
    sheet.set_column("D:F",25)
    for i in range(0,6):
        sheet.write(0,i,detail[i])
    cow=0
    for item in info:
        cow+=1
        for i in range(0,6):
            sheet.write(cow,i,str(item[i]))
    movieInfo.close()    

def comic_spyder():         #kuman网站爬虫，因为漫画资源不全和网站不稳定，放弃后续完善，已成功爬取过《勇者死了》作为练习成果，大致也可以用了，练习进度：初次使用了selenium模拟点击爬取以及大量文件储存下载
    url_temp="http://kuman55.com/search.php?key="+input("输入想要爬取的漫画名：")
    drive_path=r"C:\Users\usaki\Desktop\spyderfile\chromedriver.exe"
    drive=webdriver.Chrome(executable_path=drive_path)
    rsp=requests.get(url=url_temp,headers=HEADERS)      #获得指定漫画的详情地址
    comic_list=[]   #漫画子列表url（第几话）储存位置
    numb=re.findall(re.compile('href="/(\d+)/"'),rsp.text)[0] #漫画序号提取
    drive.get("http://kuman55.com/"+numb+"/")
    try:
        drive.find_element_by_id("all_mores1").click()
    except:
        pass
    sleep(3)
    comic_id=re.findall(re.compile('/\d+.html'),drive.page_source)  #提取漫画子集序号
    for i in range(0,len(comic_id)):
        comic_list.append(("http://kuman55.com/"+numb+comic_id[i]))
    comic_list.reverse() #完整的将漫画链接正序储存
    check=[]    #检查有无将页面翻到页底
    link=[]     #图片链接，下载图片时用到
    num=0       #文件名z
    for i in range(0,len(comic_list)):  #开始爬取图片链接
        drive.get(comic_list[i])    #获取目标网页的代码
        check=[]                #重置检查是否结束的状态
        while len(check)==0:        #检查是否翻到页底
            drive.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            check=re.findall(re.compile('.*已经结束.*'),drive.page_source)
        link.append(re.findall(re.compile('(http://dingyue\S+jpg)'),drive.page_source))
        sleep(1)
    for item in link:       #开始下载图片到指定位置
        for item2 in item:
            with open(("C:/Users/usaki/Desktop/spyderfile/img/"+str(num)+".jpg"), 'wb') as f:
                num+=1
                f.write((requests.get(item2)).content)
    drive.quit()
    
if __name__ == "__main__":
    
     #information=dytt_spyder_cn()           #国产电影资源爬虫
     #dytt_spyder_cn_save_data_byxlsx(information) #保存爬取到的电影数据
     #infomation2=Hatsune_club_spyder()      #施法材料爬虫，需要cookie
     #Hatsune_club_spyder_data_save(infomation2) #保存施法材料数据
     #comic_spyder()
     # test()
     # comic_spyder()
