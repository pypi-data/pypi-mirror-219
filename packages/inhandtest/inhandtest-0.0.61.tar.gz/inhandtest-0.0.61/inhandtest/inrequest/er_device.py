# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 18:26:55
# @Author  : Pane Li
# @File    : er_device.py
"""
er_device

"""
import random
import re
import time
from typing import List
from inhandtest.inrequest.er_default_config import *
from inhandtest.inrequest.inrequest import *
from inhandtest.exception import ResourceNotFoundError


class ErRequest(InRequest):

    def send_request(self, path, method, param=None, body=None, expect=None, file_path=None,
                     params_type='json', header=None, code=200, auth=True):
        def switch_config(in_payload: dict) -> dict:
            """转换配置，当配置中的key是随机id时， 可使用$id, 然后该函数会自动替换成随机id并返回

            :param in_payload: 需要修正的配置项，其中需要更新的key 使用$id来替换
            :return:
            """

            def _uuid():
                def _random():
                    result = hex(random.randint(0, 16 ** 4)).replace('0x', '')
                    if len(result) < 4:
                        result = '0' * (4 - len(result)) + result
                    return result

                return '0' + _random()[1:] + hex(int(time.time())).replace('0x', '') + _random()

            in_payload = str(in_payload)
            for i in range(0, len(re.findall('\$id', in_payload))):
                in_payload = in_payload.replace('$id', _uuid(), 1)
            return eval(in_payload)

        body = switch_config(body) if body else body
        return super().send_request(path, method, param, body, expect, file_path, params_type, header, code, auth)


