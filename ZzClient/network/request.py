import asyncio
import json
import aiohttp
from PyQt5.QtCore import pyqtSignal, QObject

"""https://github.com/jiangfubang/jfbrequests"""

loop = asyncio.get_event_loop()

async def main(url, method, timeout=None, headers=None, cookies=None, proxy=None, data=None, params=None):
    async with aiohttp.ClientSession() as client:
        try:
            async with client.request(url=url, method=method, headers=headers, timeout=timeout, cookies=cookies,
                                      proxy=proxy, data=data, params=params) as resp:
                return HighResponse(await resp.read(), resp)
        except:
            pass

def request(url, method, timeout=None, headers=None, cookies=None, proxy=None, data=None, params=None):
    return loop.run_until_complete(main(url, method, timeout, headers, cookies, proxy, data, params))

def get(url, timeout=60, headers=None, cookies=None, proxy=None, data=None):
    return request(url, 'GET', timeout, headers, cookies, proxy, data=None, params=data)

def post(url, timeout=60, headers=None, cookies=None, proxy=None, data=None):
    return request(url, 'POST', timeout, headers, cookies, proxy, data=data, params=None)

class HighResponse():
    def __init__(self, content, clientResponse):
        self.content = content
        self.clientResponse = clientResponse

    def raw(self):
        return self.clientResponse

    @property
    def url(self):
        return self.clientResponse.url

    @property
    def cookies(self):
        return self.clientResponse.cookies

    @property
    def headers(self):
        return self.clientResponse.headers

    @property
    def status(self):
        return self.clientResponse.status

    @property
    def method(self):
        return self.clientResponse.method

    @property
    def text(self, encoding="utf-8"):
        return self.content.decode(encoding=encoding)

    @property
    def json(self):
        return json.loads(self.text)

    def get_value_from_key(self, key):
        json_results = []
        return get_value_by_key(self.json, json_results, key)[0]

    def get_values_from_key(self, key):
        json_results = []
        return get_value_by_key(self.json, json_results, key)

    def __repr__(self):
        return "<HighResponse [status {}]>".format(self.clientResponse.status)

    __str__ = __repr__

def get_dict_from_str(param):
    params = {}
    for data in param.split('\n'):
        params.update({data.split(':')[0].strip(): data.split(':')[1].strip()})
    return params

def get_value_by_key(input_json, results, key):
    key_value = ''
    if isinstance(input_json, dict):
        for json_result in input_json.values():
            if key in input_json.keys():
                key_value = input_json.get(key)
            else:
                get_value_by_key(json_result, results, key)
    elif isinstance(input_json, list):
        for json_array in input_json:
            get_value_by_key(json_array, results, key)
    if key_value != '':
        results.append(key_value)
    return results

class Result(object):
    def __init__(self, json):
        if json is None:
            return
        self.code = ResultCode(int(json["code"]))
        if "msg" in json:
            self.code.setMsg(json["msg"])
        if "dict" in json:
            self.dict = json["dict"]
        if "dicts" in json:
            self.dicts = json["dicts"]

    @property
    def msg(self):
        return self.code.msg

    @property
    def valid(self):
        return self.code.valid

class ResultCode(object):
    jsonIllegal     = 101
    _jsonIllegal    = "数据异常"
    success         = 200
    _success        = "请求成功"

    def __init__(self, code, msg=None):
        self.code = code
        self.msg = msg if msg is not None else self.msg(code)

    def setMsg(self, msg):
        self.msg = msg

    def msg(self, code):
        if code == self.success:
            return self._success
        elif code == self.jsonIllegal:
            return self._jsonIllegal
        else:
            return "unknown"

    @property
    def valid(self):
        if self.code == self.success:
            return True
        else:
            return False

    @property
    def value(self):
        return self.code

class ResultSet:
    jsonIllegal = ResultCode(ResultCode.jsonIllegal)