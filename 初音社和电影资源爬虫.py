#练习项目

import requests
import re
import xlsxwriter

HEARDES={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

def dytt_spyder_cn():      #电影天堂国产电影资源爬虫
    print("正在使用电影资源爬虫")    
    information=[]
    url_temp=[]
    for i in range(1,int(input("需要爬取多少页："))):
            url="https://www.dytt8.net/html/gndy/china/list_4_"+str(i)+".html"
            rsp=requests.get(url,headers=HEARDES)
            url_temp.append(re.findall(re.compile(r'<a href="/(.*)" class="ulink"'),rsp.text))
    for list1 in url_temp:  #逐一解析爬取到的整个网页的子链接获取相关信息       
        for item in list1:
            print("正在爬取%s页"%(url_temp.index(list1)))
            url="https://www.dytt8.net/"+item
            rsp=requests.get(url,headers=HEARDES)
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
    
def Hatsune_club_spyder():
    print("正在使用初音社爬虫")
    url_temp1=[]
    Info=[]  
    cookie={
         "cookie":input("请输入初音社cookie")        
         }  
    for i in range(1,int(input("需要爬取多少页："))):
        url="https://www.mikuclub.org/mofa/dojinshi/page/"+str(i)
        rsp=requests.get(url,headers=HEARDES,cookies=cookie)
        url_temp1.append(re.findall(re.compile('href="(https://www.mikuclub.org/\d+)" title='),rsp.content.decode('utf-8'))[1::2])
    for item in url_temp1:
        print("正在爬取%s页"%(url_temp1.index(item)))
        for item2 in item:
            rsp=requests.get(item2,headers=HEARDES,cookies=cookie)
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

if __name__ == "__main__":
    
     #information=dytt_spyder_cn()           #国产电影资源爬虫，网站有时会崩，不稳定，暂时关了
     #dytt_spyder_cn_save_data_byxlsx(information) #保存爬取到的电影数据
     infomation2=Hatsune_club_spyder()      #施法材料爬虫，需要cookie
     Hatsune_club_spyder_data_save(infomation2) #保存施法材料数据
      

