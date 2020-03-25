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





