import hashlib
import json
import requests
import time
from collections import OrderedDict

class Client:
    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.httpClient = requests.Session()
        self.httpClient.timeout = 10

    def post_open_api(self, requestURL, values):
        now = str(int(time.time()))
        values['apikey'] = self.apiKey
        values['timestamp'] = now

        sign = self.get_sign(values)

        headerMap = {
            'sign': sign,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = self.post_with_header(requestURL, values, headerMap)
        responseStr = response.text

        print(responseStr)

        response_data = json.loads(responseStr)

        if response_data['status'] != 0:
            return response_data['data'], Exception("open-api返回的状态码错误: " + response_data['reason'])

        return response_data['data'], None

    def post_with_header(self, url, data, headerMap):
        response = self.httpClient.post(url, data=data, headers=headerMap)
        response.raise_for_status()
        return response

    def get_sign(self, params):
        params['apisecret'] = self.apiSecret

        sorted_params = OrderedDict(sorted(params.items()))
        tmp = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])

        sign = self.md5_v(tmp)
        del params['apisecret']

        return sign

    def md5_v(self, str):
        md5_hash = hashlib.md5()
        md5_hash.update(str.encode('utf-8'))
        return md5_hash.hexdigest()

