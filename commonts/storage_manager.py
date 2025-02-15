# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:27
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : storage_manager.py
# @Software: PyCharm
import json
import datetime
import base64
from loguru import logger
import os


class StorageManager:

    def __init__(self, filename: str, default_data: dict, dir_path: str = 'b64_db'):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.file_path = f'{dir_path}/{filename}.b64'
        self.data: dict = self.read_file()
        if not self.data:
            self.data = default_data
            self.save_file()

    def reset_data(self):
        self.data = {}
        self.save_file()

    def get_value(self, key, default):
        return self.data.get(key, default)

    def del_key(self, key):
        try:
            del self.data[key]
            self.save_file()
        except Exception as e:
            logger.error(f'del {key} error {e}')

    def set_value(self, key, value, save=True):
        self.data[key] = value
        if save: self.save_file()

    def add_to_key(self, key, value):
        key_list = self.data.get(key, [])
        if value not in key_list:
            key_list.append(value)
        self.set_value(key, key_list)
        logger.info(f'add {value} {key}: {key_list}')

    def del_from_key(self, key, value):
        key_list = self.data.get(key, [])
        if value in key_list:
            key_list.remove(value)
        self.set_value(key, key_list)
        logger.info(f'del {value} {key}: {key_list}')

    def save_file(self):
        try:
            # 将 JSON 数据转为字符串
            json_str = json.dumps(self.data)
            # 将字符串进行 base64 编码
            encoded_data = base64.b64encode(json_str.encode()).decode()
            # 写入文件
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(encoded_data)
        except Exception as e:
            print(e)
            logger.error('save_file error')

    def read_file(self):
        if not os.path.exists(self.file_path):
            return {}
        # 从文件读取 base64 编码的数据
        with open(self.file_path, 'r', encoding='utf-8') as file:
            encoded_data = file.read()
        # 进行 base64 解码
        decoded_data = base64.b64decode(encoded_data.encode()).decode()
        # 将解码后的字符串转回 JSON
        json_data = json.loads(decoded_data)
        return json_data


timer_task_storage = StorageManager('timer_task', {
    'chat_ids': [],
    'wallets': []
})

