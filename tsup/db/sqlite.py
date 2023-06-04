# -*- coding: utf-8 -*-
"""
Created on 2016-11-16 16:25
---------
@summary: 操作SQLite数据库
---------
@author: Boris
@email: boris_liu@foxmail.com

@chatgpt
prompt:
converted Python script that uses SQLite instead of MySQL:
"""
import datetime
import json
from typing import List, Dict

import sqlite3

import tsup.setting as setting
from tsup.utils.log import log
from tsup.utils.tools import make_insert_sqlite, make_batch_sqlite, make_update_sqlite


def auto_retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except sqlite3.InterfaceError as e:
                log.error(
                    """
                    error:%s
                    sql:  %s
                    """
                    % (e, kwargs.get("sql") or args[1])
                )

    return wrapper


class SqliteDB:
    def __init__(self, db_path=None, **kwargs):
        if not db_path:
            db_path = setting.SQLITE_DB_PATH

        try:
            self.conn = sqlite3.connect(db_path, **kwargs)
            self.cursor = self.conn.cursor()
        except Exception as e:
            log.error(f"连接失败：db_path: {db_path}, exception: {e}")
        else:
            log.debug(f"连接到SQLite数据库: {db_path}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def find(self, sql, limit=0, to_json=False, convert_col=True):
        self.cursor.execute(sql)

        if limit == 1:
            result = self.cursor.fetchone()
        elif limit > 1:
            result = self.cursor.fetchmany(limit)
        else:
            result = self.cursor.fetchall()

        if to_json:
            columns = [col[0] for col in self.cursor.description]

            def convert(col):
                if isinstance(col, (datetime.date, datetime.time)):
                    return str(col)
                elif isinstance(col, str) and (
                    col.startswith("{") or col.startswith("[")
                ):
                    try:
                        return json.loads(col)
                    except:
                        return col
                else:
                    return col

            if limit == 1:
                if convert_col:
                    result = [convert(col) for col in result]
                result = dict(zip(columns, result))
            else:
                if convert_col:
                    result = [[convert(col) for col in row] for row in result]
                result = [dict(zip(columns, row)) for row in result]

        return result

    def add(self, sql, exception_callfunc=None):
        affect_count = None

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            affect_count = self.cursor.rowcount
        except Exception as e:
            log.error(f"error:{e}\nsql: {sql}")
            if exception_callfunc:
                exception_callfunc(e)

        return affect_count

    def add_smart(self, table, data: Dict, **kwargs):
        sql = make_insert_sql(table, data, **kwargs)
        return self.add(sql)

    def add_batch(self, sql, datas: List[List]):
        affect_count = None

        try:
            self.cursor.executemany(sql, datas)
            self.conn.commit()
            affect_count = self.cursor.rowcount
        except Exception as e:
            log.error(f"error:{e}\nsql: {sql}")

        return affect_count

    def add_batch_smart(self, table, datas: List[Dict], **kwargs):
        sql, datas = make_batch_sql(table, datas, **kwargs)
        return self.add_batch(sql, datas)

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            log.error(f"error:{e}\nsql: {sql}")
            return False
        else:
            return True

    def update_smart(self, table, data: Dict, condition):
        sql = make_update_sql(table, data, condition)
        return self.update(sql)

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            log.error(f"error:{e}\nsql: {sql}")
            return False
        else:
            return True

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            log.error(f"error:{e}\nsql: {sql}")
            return False
        else:
            return True
