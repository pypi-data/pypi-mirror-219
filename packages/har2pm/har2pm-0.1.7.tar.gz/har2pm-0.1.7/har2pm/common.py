import json
import logging
from urllib.parse import urlparse

import jmespath


def load_har(har_path):
    """

    :param har_path:
    :return:
    """
    with open(har_path, 'r', encoding='utf-8') as har:
        return json.load(har)


def save_postman_collection(file_path, postman_json):
    with open(file_path, 'w') as postman:
        postman.write(json.dumps(postman_json, indent=4, ensure_ascii=True))


def extract_params(query):
    """
    :param query: (str) eg: q=testerhome&encoding=utf-8
    :return:
        [
            {
                "key": "q",
                "value": "testerhome"
            },
            {
                 "key": "encoding",
                "value": "utf-8"
            }
        ]
    """
    params = []
    if not query:
        return params

    for i in query.split('&'):
        param = i.split('=')
        key = param[0]
        value = None
        if len(param) > 1:
            value = param[-1]
        params.append({
            'key': key,
            'value': value
        })
    return params


def convert_dict_key(har_dict):
    """

    :param har_dict: [
        {"name": "123", "value": "321"},
        ...
    ]
    :return: [
        {"key": "123", "value": "321"},
        ...
    ]
    """
    for header in har_dict:
        header['key'] = header.pop('name')

    return har_dict


def convert_url(har_request):
    """
    :param har_request: {'url': 'https://www.baidu.com:80/s?wd=12345'}
    :return: {
        'protocol': https,
        'host': ['www', 'baidu', 'com'],
        'port': 80,
        'path': ['s'],
        'query': [
            {'key': 'wd', 'value': '12345'},
            ...
        ]
    }
    """

    url = urlparse(har_request['url'])

    protocol = url.scheme

    host = url.netloc.split('.')

    port = url.port or ""

    path = url.path.split('/')

    # 提取query
    params = extract_params(url.query)

    return {
        'raw': url.path,
        'protocol': protocol,
        'host': host,
        'path': path,
        'port': port,
        'query': params
    }


def convert_headers(har_headers: list):
    """
        :param har_headers: [
            {"name": "123", "value": "321"},
            ...
        ]
        :return: [
            {"key": "123", "value": "321"},
            ...
        ]
        """

    black_list = ['content-length', 'accept-encoding']

    har_headers = list(filter(lambda x: x.get('name', '').lower() not in black_list, har_headers))

    def extract(header):
        header['key'] = header.pop('name')
        return header

    return list(map(extract, har_headers))


def convert_body(har_request):
    mime_type = jmespath.search('postData.mimeType', har_request)

    # t=False or t=[None]
    if not mime_type or mime_type is None:
        return None

    if mime_type.find('form-data') != -1:
        return {'mode': 'formdata', 'formdata': convert_dict_key(har_request['postData']['params'])}

    elif mime_type.find('x-www-form-urlencoded') != -1:
        return {'mode': 'urlencoded', 'urlencoded': convert_dict_key(har_request['postData']['params'])}

    elif mime_type.find('json') != -1:
        return {
            'mode': 'raw',
            'raw': har_request['postData']['text']
        }
    elif mime_type.find('plain') != -1:
        return {'mode': mime_type, 'raw': jmespath.search('postData.text', har_request)}

    else:
        logging.error('调用{},参数为：{}'.format(convert_body.__name__, mime_type, har_request))
        raise Exception('无法识别:%s' % mime_type)
