# **有道翻译破解案例(post)**

## 目标

```python
#破解有道翻译接口，抓取翻译结果
#通过抓包抓到有道真正执行翻译的url：这个url是一个post请求，难点在于post表单的制作。这里post表单参数有道进行了js加密，所以需要js解密
url="http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
```

## 实现步骤

- 真正的url

![真正的url](D:\Github\Github project\反爬\有道翻译反爬解密\真正的url.png)

```python
1、浏览器F12开启网络抓包,Network-All,页面翻译单词后找Form表单数据
2、在页面中多翻译几个单词，观察Form表单数据变化（有数据是加密字符串）
3、刷新有道翻译页面，抓取并分析JS代码（本地JS加密）
4、找到JS加密算法，用Python按同样方式加密生成加密数据
5、将Form表单数据处理为字典，通过session.post()的data参数发送
```

```python
# Formdata数据：
#第一次
i: bag
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 15849471478739
sign: 64ba051c2735c830e4194b79e07fc228
ts: 1584947147873
bv: 70244e0061db49a9ee62d341c5fed82a
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
    
# 第2次
i: pencil
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 15849471804079
sign: 5a5f500af8c07c17962761c844828d00
ts: 1584947180407
bv: 70244e0061db49a9ee62d341c5fed82a
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
  
#所以发现只有：salt、sign、ts、i在变动。其中i使我们自己输入的单词。所以只需破解salt、sign和ts即可
```



## **具体实现**

- 1、开启F12抓包，找到js文件如下:

  ![解密文件](D:\Github\Github project\反爬\有道翻译反爬解密\解密文件.png)

  ```python
  #是叫fanyimin.js
  ```

- 2、js具体抓到方法

```python
# 方法1
Network - JS选项 - 搜索关键词salt
# 方法2
控制台右上角 - Search - 搜索salt - 查看文件 - 格式化输出

# 最终找到相关JS文件 : fanyi.min.js
```

- 4、打开JS文件，分析加密算法，用Python实现

```python
# ts : 经过分析为13位的时间戳，字符串类型
js代码实现:  "" + (new Date).getTime()
python实现: ts = str(int(time.time()*1000))

# salt
js代码实现:  ts + parseInt(10 * Math.random(), 10);
python实现:  salt = ts + str(random.randint(0,9))

# sign（设置断点调试，来查看 e 的值，发现 e 为要翻译的单词）
js代码实现: n.md5("fanyideskweb" + e + salt + "Nw(nmmbP%A-r6U3EUn]Aj")
python实现:
from hashlib import md5
s = md5()
s.update('"fanyideskweb" + e + salt + "Nw(nmmbP%A-r6U3EUn]Aj"'.encode())
sign = s.hexdigest()
```

- e如何找到：
- ![断点测试](D:\Github\Github project\反爬\有道翻译反爬解密\断点测试.png)

- 5、代码实现

```python
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

```

## 难点

```python
1.有道翻译的真正的url，可以通过谷歌的XHR抓到
2.js解密，其中e需要断点测试才能知道代表什么
3.md5加密
```

