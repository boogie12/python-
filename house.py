import requests
from bs4 import BeautifulSoup
import re
import csv
class GetLianJia():
    def __init__(self,pagenum,address):
        self.pagenum = pagenum
        self.address = address
    # 翻页 以及选择城市
    def get_url(self): #page后面是页数 rs后面是地址
        url='https://wh.lianjia.com/zufang/pg'+str(self.pagenum)+'rs'+str(self.address)+'/#contentList'
        return url
    # 解出目标网页
    def get_target_url(self):
        # url='https://wh.lianjia.com/zufang/pg3rs%E6%AD%A6%E6%B1%89/#contentList' #rs后面是具体的地址(武汉) 可更改
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        response = requests.get(self.get_url(),headers=headers)
        if response.status_code == 200:
            demo = response.text #网页文本文件
            soup = BeautifulSoup(demo,'lxml')
            item = soup.find_all('p',{'class':'content__list--item--title twoline'})
            ze=r"/.*\.html"
            for i in item:
                for j in i:
                    url_ = re.findall(ze,str(j))
            # print(item.attrs)
                    if url_ != []:
                        target_url = 'https://wh.lianjia.com'+url_[0]
                        title = self.get_title(target_url)
                        info = self.get_info(target_url)
                        money = self.get_money(target_url)
                        area = self.get_area(target_url)
                        picture = self.get_picture(target_url)
                        header = ['标题','房屋信息','租金','面积','图片','房源链接']
                        values = [(title,info,money,area,picture,target_url)]
                        with open('data.csv','a+',encoding='utf-8',newline='') as fp:
                            writer = csv.writer(fp)
                            writer.writerow(header)
                            writer.writerows(values)
    # 得到目标标题
    def get_title(self,target_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        # target_url = 'https://wh.lianjia.com/zufang/WH2329469084426567680.html'
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            demo = response.text  # 网页文本文件
            soup = BeautifulSoup(demo, 'lxml')
            # item = soup.find_all('p',{'class':'content__title'})
            item = soup.find_all('img')
            ze = r'.jpg\Z|.png\Z'
            try:
                for j in item:
                    if(re.findall(ze,j.attrs["src"])):
                        # print(j.attrs["src"])
                        return j.attrs["alt"]
            except Exception:
                pass
    # 获取目标房屋信息
    def get_info(self,target_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        # target_url = 'https://wh.lianjia.com/zufang/WH2329469084426567680.html'
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            demo = response.text  # 网页文本文件
            soup = BeautifulSoup(demo, 'lxml')
            item = soup.find_all('li',{'class':'fl oneline'})
            lis = []
            # print(item)
            for i in item:
                for j in i:
                    lis.append(j)
                    return '-'.join(lis[:])
    # 获取价格
    def get_money(self,target_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        # target_url = 'https://wh.lianjia.com/zufang/WH2329469084426567680.html'
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            demo = response.text  # 网页文本文件
            soup = BeautifulSoup(demo, 'lxml')
            item = soup.find_all('p',{'class':'content__aside--title'})
            # print(item)
            lis = []
            for i in item:
                for j in i:
                    for a in j:
                        if a is not None:
                            lis.append(a)
            return ''.join(lis[1:5])
    # 获取面积
    def get_area(self,target_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        # target_url = 'https://wh.lianjia.com/zufang/WH2331658141118504960.html'
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            demo = response.text  # 网页文本文件
            soup = BeautifulSoup(demo, 'lxml')
            item = soup.find_all('p', {'class': 'content__article__table'})
            # print(item)
            lis = []
            for i in item:
                for j in i:
                    for a in j:
                        for x in a:
                            lis.append(x)
            return ''.join(lis)
    # 获取图片
    def get_picture(self,target_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        # target_url = 'https://wh.lianjia.com/zufang/WH2329469084426567680.html'
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            demo = response.text  # 网页文本文件
            soup = BeautifulSoup(demo, 'lxml')
            # item = soup.find_all('p',{'class':'content__title'})
            item = soup.find_all('img')
            ze = r'.jpg\Z|.png\Z'
            try:
                for j in item:
                    if(re.findall(ze,j.attrs["src"])):
                        return j.attrs["src"]
            except Exception:
                pass



if __name__ == '__main__':
    i=2
    try:
        a = GetLianJia(i,'武汉')
        i+=1
        a.get_target_url()
    except Exception as  e:
        print(e)
# get_money()

# print(get_url(5,'武汉'))

# get_url(5,'武汉')
