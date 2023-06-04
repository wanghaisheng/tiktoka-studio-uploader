# -*- coding: utf-8 -*-
"""
Created on 2016-11-16 16:25
---------
@summary: 操作Excel
---------
"""

import datetime
import json
from typing import List, Dict

import pandas as pd


class ExcelDB:
    def __init__(self, file_path=None, sheet_name=None, **kwargs):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def find(self, condition=None, limit=None, to_json=False, convert_col=True):
        """
        @summary:
        无数据： 返回()
        有数据： 若limit == 1 则返回 (data1, data2)
                否则返回 ((data1, data2),)
        ---------
        @param condition: 查询条件
        @param limit: 查询数量限制
        @param to_json: 是否将查询结果转为json
        @param convert_col: 是否处理查询结果，如date类型转字符串，json字符串转成json。仅当to_json=True时生效
        ---------
        @result:
        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

        if condition:
            df = df.query(condition)

        if limit:
            df = df.head(limit)

        if to_json:
            result = df.to_json(orient="records")

            if convert_col:
                result = json.loads(result)

            return result

        return df

    def add(self, data: Dict):
        """
        添加数据
        Args:
            data: 字典 {"xxx":"xxx"}

        Returns: 添加行数

        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        df = df.append(data, ignore_index=True)
        df.to_excel(self.file_path, sheet_name=self.sheet_name, index=False)

        return 1

    def update(self, condition, data: Dict):
        """
        更新数据
        Args:
            condition: 更新条件
            data: 数据 {"xxx":"xxx"}

        Returns: True / False

        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        df.loc[df.query(condition).index, data.keys()] = data.values()
        df.to_excel(self.file_path, sheet_name=self.sheet_name, index=False)

        return True

    def delete(self, condition):
        """
        删除数据
        Args:
            condition: 删除条件

        Returns: True / False

        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        df = df.drop(df.query(condition).index)
        df.to_excel(self.file_path, sheet_name=self.sheet_name, index=False)

        return True
