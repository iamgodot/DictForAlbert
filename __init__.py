'''
Albert Python Plugin:

    https://github.com/albertlauncher/plugins/tree/master/python

'''
import hashlib
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from uuid import uuid1

import requests

__title__ = 'Dictionary for Albert'
__version__ = '0.1.0'
__triggers__ = 'd'
__authors__ = 'iamgodot'

cwd = Path(__file__).parent
ICON_PATH = str(cwd / 'logo.svg')

parser = ConfigParser()
parser.read(cwd / 'config.ini')

APP_KEY = parser['youdao']['app_key']
APP_SECRET = parser['youdao']['app_secret']
YOUDAO_URL = 'https://openapi.youdao.com/api'


def _make_item(text='', subtext='', actions=None):
    from albert import Item
    return Item(id=__title__,
                icon=ICON_PATH,
                text=text,
                subtext=subtext,
                actions=actions or [])


def handleQuery(query):
    from albert import UrlAction

    if query.isTriggered:
        stripped = query.string.strip()
        answer = 'Enter a word to query'
        if stripped:
            answer = translate(stripped)
            if isinstance(answer, dict):
                return [
                    _make_item(text=meaning,
                               subtext=answer.get('phonetic', ''),
                               actions=[
                                   UrlAction(text='open youdao web',
                                             url=answer['url'])
                               ]) for meaning in answer.get('meanings', [])
                ]

        return _make_item(answer)


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def query_youdao_api(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(YOUDAO_URL, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()


def translate(query):
    en_to_ch = query.isascii()
    if en_to_ch:
        lang_from, lang_to = 'en', 'zh-CHS'
    else:
        lang_from, lang_to = 'zh-CHS', 'en'
    salt = str(uuid1())
    timestamp = str(int(datetime.now().timestamp()))
    payload = {
        'from': lang_from,
        'to': lang_to,
        'signType': 'v3',
        'curtime': timestamp,
        'appKey': APP_KEY,
        'q': query,
        'salt': salt,
        'sign':
        encrypt(APP_KEY + truncate(query) + salt + timestamp + APP_SECRET),
        'vocabId': '',
    }

    resp_json = query_youdao_api(payload)
    if not resp_json.get('basic'):
        result = f'{query} not found'
    else:
        basic = resp_json['basic']
        result = {
            'meanings': basic.get('explains', []),
            'url': f'https://www.youdao.com/w/eng/{query}',
        }
        if en_to_ch:
            phonetic_us = basic.get('us-phonetic')
            phonetic_uk = basic.get('uk-phonetic')
            if phonetic_us and phonetic_uk:
                result['phonetic'] = f'英：[{phonetic_uk}], 美：[{phonetic_us}]'

    return result
