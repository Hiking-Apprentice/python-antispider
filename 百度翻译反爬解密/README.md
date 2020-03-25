# **百度翻译反爬解密**

## **目标**

```python
破解百度翻译接口，抓取翻译结果数据
```

## **实现步骤**

### **1、F12抓包,找到json的地址,观察Form表单数据**

```python
1、POST地址: https://fanyi.baidu.com/v2transapi
2、Form表单数据（多次抓取在变的字段）
   #这两个是你需要翻译的语种
   from: zh
   to: en
   #这个sign相比于有道翻译那个难，只要sign解决了就没问题了
   sign:  
   # 基本固定,跟浏览器有关。直接抓过来用就好，不用改
   token: 1eb38341d1d4b3f659a93f1836aa40e9
  
```

### **2、抓取相关JS文件**

```python
右上角 - 搜索 - sign: - 找到具体JS文件(index_c8a141d.js) - 格式化输出
```

### **3、在JS中寻找sign的生成代码**

```python
1、在格式化输出的JS代码中搜索: sign: 找到如下JS代码：sign: y(a),
2、通过设置断点，找到m(a)函数的位置，即生成sign的具体函数
   # 1. a 为要翻译的单词
   # 2. 鼠标移动到 y(a) 位置处，点击可进入具体y(a)函数代码块
```

### **4、生成sign的m(a)函数具体代码如下(在一个大的define中)**

```javascript
function a(r) {
    if (Array.isArray(r)) {
        for (var o = 0, t = Array(r.length); o < r.length; o++)
            t[o] = r[o];
        return t
    }
    return Array.from(r)
}

function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}

function e(r) {
    var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === o) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
    } else {
        for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
            "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
            C !== h - 1 && f.push(o[C]);
        var g = f.length;
        g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
    }
    #这个地方的var u值直接用过断点测试找到，然后重写就好
    // var u = void 0
    //     , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
    // u = null !== i ? i : (i = window[l] || "") || "";
    var u = '320305.131321201'
    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
        var A = r.charCodeAt(v);
        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
    }
    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
        p += S[b],
            p = n(p, F);
    return p = n(p, D),
        p ^= s,
    0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
    p.toString() + "." + (p ^ m)
}

var i = null;

```

### **5、直接将代码写入本地js文件,利用pyexecjs模块执行js代码进行调试**

```python
1、安装pyexecjs
   sudo pip3 install pyexecjs
2、安装js执行环境:nodejs
   sudo apt-get install nodejs
# 执行js代码流程
import execjs
with open('node.js','r') as f:
    js_data = f.read()
execjs_obj = execjs.compile(js_data)
sign = execjs_obj.eval('e("{}")'.format()) #这个输入你要翻译的单词
```

### **具体代码实现**

```python
#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020/3/25 14:09  
document:text.py
IDE：PyCharm 
'''
import execjs
import requests
import re

def get_parameter(word):
    #打开js文件找到sign
    with open('node1.js', 'r') as f:
        js_data = f.read()
    exec_obj = execjs.compile(js_data)
    sign = exec_obj.eval('e("{}")'.format(word))
    print(sign)
    return sign

def crack(sign,word):
    headers = {
        'cookie':'BAIDUID=1DD1F4C616F8CDDC4233D4E22FDBBC0F:FG=1; BIDUPSID=1DD1F4C616F8CDDC4233D4E22FDBBC0F; PSTM=1566211897; BDUSS=kFPWXN5bEN1UzViV2FVcTNHbXd5aWxpRHdKYWNJUjhlMWlHSXpLRm1lOWVzb3BlSVFBQUFBJCQAAAAAAAAAAAEAAAAn2~dDtqzmv8~EsKxjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF4lY15eJWNed; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=142978_143859_142508_141749_142058_140842_142080_143577_142205_142113_142019_140631_139049_141744_143867_143786_139176_141899_142780_136861_131246_137743_138165_138883_140259_141941_127969_140065_143995_140593_143057_141808_140350_138425_143471_143923_143276_131423_144003_107315_138595_143477_142911_140367_140798_143549_141364_110085; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; H_PS_PSSID=30974_1465_31169_21084_30906_30823_31085_26350; delPer=0; PSINO=5; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1585112931,1585112934,1585112941,1585115086; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1585116994; __yjsv5_shitong=1.0_7_682fb3ec7febd040c273111c3b81e18351e4_300_1585116994730_61.170.153.184_2060026f; yjs_js_security_passport=49e22386ecd73b62124aca6c75efd4039e895c77_1585116997_js',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    url='https://fanyi.baidu.com/v2transapi'
    formdata = {
        "from": "en",
        "to": "zh",
        "query": word,
        # 'transtype': 'realtime',
        # 'simple_means_flag': '3',
        "sign": sign,
        'token':'1eb38341d1d4b3f659a93f1836aa40e9',
        # 'domain': 'common'
    }
    session = requests.session()

    res = session.post(url, data=formdata, headers=headers).json()
    result = res['trans_result']['data'][0]['dst']
    return result

def run(word):
    #先获得js加密的参数
    sign=get_parameter(word)
    result=crack(sign,word)
    print(result)


if __name__ == '__main__':
    word=input('请输入你要翻译的单词（英文）：')
    run(word)


```

## 总结

- 抓包方式和有道翻译那个几乎一样
- js破解逻辑思路一样
- 难度比有道翻译难一点，主要有一个js函数我们不知道他怎么运行，不过不重要用暴力破解法即可