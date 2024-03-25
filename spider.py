import chardet      #网络爬虫
import requests as rq
from bs4 import BeautifulSoup as bs
from restr import *
import lxml
def get_response(url):     #对于输入的url网址代码进行解析
    try:
        response = rq.request(url=url, method='get',timeout=1)
        response.raise_for_status()    #异常处理
        response.encoding = response.apparent_encoding
        if not response == None:
            return bs(response.content,'lxml')   #解析网页的html标签
        return response
    except:
        print(f'网址{url} 无响应, 已跳过该网址')
        return None


def get_base_url(url):     #记录已经访问过的网页页面
    regex_exp = r'(?<=://)[a-zA-Z\.0-9]+(?=\/)'
    baseurl = re.findall(regex_exp, url, re.U)
    if baseurl:
        return baseurl[0]
    return None


def get_info(page):    #通过正则表达式，提取处理过的网页中的电话号码及单位名称
    content = str(page)
    org = find_org(content)
    tel_list = find_tel(content)
    tel_list = [tel.replace(u'\xa0',u'') for tel in tel_list]
    return org, tel_list


def get_url(soup, url):   #获取网页中的所有超链接
    try:
        baseurl = get_base_url(url)
        if baseurl == None:
            return []
        baseurl = 'https://' + baseurl + '/'     #设计模板，判断哪些为所要的网页链接
        tags = soup.select("a")
        ans = set()
        for a in tags:
            if not a.get('href') == None:
                context = str(a['href'])
                if context.endswith('.htm') and not context.startswith('http'):
                    ans.add(baseurl + a['href'])
                elif context.__contains__('xmu.edu.cn') and not context.endswith('pdf'):
                    ans.add(a['href'])
        return ans
    except KeyError as ke:
        print(f'{url} do not has key {ke}')
        return None
