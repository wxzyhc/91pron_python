# coding=utf-8
import requests
import os
import re
import time
import random
import threading
import progressbar
import requests.packages.urllib3
import sys
import base64
from bs4 import BeautifulSoup
import js2py
import youtube_dl
import signal
from tqdm import tqdm
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def download_from_url(url, title):
    if not os.path.exists("../91视频MP4/"):
        os.makedirs("../91视频MP4/")
    if not os.path.exists("../下载汇总/"):
        os.makedirs("../下载汇总/")
    dst="../91视频MP4/"+title+'.mp4'
    dst1 = "../下载汇总/"+title+'.mp4'
    if not os.path.exists(dst) and not os.path.exists(dst1):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
        response = s.get(url, headers=headers, stream=True) #(1)
        file_size = int(response.headers['content-length']) #(2)
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst) #(3)
        else:
            first_byte = 0
        if first_byte >= file_size: #(4)
            return file_size
        # headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com',"Range": f"bytes={first_byte}-{file_size}"}
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=dst)
        # req = s.get(url, headers=headers, stream=True) #(5)
        with(open(dst, 'ab')) as f:
            for chunk in response.iter_content(chunk_size=1024): #(6)
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        return file_size


# 定义随机ip地址
def random_ip():
    a=random.randint(1, 255)
    b=random.randint(1, 255)
    c=random.randint(1, 255)
    d=random.randint(1, 255)
    return (str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

encodedata2 = open("strencode2.js",'r',encoding= 'utf8').read()
encodedata1 =  open("strencode.js",'r',encoding= 'utf8').read()
strencode2 = js2py.eval_js(encodedata2)
strencode = js2py.eval_js(encodedata1)

def filter_str(desstr, restr=''):
    # 过滤除中英文及数字以外的其他字符
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    title = res.sub(restr, desstr).replace("Chinesehomemadevideo","")
    return title

requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接
# 爬虫主体，flag为页码
def spider():
    inputPage = input("请输入开始下载的页数：")
    inputtitle = input("请输入从当前页的第几个帖子开始下载：")
    page = int(inputPage)

    while int(page)<= int(100000):
        viewurl=[]
        # https://f1105.workarea3.live/v.php?category=rf&viewtype=basic&page=1
        # 如果连接访问不了，在这里把base_url替换成你知道的标准地址
        base_url = 'https://f1105.workarea3.live/view_video.php?viewkey='
        page_url = 'https://f1105.workarea3.live/v.php?next=watch&page='+str(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
            'Referer': 'http://91porn.com'}
        get_page=s.get(url=page_url, headers=headers)
        # 利用正则匹配出特征地址
        div = BeautifulSoup(get_page.text, "html.parser").find_all("div",class_="well well-sm videos-text-align")
        for i in div:
            viewurl.append(i.a.attrs["href"])
        arr = []
        if int(inputPage) ==  int(page):
            arr = range(-1 + int(inputtitle), len(viewurl))
        else:
            arr = range(0, len(viewurl))
        for index in arr:
            print('#' * 100)
            headers={'Accept-Language':'zh-CN,zh;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
                    'X-Forwarded-For': random_ip(),
                    'referer': page_url,
                    'Content-Type': 'multipart/form-data; session_language=cn_CN',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    }
            base_req = s.get(url=viewurl[index],headers=headers)
            a = re.compile('document.write\(strencode2\("(.*)"').findall(base_req.content.decode('utf-8'))
            url = ''
            if len(a)>0:
                a = a[0].split(',')
                text = a[0].replace('"', '')
                url = BeautifulSoup(strencode2(text), "html.parser").source.attrs['src']
            else:
                a= re.compile('document.write\(strencode\("(.*)"').findall(base_req.content.decode('utf-8'))
                text = a[0].split(',')
                url = BeautifulSoup(strencode(text[0].replace('"', ''),text[1].replace('"', ''),text[2].replace('"', '')), "html.parser").source.attrs['src']
            title = BeautifulSoup(base_req.text, "html.parser").title.text.replace(" ","").replace("\n","")
            title = filter_str(title)
            print('第'+str(page)+'页数据,共'+str(len(viewurl))+'条帖子 =>>>> 正在下载第'+str(index+1)+'个帖子……'+title)
            videotype = urlparse(url).path.split(".")[1]
            if videotype == "m3u8":
                if not os.path.exists("../91视频/"):
                    os.makedirs("../91视频/")
                if not os.path.exists("../91视频/"+title+".mp4"):
                    with open("urlwithtitle.txt", "r") as f:  # 打开文件
                        finddata = f.read()  # 读取文件
                        findindex = finddata.find(filter_str(title))
                    if findindex == -1:
                        with open("urlwithtitle.txt","a") as f:
                            f.write(url + "----"+title)
                            f.write("\n")
                        print("----------------下载结束------------------")
            else:
                download_from_url(url,filter_str(title))
            print('#' * 100 + '\n')
            time.sleep(3)
        page += 1


# i为线程数
def main():    
    work_thread = threading.Thread(target=spider)
    work_thread.daemon = True
    work_thread.start()
    signal.signal(signal.SIGINT, quit)
    print("Start Working")
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()


