# coding: UTF-8
"""
user: 五根弦的吉他
func：爬取浙大教务处的验证码（很适合入门，太规整了这验证码！！不知是好事还是坏事）
description： 单进程与多进程都有，把注释去掉即可更换单多进程
"""
import requests
from fake_useragent import UserAgent
import os
from hashlib import md5
import random
from datetime import datetime
from multiprocessing.pool import Pool

url = 'http://jwbinfosys.zju.edu.cn/CheckCode.aspx'
headers = {'User-Agent': UserAgent(use_cache_server=False).random}
folder = 'zheda_aspx'
proxies = [{"http": "http://157.230.236.97:8080"},
            {"http": "http://147.135.121.131:8080"},
            {"http": "http://68.183.53.127:8080"},
            {"http": "http://104.248.51.135:8080"},
            {"http": "http://206.81.11.75:8080"},
            {"http": "http://67.205.133.13:8080"},
            {"http": "http://178.128.156.143:8080"},
            {"http": "http://157.230.54.155:8080"},
            {"http": "http://134.209.123.111:8090"},
            {"http": "http://157.230.220.233:8080"},
            {"http": "http://134.209.45.249:8080"}]

'''
def main():
    """
    单进程
    :return:
    """
    if not os.path.exists(folder):
        os.mkdir(folder)
    for i in range(1, get_num+1):

        try:
            response = requests.get(url=url, headers=headers, proxies=random.choice(proxies))
            if response.status_code == 200:
                file = '{}/{}.{}'.format(folder, md5(response.content).hexdigest(), save_format)
                if not os.path.exists(file):
                    with open(file, 'wb') as f:
                        f.write(response.content)
                        print('抓取第{}张验证码成功'.format(i))
                        response.close()
                else:
                    print('已下载过了')
        except Exception as e:
            print('Error:', e.args)
'''


def main(num):
    """
    多进程
    :return:
    """
    if not os.path.exists(folder):
        os.mkdir(folder)

    try:
        response = requests.get(url=url, headers=headers, proxies=random.choice(proxies))
        if response.status_code == 200:
            file = '{}/{}.{}'.format(folder, md5(response.content).hexdigest(), save_format)
            if not os.path.exists(file):
                with open(file, 'wb') as f:
                    f.write(response.content)
                    print('抓取第{}张验证码成功'.format(md5(response.content).hexdigest()))

                    response.close()

            else:
                print('已下载过了')
    except Exception as e:
        print('Error:', e.args)


if __name__ == '__main__':

    start = datetime.now()
    """
    # 单进程
    
    
    get_num = 1000
    
    save_format = 'aspx'
    main()
    """
    # *********************************
    """
    多进程
    """
    get_num = 1000
    save_format = 'aspx'
    pool = Pool()
    numlist = [i for i in range(1, get_num + 1)]
    pool.map(main, numlist)
    pool.close()
    pool.join()
    # **********************************
    print("Done!")
    end = datetime.now()
    print("Duration:", end-start)