class ErDevice:
    def __init__(self, username, password, host, protocol='https', port='443', model='ER805'):
        """
        :param username: 设备用户名
        :param password: 设备密码
        :param protocol: http|https
        :param host: 设备IP
        :param model: 设备型号, 默认ER805
        """
        self.username = username
        self.password = password
        self.protocol = protocol
        self.host = host
        self.port = port
        self.model = model
        self.api = ErRequest(host=self.host, username=self.username, password=self.password, type_='device',
                             protocol=self.protocol, port=self.port, device_model=self.model)
        self.default_config = {'ER805': er805_default_config}.get(self.model)

    @property
    def path(self) -> dict:
        """
        :return: 返回设备的url
        """
        return {'ER805': {'import_firmware': '/api/v1/import/firmware',
                          'import_config': '/api/v1/config/import',
                          'upgrade_config': '/api/v1/config/update',
                          'upgrade_firmware': '/api/v1/upgrade',
                          'config_backup': '/api/v1/config/backup',
                          'config_url': '/api/v1/config',
                          'status_url': '/api/v1/status/',
                          'login': '/api/v1/user/login',
                          'basic': '/api/v1/basic',
                          'diagnose': '/api/v1/diagnose',
                          'download': '/api/v1/syslog/download',
                          'events_url': '/api/v1/events/get'}}.get(self.model)

    def _get_config(self, fields: str):
        """

        :param fields: cellular| wlan_ap| lan| static_route4| uplink| wan| admin| system| ntp| data_usage| record| alerts|
                         ipsec| email| ippt| l2tp| link_quality| uplink| dhcp| admin_access| firewall| policy_route| qos|
                         port_mapping| wlan_sta| switch_port| mac_filter
                         可根据配置层级使用.来获取，例'cellular.modem'，
                         也可使用逗号分隔获取多个配置项，例'wlan_ap,lan,wlan_sta'
        """
        return self.api.send_request(self.path.get('config_url'), method='get',
                                     param={'fields': fields}).json()['result']['config']

    def get_uuid_config(self, fields: str, condition: dict) -> List or None:
        """根据条件返回当前配置的uuid


        :param fields: cellular| wlan_ap| lan| static_route4| uplink| wan| admin| system| ntp| data_usage| record| alerts|
                         ipsec| email| ippt| l2tp| link_quality| uplink| dhcp| admin_access| firewall| policy_route| qos|
                         port_mapping| wlan_sta| switch_port
                         可根据配置层级使用.来获取，例'cellular.modem'，不可获取多个配置项
                         传参时需写到uuid前一级
        :param condition: 查找uuid的条件，以字典形式传入，注意匹配大小写并保证key和value的值需完全匹配
                            例当需要查找ssid=test且band=2.4G的wifi时可传入{'ssid': 'test', 'band': '2.4G'}
                例当需要匹配qos中interface=wan1的uuid时
                         "qos": {"uplink_rules":
                         {"0000f0804da7846f": {
                         "interface": "wan1",
                         "egress_rate": "0Mbps",
                         "ingress_rate": "0Mbps"}
                         fields传参为'qos.uplink_rules'，condition传参为{'interface': 'wan1'}
        :return: 如存在uuid则返回uuid及匹配的config，否则返回None
        """
        config = self._get_config(fields)
        con = (fields, condition)
        try:
            for k in con[0].split('.'):
                config = config.get(k)
            for uuid_, v in config.items():
                for ex_k, ex_v in con[1].items():
                    if v.get(ex_k) != ex_v:
                        break
                else:
                    id_ = uuid_
                    config_ = v
                    break
            else:
                raise ResourceNotFoundError('not find uuid, please check the condition')
        except Exception:
            raise ResourceNotFoundError('not find key, please check the fields')
        logging.info(f'find the matched uuid: {id_}')
        return [id_, config_]

    def wifi_ap(self, ssid: str, band: str, action: str, **kwargs):
        """编辑wifi ap

        :param ssid: 编辑和删除时填入操作前的ssid, 添加时填入新的ssid
        :param band: '2.4g'| '5g' 频段 编辑和删除时填入操作前的频段, 添加时填入新的频段
        :param action: 'edit'| 'add'| 'delete' 编辑\添加\删除, 添加和删除只对副wifi有效
        :param kwargs: ssid|enabled|auth|key|encrypt|ap_isolate|vlan|channel
                        new_ssid: 新的ssid, 添加和删除时不需要填写
                        enabled: True| False 启用或者禁用
                        key: 密码, 添加ap时密码为必填项, 8-63 characters,support letters, numbers, special characters
                        auth: 'WPA2-PSK'|'OPEN'|'WPA-PSK'|'WPA-PSK/WPA2-PSK' 安全方式,只支持大写
                        encrypt: 'CCMP'|'CCMP/TKIP' 加密方式,只支持大写
                        vlan: int, 默认为1
                        channel: 信道，只能在主wifi中编辑 'Auto'或数字
                        ap_isolate: True| False 启用或者禁用
        :return:
        """
        wlan_ap = self._get_config('wlan_ap').get('wlan_ap')
        band = band.upper()
        is_primary = False
        body = {}
        if kwargs.get('new_ssid'):
            kwargs.update({'ssid': kwargs.pop('new_ssid')})
        if action in ('edit', 'delete'):
            try:
                config_ap = self.get_uuid_config('wlan_ap', {'ssid': ssid, 'band': band})
                if config_ap[1].get('channel'):
                    is_primary = True
                if action == 'edit':
                    config_ap[1].update(kwargs)
                    body = {'wlan_ap': {config_ap[0]: config_ap[1]}}
                elif action == 'delete':
                    config_ap[1] = None
                    body = {'wlan_ap': {config_ap[0]: config_ap[1]}}
                    if is_primary:
                        raise ParameterValueError('the primary wifi can not be deleted')
                else:
                    pass
            except Exception:
                raise ParameterValueError(f'the ssid:{ssid} and band:{band} is not exist')
        else:
            # 添加时先获取已有ap的name
            list_2_4 = [v.get('name') for k, v in wlan_ap.items() if 'wlan1' in v.get('name')]
            list_5 = [v.get('name') for k, v in wlan_ap.items() if 'wlan2' in v.get('name')]
            try:
                if band == '2.4G':
                    name = [un_name for un_name in ('wlan1.1', 'wlan1.2', 'wlan1.3') if un_name not in list_2_4][0]
                else:
                    name = [un_name for un_name in ('wlan2.1', 'wlan2.2', 'wlan2.3') if un_name not in list_5][0]
            except IndexError:
                raise ParameterValueError(f'the {band} wifi is full')
            config_ap = self.default_config.get('wlan_ap').get(band)
            config_ap.update(kwargs)
            config_ap.update({'ssid': ssid, 'band': band, 'name': name})
            body = {'wlan_ap': {'$id': config_ap}}
        self.api.send_request(self.path.get('config_url'), method='put', body=body,
                              expect={'result': 'ok'})
        logging.info(f'{action} wifi {band} {ssid}  ap success')

    def config_wan(self, interface='wan1', status='enable', **kwargs):
        """
        :param interface: 'wan1'|'wan2'
        :param status: 'enable'|'disable'|'delete'
        :kwargs: dict
                nat: True| False
                mtu: int
                ipv4:
                    dhcpc: True | False
                    ip: str
                    prefix_len: int, 0-32, 掩码长度
                    gateway: str
                    dns1: str
                    dns2: str
                pppoe:
                    enabled: True| False
                    username: str
                    password: str
                    local_ip: str
                    remote_ip: str
        """
        try:
            config_wan = self.get_uuid_config('wan', {'name': interface})
        except ResourceNotFoundError:
            config_wan = ['$id', self.default_config.get('wan').get(interface)]
        if status == 'enable':
            kwargs.update({'enabled': True})
            if kwargs.get('ipv4'):  # 改为ipv4时  清除原来的pppoe配置
                kwargs.update({'pppoe': {'enabled': False}})
            config_wan[1].update(kwargs)
            body = {'wan': {config_wan[0]: config_wan[1]}}
        elif status in ('disable', 'delete'):
            if config_wan[0] == '$id':
                raise ParameterValueError(f'wan {interface} is not exist')
            else:
                if status == 'disable':
                    body = {'wan': {config_wan[0]: {'enabled': False}}}
                else:
                    body = {'wan': {config_wan[0]: None}}
        else:
            raise ParameterValueError(f'status:{status} is not support')
        self.api.send_request(self.path.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{status} wan {interface} success')

    def config_wifi_sta(self, status='enable', **kwargs):
        """编辑wifi_sta
        :param status: 'edit'|'add'|'delete'
        :param kwargs: ssid| auth| encrypt| key| mtu| encrypt| band| enabled|type_| ip| mask| gateway| dns1| dns2
                        ssid: str
                        auth: 'OPEN'|'WPA-PSK'|'WPA2-PSK'|'WPAWPA2-PSK'
                        key: str, 密码
                        encrypt: 'CCMP'|'CCMP-TKIP'
                        mtu: int
                        band: '2.4G'|'5G'
                        enabled: True| False
                        type_: 'static'| 'dhcp'
                        ip: str
                        mask: str
                        gateway: str
                        dns1: str
                        dns2: str
        :param status: 'enable'|'disable'|'delete'
        :param kwargs: dict
                    band: '2.4G'|'5G'
                    ssid: str
                    mtu: int
                    nat: True| False
                    auth: 'OPEN'|'WPA-PSK'|'WPA2-PSK'|'WPAWPA2-PSK'
                    encrypt: 'CCMP'|'CCMP-TKIP'
                    key: str, 密码
                    ipv4:
                        dhcpc: True | False
                        ip: str
                        prefix_len: int, 0-32, 掩码长度
                        gateway: str
                        dns1: str
                        dns2: str
        """
        config_wlan = ['wlan_sta', self._get_config('wlan_sta').get('wlan_sta')] if self._get_config('wlan_sta').get(
            'wlan_sta') else ['$id', self.default_config.get('wlan_sta')]
        if status == 'enable':
            kwargs.update({'enabled': True})
            config_wlan[1].update(kwargs)
            body = {config_wlan[0].replace('$id', 'wlan_sta'): config_wlan[1]}
        elif status in ('disable', 'delete'):
            if config_wlan[0] == '$id':
                raise ParameterValueError(f'wlan_sta is not exist')
            else:
                if status == 'disable':
                    body = {config_wlan[0].replace('$id', 'wlan_sta'): {'enabled': False}}
                else:
                    body = {config_wlan[0].replace('$id', 'wlan_sta'): None}
        else:
            raise ParameterValueError(f'status:{status} is not support')
        self.api.send_request(self.path.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{status} wlan_ap success')

    def mac_filter(self, mac: str = None, action: str = None, **kwargs):
        """编辑mac地址过滤

        :param mac: str, 新增和删除时必填, 只变更过滤模式可为None
        :param action: 'edit'|'add'|'delete', 只变更过滤模式可为None
        :param kwargs: new_mac| action| mode| desc
                        mac_new: str, 编辑时填入新的mac地址,新增和删除时不填
                        mode: 'none'|'blacklist'| 'whitelist', 过滤模式, 无限制|黑名单|白名单, 支持只变更过滤模式,
                        desc: str, 描述
        """
        body = {}
        if mac and action and action in ('edit', 'delete'):
            config_mac_filter = self.get_uuid_config('mac_filter.mac_list', {'mac': mac})
            if action == 'edit':
                info = {'mac': kwargs.get('new_mac') if kwargs.get('new_mac') else '',
                        'desc': kwargs.get('desc') if kwargs.get('desc') else ''}
                config_mac_filter[1].update(info)
                body = {'mac_filter': {'mac_list': {config_mac_filter[0]: config_mac_filter[1]}}}
            elif mac and action and action == 'delete':
                config_mac_filter[1] = None
                body = {'mac_filter': {'mac_list': {config_mac_filter[0]: config_mac_filter[1]}}}
            else:
                raise ParameterValueError(f'action:{action} is not support')
        else:
            if mac and action and action == 'add':
                config_mac_filter = {'mac': mac, 'desc': kwargs.get('desc') if kwargs.get('desc') else ''}
                body = {'mac_filter': {'mac_list': {'$id': config_mac_filter}}}
        if 'mode' in kwargs.keys():
            if body:
                body.get('mac_filter').update({'mode': kwargs.get('mode')})
                action = 'change_mode'
            else:
                body = {'mac_filter': {'mode': kwargs.get('mode')}}
        self.api.send_request(self.path.get('config_url'), method='put', body=body,
                              expect={'result': 'ok'})
        logging.info(f'{action} mac_filter success')


if __name__ == '__main__':
    from inhandtest.log import enable_log
    enable_log(console_level='debug')
