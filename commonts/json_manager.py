# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:03
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : json_manager.py
# @Software: PyCharm
import json
import base64
from loguru import logger
import os


class JsonManager:

    def __init__(self, dir_path: str = 'json_db'):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.dir_path = dir_path

    def save_file(self, data, filename):
        try:
            json_str = json.dumps(data)
            encoded_data = base64.b64encode(json_str.encode()).decode()
            with open(f'{self.dir_path}/{filename}.b64', 'w', encoding='utf-8') as file:
                file.write(encoded_data)
        except Exception as e:
            print(e)
            logger.error(f'save json file {filename} error')

    def read_file(self, filename):
        file_path = f'{self.dir_path}/{filename}.b64'
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as file:
            encoded_data = file.read()
        decoded_data = base64.b64decode(encoded_data.encode()).decode()
        json_data = json.loads(decoded_data)
        return json_data


json_manager = JsonManager()
