import http.client
import math
from concurrent.futures import ThreadPoolExecutor
from urllib import request

from bs4 import BeautifulSoup

COOKIES = None
HOST = 'https://bing.ioliu.cn/'
NUMBERTHREAD = 6
THREADPOOL = ThreadPoolExecutor(NUMBERTHREAD)


def ioliudownload(path):
    amt = get_amt_of_page(HOST)

    for i in range(1, int(amt)):
        myhost = HOST
        pageurl = myhost + '?p=' + str(i)
        # print(pageurl)
        home_page = 'home_' + str(i)
        __get_the_page(path, pageurl, home_page)


def get_amt_of_page(host: str):
    '''
    获取页数
    :param host:
    :return:
    '''
    response = __simpleget(host)
    body = str(response.read())
    soup = BeautifulSoup(body, 'html.parser')
    page = soup.find('div', attrs={'class': 'page'}).find('span')
    return page.contents[0].split('/')[1]


def __get_pic_intro(soup: BeautifulSoup):
    div = soup.find_all('div', attrs={'class': 'description'})
    soup1 = BeautifulSoup(div.__str__(), 'html.parser')
    intro = soup1.find('h3').contents[0]
    return intro


def __get_the_page(path, pageurl, home_page):
    """
获取本页面所有的的下载链接
    :param path:
    :param home_page:
    """
    response = __simpleget(uri=pageurl)
    page = str(response.read().decode('utf-8'))
    soup = BeautifulSoup(page, 'html.parser')
    i = soup.find_all('a', attrs={'class': 'mark'})
    uri_list = []
    for href in i:
        sub = str(href['href']).replace(home_page, 'download')
        uri_list.append(sub)

    work(uri_list, path)
    # i[]
    # for href in it:
    #     lock = threading.Lock()
    #     sub = str(href['href']).replace(home_page, 'download')  # 转换为下载链接
    #     threadpool.submit(__download(HOST, sub, path, __get_pic_intro(soup)))


def work(download_url_list: list, path: str):
    lens = len(download_url_list)
    if lens is None or 0:
        raise Exception('传入url列表为空')
    count = 0
    step_length = math.ceil(lens / NUMBERTHREAD)
    fs = []
    for i in range(NUMBERTHREAD):
        uri = download_url_list[count:count + step_length]
        f = THREADPOOL.submit(__download, uri, path)
        fs.append(f)
        count += step_length

    for f in fs:
        res = f.result()
        save_pic(res[0], res[1])


def __simpleget(uri=None):
    header = {'Connection': 'keep-alive',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                        'application/signed-exchange;v=b3;q=0.9 '
              }
    if uri is None:
        raise Exception('uri为None')
    else:
        req = request.Request(uri, headers=header, method="GET")
    return request.urlopen(req)


def __download(uri_list: list = None, path: str = None):
    print()
    if path is not None and uri_list is not None:
        na = []
        res = []
        for uri in uri_list:
            name = uri.split('/')[2].split('?')[0]  # 通过分割字符串得到文件名
            filename = str(path + name + '.jpg')
            url = HOST + uri
            print(url)
            try:
                response = __simpleget(url).read()
            except http.client.IncompleteRead as e:
                response = e.partial
            res.append(response)
            na.append(filename)
        return na, res
    else:
        raise Exception('uri,host或者path为None')


def save_pic(name: list, res: list):
    for na, re in zip(name, res):
        print(type(re))
        file = open(str(na).encode('utf-8'), 'wb', 2048)

        file.write(re)
        # picoperation.modify_meta(filename, intro)


if __name__ == '__main__':
    ioliudownload('C:\\file\\Bing\\')
