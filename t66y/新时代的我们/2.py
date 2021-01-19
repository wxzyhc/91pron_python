import requests
import os
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import signal
import sys
import threading

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36", 'Cache-Control': 'no-cache'}

titles = []
links = []

requestURL = 'https://cl.nh52.xyz/'
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接

def get_info(site, titles, links):
    re = s.get(site, headers=header)
    re.encoding = 'gbk'
    td = BeautifulSoup(re.text, "html.parser").find_all('td', class_='tal')
    for i in td:
        name = i.contents[0].replace('\n', '').replace(
            '\r', '').replace('\t', '')
        titles.append(i.contents[0].replace('\n', '').replace(
                '\r', '').replace('\t', '')+' '+i.h3.string.replace('?', ''))
        links.append(requestURL + i.a['href'])


def download_img(title, link):
    nomakechar =  [":","/","\\","?","*","“","<",">","|"]
    for item in nomakechar:
        if title.find(item)>-1:
            title = title.replace(item, '')
    if os.path.exists(title):
        return
    os.makedirs(title)
    re = s.get(link, headers=header)
    re.encoding = 'gbk'
    div = BeautifulSoup(re.text, "html.parser").find_all(
        'div', class_='tpc_content do_not_catch')[0]
    img = BeautifulSoup(str(div), "html.parser").find_all('img')
    pbar = tqdm(total=len(img))
    for i in img:
        file_name = title + '/' + str(img.index(i)) + '.jpg'
        if not os.path.exists(file_name):
            download_link = ''
            if i.get('data-src') == None:
                download_link = i.get('ess-data')
            else:
                download_link = i.get('data-src')
            index = 1
            while True:
                try:
                    re = s.get(download_link, headers=header)
                    with open(file_name, 'wb') as f:
                        f.write(re.content)
                except:
                    index += 1
                    continue
                else:
                    break
        pbar.update(1)
    pbar.close()

def quit(signum, frame):
    print("Bye!")
    sys.exit(0)

def work():
    re = s.get(
        requestURL+'thread0806.php?fid=8&search=&page=1', headers=header)
    re.encoding = 'gbk'
    tabA = BeautifulSoup(re.text, "html.parser").find('a', class_='w70')
    pages = tabA.contents[0].attrs["value"].split('/')[1]
    print(pages)
    inputPage = input("请输入开始下载的页数：")
    page = int(inputPage)
    inputtitle = input("请输入从当前页的第几个帖子开始下载：")

    while page <= int(pages):
        site = requestURL+'thread0806.php?fid=8&search=&page='+str(page)
        titles = []
        links = []
        get_info(site, titles, links)
        arr = []
        if page == 1:
            arr = range(7 + int(inputtitle), len(titles))
        else:
            arr = range(-1 + int(inputtitle), len(titles))
        for i in arr:
            print('#' * 100)
            if page == 1:
                print('第'+str(page)+'页数据,共'+str(len(titles)) +
                      '条帖子 =>>>> 正在下载第'+str(i-6)+'个帖子……'+titles[i])
            else:
                print('第'+str(page)+'页数据,共'+str(len(titles)) +
                      '条帖子 =>>>> 正在下载第'+str(i+1)+'个帖子……'+titles[i])
            download_img(titles[i], links[i])
            print('#' * 100 + '\n\n')
            time.sleep(3)
        page += 1


def main():
    work_thread = threading.Thread(target=work)
    work_thread.daemon = True
    work_thread.start()
    signal.signal(signal.SIGINT, quit)
    print("Start Working")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
