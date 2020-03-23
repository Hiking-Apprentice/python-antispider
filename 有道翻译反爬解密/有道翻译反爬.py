# coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import requests, random
import time
from hashlib import md5
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

def get_parameter(word):
    #ts表示为毫秒级时间
    t = time.time()
    ts = str(int(round(t * 1000)))

    #salt表示ts外加一个随机变量
    salt = ts + str(random.randint(0, 10))

    #sign是经过md5加密后的结果
    sig = "fanyideskweb" + word + salt + "Nw(nmmbP%A-r6U3EUn]Aj"
    s = md5()
    s.update(sig.encode('utf-8'))
    sign = s.hexdigest()

    return ts,salt,sign

def crack(ts,salt,sign):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "238",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=-1449945727@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=1492587933.976261; JSESSIONID=aaa5_Lj5jzfQZ_IPPuaSw; ___rl__test__cookies=1559193524685",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    formdata = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": "70244e0061db49a9ee62d341c5fed82a",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }
    session = requests.session()

    res = session.post(url, data=formdata, headers=headers).json()
    result = res['translateResult'][0][0]['tgt']
    return result

def run(word):
    #先获得js加密的参数
    ts,salt,sign=get_parameter(word)
    result=crack(ts,salt,sign)
    print(result)


if __name__ == '__main__':
    word=input('请输入你要翻译的单词（中文或英文）：')
    run(word)



