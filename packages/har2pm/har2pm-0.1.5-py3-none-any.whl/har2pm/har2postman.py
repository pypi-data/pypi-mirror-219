import json
import logging
import os

import jmespath

from har2pm.common import (convert_url, load_har, save_postman_collection, convert_body, convert_headers)


class Har2Postman:

    def __init__(self, har_path):
        self.har_path = har_path
        self.postman_collection = {
            "info": {
                "name": "Har2toPostman",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            'item': []
        }

    def __convert_request(self, request):
        logging.debug('-----------------------item------------------')
        logging.debug('%s' % json.dumps(request, ensure_ascii=False))

        postman_request = {'method': request['method'], 'header': [], 'body': {}, 'url': convert_url(request)}

        if request['method'] == 'POST':
            postman_request['body'] = convert_body(request)

        # 处理 headers
        postman_request['header'] = convert_headers(request['headers'])

        self.postman_collection['item'].append({'name': request['url'], 'request': postman_request})

    def run(self, generate_file=True):
        logging.info(f'read {self.har_path}')

        data = load_har(self.har_path)
        requests = jmespath.search('log.entries[].request', data)

        logging.debug(f'request count: {len(requests)}')

        for request in requests:
            self.__convert_request(request)

        # 是否保存为.json文件
        if generate_file:
            tmp = os.path.splitext(self.har_path)[0]
            postman_collection_path = '{}.json'.format(tmp)
            logging.info('Generate postman collection successfully: %s' % postman_collection_path)
            save_postman_collection(postman_collection_path, self.postman_collection)
        return 0
