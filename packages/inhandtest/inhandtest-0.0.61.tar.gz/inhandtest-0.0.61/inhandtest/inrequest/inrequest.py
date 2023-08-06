# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 9:23:56
# @Author  : Pane Li
# @File    : inrequest.py
"""
封装request， 使设备和平台都能来正常调用，统一入口，token过期时也能自动更新

"""
import base64
import os
import urllib3
import requests
from inhandtest.exception import ParameterValueError, UsernameOrPasswordError
from inhandtest.file import file_hash
from inhandtest.tools import dict_in, dict_merge
import logging


class InRequest:

    def __init__(self, host: str, username: str, password: str, type_='device', protocol='https', port=443, **kwargs):
        """支持设备，平台登录及操作API, 自动识别地址

        :param host:  主机地址，如果是平台的就填写平台server，如果是设备就填写设备的地址
        :param username:  用户名
        :param password: 密码
        :param type_: device|iot|ics|star|iscada|iwos|dn4  区分平台和设备
        :param protocol: 协议，当前只支持http https
        :param port: 端口
        :param kwargs: 'device_model'
                        device_model: 设备型号，用于区分设备类型
        """
        self.protocol = protocol
        self.host = host
        self.username = username
        self.password = password
        self.headers = {}
        self.type_ = type_
        self.port = port
        self.device_model = kwargs.get('device_model').upper() if kwargs and 'device_model' in kwargs.keys() else None
        self.__login()

    def __url_pre(self, path: str):
        """host+path

        :param path:  请求路径
        :return:
        """
        if path.startswith('/'):
            return self.protocol + '://' + self.host + ':' + str(self.port) + path
        else:
            return self.protocol + '://' + self.host + ':' + str(self.port) + '/' + path

    def __login(self):
        if self.type_ in ('iot', 'ics', 'iwos', 'dn4'):
            self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
            param = {
                'client_id': '17953450251798098136',
                'client_secret': '08E9EC6793345759456CB8BAE52615F3',
                'grant_type': 'password',
                'type': 'account',
                'autoLogin': 'true',
                'password_type': 2,
                'pwdType': 'pwd',
                "username": self.username,
                "password": file_hash(self.password)}
            response = self.send_request('/oauth2/access_token', method='post', param=param).json()
            self.headers = {'Authorization': 'Bearer ' + response['access_token']}
        elif self.type_ in ('iscada', 'star'):
            settings_url = '/api/v1/erlang/frontend/settings' if self.type_ == 'iscada' else '/api/v1/frontend/settings'
            res_setting = self.send_request(settings_url, 'get', expect='result').json()
            # erlang 登录地址不一样，需要重新指向
            authority = res_setting['result']['authProvider']['authority']
            protocol_re = self.protocol
            host_re = self.host
            self.protocol = authority.split('://')[0]
            self.host = authority.split('://')[-1]
            param = {
                'client_id': res_setting['result']['authProvider']['clientId'],
                'client_secret': res_setting['result']['authProvider']['clientSecret'],
                'grant_type': 'password',
                'scope': 'offline',
                "username": self.username,
                "password": self.password,
                # "type": 'account'
            }
            response = self.send_request('/oauth2/token', method='post', param=param, params_type='form').json()
            self.headers = {'Authorization': 'Bearer ' + response['access_token']}
            self.protocol = protocol_re
            self.host = host_re
        elif self.type_ == 'device':
            username_password = '%s:%s' % (self.username, self.password)
            base_auth = base64.b64encode(username_password.encode()).decode()
            self.headers = {'Authorization': 'Basic %s' % base_auth}
            if self.device_model and self.device_model in ('ER805',):
                resp = self.send_request('/api/v1/user/login', 'post',
                                         body={'username': self.username, 'password': self.password}).json()
                self.headers['Authorization'] = 'Bearer ' + resp.get('result').get('token')
            else:
                resp = self.send_request('v1/user/login', 'post').json()
                self.headers['Authorization'] = 'Bearer ' + resp['results']['web_session']
        logging.info(f'{self.username} login success')

    def send_request(self, path, method, param=None, body=None, expect=None, file_path=None,
                     params_type='json', header=None, code=200, auth=True):
        """封装http请求，根据请求方式及参数类型自动判断使用哪些参数来发送请求

        :param path: 请求路径
        :param method: 请求方法
        :param param: 请求中的参数,
        :param body: post请求中的body，当消息体为json时使用
        :param expect: 期望包含的结果
        :param file_path: 文件路径，用于文件上传或者下载文件
        :param params_type: 参数类型，用于post请求，参数值：form|json
        :param header: 请求头 只支持字典
        :param code: 验证返回code
        :param auth: 是否认证， 默认需要的
        :return:
        """
        header = dict_merge(self.headers, header) if auth else header
        urllib3.disable_warnings()  # 去除https warnings提示
        method = method.upper()
        params_type = params_type.upper()
        url = self.__url_pre(path)
        if method == 'GET':
            res = requests.get(url=url, params=param, headers=header, verify=False)
            if file_path:
                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(res.text)
        elif method == 'POST':
            if params_type == 'FORM':
                if file_path:
                    if self.type_ == 'device':
                        files = {
                            'file': (
                                os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
                        res = requests.post(url, params=param, files=files, headers=header, verify=False)
                    else:
                        with open(file_path, 'rb') as f:
                            file_info = {"file": f}
                            res = requests.post(url, data=param, files=file_info, headers=header, verify=False)
                else:
                    res = requests.post(url=url, data=param, headers=header, verify=False)
            elif params_type == 'JSON':
                res = requests.post(url=url, params=param, json=body, headers=header, verify=False)
            else:
                res = requests.post(url=url, headers=header, verify=False)
        elif method == 'DELETE':
            if body:
                if params_type == 'JSON':
                    res = requests.delete(url, headers=header, json=body, verify=False)
                else:
                    res = requests.delete(url, headers=header, data=body, verify=False)
            else:
                res = requests.delete(url, params=param, headers=header, verify=False)
        elif method == 'PUT':
            if params_type == 'JSON':
                res = requests.put(url, json=body, params=param, headers=header, verify=False)
            else:
                res = requests.put(url, data=param, headers=header, verify=False)
        else:
            logging.exception(f"requests method {method} not support")
            raise ParameterValueError(f"requests method {method} not support")
        # logging.debug(f'Requests Method:[{method}] Code: {res.status_code} URL: {url}, Param: {param}, Body: {body}')
        if res.status_code != 401:
            if self.type_ == 'device':
                if res.status_code == 404:
                    logging.exception(f"not support API login")
                    raise Exception('not support API login')
                if res.status_code == 200 and 'login' in path:
                    if 'error' in res.json().keys():
                        logging.exception(f"UsernameOrPasswordError")
                        raise UsernameOrPasswordError
            res.encoding = 'utf-8'  # 如返回内容有中文的需要编码正确
            try:
                logging.debug(f'Requests Response json is {res.json()}')
            except Exception:
                logging.warning(f'Requests Response json is None')
        else:
            # 当token过期时，统一重新登录后再次调API
            self.__login()
            res = self.send_request(path, method, param, body, expect, file_path, params_type, header, code)
        if code:
            assert res.status_code == code, res.text
        if expect:
            if isinstance(expect, list):
                if len(expect) > 0:
                    for i in expect:
                        if isinstance(i, str) or isinstance(i, int):
                            assert str(i) in res.text, f"Response text {res.text} Does not contain {i}"
                        elif isinstance(i, dict):
                            dict_in(res.json(), i)
            elif isinstance(expect, dict):
                dict_in(res.json(), expect)
            elif isinstance(expect, str) or isinstance(expect, int):
                assert str(expect) in res.text, f"Response text {res.text} Does not contain {expect}"
            else:
                logging.exception(f'expect param type error！')
                raise ValueError('expect param type error！')
        return res


if __name__ == "__main__":
    from inhandtest.log import enable_log

    enable_log(console_level='info')
    # my.delete('test', None, )
