#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :base_model.py
# @Time :2024/12/23 16:30
# @Author :Jiamid
from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    code: int = Field(default=0)
    msg: str = Field(default='success')
    data: None = Field(default=None)
