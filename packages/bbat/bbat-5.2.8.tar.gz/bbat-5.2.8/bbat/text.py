import hashlib
import json
import re
import time
from typing import Any
from urllib.parse import parse_qs, urlparse
import uuid



def parse_json(str='{"demo":1}'):
    return json.loads(str)



def parse_mysql_url(url="mysql://username:password@localhost:3306/database_name?param1=value1&param2=value2"):
    parser = urlparse(url)
    query_string = parser.query
    query_params = parse_qs(query_string)
    
    db_dict = {
        'scheme': parser.scheme,
        'host': parser.hostname,
        'port': parser.port,
        'user': parser.username,
        'password': parser.password,
        'database': parser.path[1:],  # 去除路径中的斜杠
        'query_params': query_params
    }
    return db_dict



def remove_punctuation(sentence: str, punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'):
    dic = str.maketrans('', '', punctuation)
    return sentence.translate(dic)


# 匹配并抠出
def cutout(pattern, string):
    '''
    cutout(r'\(.*?\)', string)
    '''
    string = string.replace(" ", "")
    match = re.findall(pattern, string)
    if len(match) > 0:
        for i in match:
            string = string.replace(i, "")
        return string, match[0]
    return string, None



def symbol_split(string):
    ls = list()
    buff = ""
    enclosed = []
    symbol = ['(', ')', '[', ']', '{', '}']
    for i, val in enumerate(string):
        if i == len(string) - 1:
            buff += val
            ls.append(buff)
            buff = ""
        if val in symbol:
            index = symbol.index(val)
            if len(enclosed) > 0 and index - enclosed[-1] == 1:
                enclosed.pop()
            else:
                enclosed.append(index)
        if val == "," and len(enclosed) == 0:
            ls.append(buff)
            buff = ""
            continue
        buff += val
    return ls

def is_chinese(char):
    '''判断是否是中文'''
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False

def chinese_to_pinyin(text='北京'):
    from xpinyin import Pinyin
    p = Pinyin()
    return p.get_pinyin(text).replace('-', '')

class Translator:

    def __init__(self, key="705d93e03f2780e6", secret="KaVHXgpo15lgOHHJ5907bRY05eCj5X6N"):
        self.host = 'https://openapi.youdao.com/api'
        self.key = key
        self.secret = secret
    
    def __call__(self, text):
        return self.translate(text)
    
    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()


    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def gen_signature(self, q, curtime, salt):
        signStr = self.key + self.truncate(q) + salt + curtime + self.secret
        sign = self.encrypt(signStr)
        return sign


    def translate(self, text="你好"):
        '''有道翻译'''
        import requests

        curtime = str(int(time.time()))
        salt = str(uuid.uuid1())

        data = {}
        data['from'] = 'auto'
        data['to'] = 'auto'
        data['signType'] = 'v3'
        data['curtime'] = curtime
        data['appKey'] = self.key
        data['q'] = text
        sign = self.gen_signature(text, curtime, salt)
        data['salt'] = salt
        data['sign'] = sign
        # data['vocabId'] = "您的用户词表ID"

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.host, data=data, headers=headers)
        # contentType = response.headers['Content-Type']
        resp = response.json()
        # print(resp)
        data = {
            "translation": resp.get("translation"),
            "basic": resp.get("basic")
        }
        translation = data['translation']
        if not translation:
            return ''
        if len(translation) > 0:
            return "".join(data['translation'])
        return translation
    
