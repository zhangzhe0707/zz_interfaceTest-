import requests
import json
import operationConfig as getConfig
from base.log import Log

localGetConfig = getConfig.OperationConfig()


class BaseHttp:
    """
    http请求封装类
    """

    def __init__(self):
        log = Log()
        self.log = log.get_logger()
        self.scheme = localGetConfig.get_http('scheme')
        self.baseurl = localGetConfig.get_http('baseurl')
        self.timeout = localGetConfig.get_http('timeout')
        self.url = self.scheme + '://' + self.baseurl

    def change_type(self, value):
        """
        对字典中的value值的中文进行识别转换
        :param value:
        :return:
        """
        try:
            if isinstance(eval(value), str):
                return value
            if isinstance(eval(value), dict):
                result = eval(json.dumps(value))
                return result
        except BaseException as e:
            self.log.error("change_type 转换错误:{0}".format(e))

    def get(self, uri, params):
        """
        Get请求方法
        :return:
        """
        # 拼装接口请求地址
        url = self.url + uri
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            response = requests.get(url, headers=headers, params=params)
            # self.log.info("GET 请求成功，返回体内容：{0} ".format(response))
            # self.log.info("GET 请求成功，返回体data：{0} ".format(response.content))
            return response
        except TimeoutError:
            self.log.error("请求超时失败!")

    def post(self, uri, data):
        """
        Post 请求方法
        """
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        # 拼装接口请求地址
        url = self.url + uri
        try:
            response = requests.post(url, headers=headers, data=data,
                                     timeout=float(self.timeout))
            self.log.info("POST 请求成功，返回体内容：{0} ".format(response))
            self.log.info("POST 请求成功，返回体data：{0} ".format(response.content))
            return response
        except TimeoutError:
            self.log.error("请求超时失败!")
            return None

    def post_with_json(self, uri, data):
        """
        Post 请求，数据体为 json
        :return:
        """
        headers = {'Content-Type': 'application/json'}
        # 拼装接口请求地址
        url = self.url + uri
        try:
            response = requests.post(url=url, headers=headers, json=data, timeout=float(self.timeout))
            # self.log.info("POST 请求发送Json成功，返回体：{0} ".format(response))
            # self.log.info("POST 请求发送Json成功，返回体data：{0} ".format(response.content))
            return response
        except TimeoutError:
            self.log.error("请求超时失败!")
            return None

