# 申请信息结构类
import json
import os

import requests

from . import *


class Result():
    def __init__(self):
        self.record_id = 0
        self.website_url = ''
        self.status = 0
        self.error_code = ''
        self.message = ''
        self.apply_params = ''
        self.result_data = ''
        self.created_ip = ''

    def to_json(self):
        return vars(self)


class Apply:
    data = {}

    def toJson(self):
        return self.data

    def set_data(self, data):
        self.data = data

class RequestApply(ApiRequest):

    def handler_result(self,data):
        for group in data['group_info']:
            component_dict = {}
            for component in group['components']:
                component_dict[component['key']] = component
            group['components'] = component_dict
        return data

    # 获取申请信息
    def get_apply(self, record_id: int) -> Apply:
        url = os.getenv("apply_info")
        apply = Apply()
        try:
            res = requests.get(url, params={'record_id': record_id})
            res.raise_for_status()
            result = res.json()
            if result['error_code'] != 0:
                raise requests.exceptions.RequestException()
            data = result['data']
            data = self.handler_result(data)
            apply.set_data(data)
            apply = toObject(apply, data)
        except requests.exceptions.RequestException as e:
            raise Exception("获取申请信息失败")
        return apply

    # 最后提交申请结果
    def post_result(self, info: Result):
        url = os.getenv("apply_result")
        try:
            res = requests.post(url, json=json.dumps(info.to_json()))
            res.raise_for_status()
            result = res.json()
            return result
        except requests.exceptions.RequestException as e:
            raise Exception("提交申请结果失败")
