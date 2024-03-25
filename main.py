from spider import *
from queue import Queue
import pandas as pd

from pybloom_live import ScalableBloomFilter, BloomFilter   #布隆过滤器
def init_bloom(size=2e8):
    bloom = BloomFilter(capacity=size)
    return bloom


query_queue = [] #输入请求网址
init_url = '在此输入网址'
query_queue.append(init_url)    #队列

url_filter = init_bloom(size=80000) #设计所要爬取的信息量   #布隆过滤器最大线程量
url_list = [init_url] #暂存已经访问的网址
tel_dict = {} #暂存已经存储的联系方式


def save_tel(name, tel):#存储电话号码
    if name in tel_dict.keys():
        tel_dict[name] = tel_dict[name] | set(tel)
    else:
        tel_dict[name] = set(tel)


def main():
    try:
        cnt = 0
        print('enter main')
        while len(query_queue) > 0:#网址不为空，继续爬取
            url = query_queue.pop(0)

            # 对url进行解析
            page = get_response(url)
            if not page == None:
                temp_url_list = get_url(page, url)   #获取页面网址
                org, temp_tel_list = get_info(page)   #获取部门，电话号码
            else:
                temp_url_list = []
                org , temp_tel_list = None, []

            # 将联系赞时存储起来
            if len(temp_tel_list) > 0:
                save_tel(org, temp_tel_list)
                print(org, temp_tel_list)

            # 将之后要访问的url储存起来
            for url in temp_url_list:
                if not url in url_filter:
                    url_filter.add(url)    #将网址存储到集合中
                    query_queue.append(url)   #网址进栈，加入到集合末尾
                    url_list.append(url)
    except IndexError as e:
        print(e)
    finally:#输出为csv文件
        print("======== Spider part is done. Saving data as files ======")
        tel_dict.update((key, str(val)) for key ,val in tel_dict.items())
        df = pd.DataFrame(list(tel_dict.items()))
        df.to_csv('data1.csv',encoding='ANSI')#输出位置
        print(df)


if __name__ == '__main__':
    main()
