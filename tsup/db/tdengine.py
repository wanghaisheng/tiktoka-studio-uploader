# -*- coding: utf-8 -*-
"""
Created on 2016-11-16 16:25
---------
@summary: 操作SQLite数据库
---------
@author: Boris
@email: boris_liu@foxmail.com

@adapter from mysql version using chatgpt
prompt:
converted Python script that uses tdengine instead of MySQL:
"""
import datetime
import json
from typing import List, Dict

from taos import Connection
from taos.cursor import Cursor

import tsup.setting as setting
from tsup.utils.log import log
from tsup.utils.tools import make_insert_sql, make_batch_sql, make_update_sql


def auto_retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error(
                    """
                    error:%s
                    sql:  %s
                    """
                    % (e, kwargs.get("sql") or args[1])
                )

    return wrapper


class TDengineDB:
    def __init__(
        self, ip=None, port=None, db=None, user_name=None, user_pass=None, **kwargs
    ):
        if not ip:
            ip = setting.TDENGINE_IP
        if not port:
            port = setting.TDENGINE_PORT
        if not db:
            db = setting.TDENGINE_DB
        if not user_name:
            user_name = setting.TDENGINE_USER_NAME
        if not user_pass:
            user_pass = setting.TDENGINE_USER_PASS

        self.connection = Connection(
            host=ip,
            port=port,
            user=user_name,
            password=user_pass,
            database=db,
            **kwargs,
        )

        log.debug("连接到TDengine数据库 %s : %s" % (ip, db))

    @staticmethod
    def unescape_string(value):
        if not isinstance(value, str):
            return value

        value = value.replace("\\0", "\0")
        value = value.replace("\\\\", "\\")
        value = value.replace("\\n", "\n")
        value = value.replace("\\r", "\r")
        value = value.replace("\\Z", "\032")
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")

        return value

    def size_of_connections(self):
        return 1

    def size_of_connect_pool(self):
        return 1

    @auto_retry
    def find(self, sql, limit=0, to_json=False, convert_col=True):
        cursor = self.connection.cursor()

        cursor.execute(sql)

        if limit == 1:
            result = cursor.fetchone()
        elif limit > 1:
            result = cursor.fetchmany(limit)
        else:
            result = cursor.fetchall()

        if to_json:
            columns = [i[0] for i in cursor.description]

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
                result = [dict(zip(columns, r)) for r in result]

        cursor.close()

        return result

    def add(self, sql, exception_callfunc=None):
        affect_count = None
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            affect_count = cursor.rowcount

        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
                """
                % (e, sql)
            )
            if exception_callfunc:
                exception_callfunc(e)
        finally:
            if cursor:
                cursor.close()

        return affect_count

    def add_smart(self, table, data: Dict, **kwargs):
        sql = make_insert_sql(table, data, **kwargs)
        return self.add(sql)

    def add_batch(self, sql, datas: List[List]):
        affect_count = None
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql, datas)
            self.connection.commit()
            affect_count = cursor.rowcount

        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
                """
                % (e, sql)
            )
        finally:
            if cursor:
                cursor.close()

        return affect_count

    def add_batch_smart(self, table, datas: List[Dict], **kwargs):
        sql, datas = make_batch_sql(table, datas, **kwargs)
        return self.add_batch(sql, datas)

    def update(self, sql):
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            return False
        else:
            return True
        finally:
            if cursor:
                cursor.close()

    def update_smart(self, table, data: Dict, condition):
        sql = make_update_sql(table, data, condition)
        return self.update(sql)

    def delete(self, sql):
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            return False
        else:
            return True
        finally:
            if cursor:
                cursor.close()

    def execute(self, sql):
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            return False
        else:
            return True
        finally:
            if cursor:
                cursor.close()


# import json
# import datetime
# import re
# from tdengine import TDengineConnection


# # Create a TDengine connection
# conn = TDengineConnection(
#     host="your_host", port=6030, username="your_username", password="your_password"
# )

# # Example usage
# data = {"id": 1, "name": "John Doe", "age": 30}
# make_insert_tdengine(conn, "my_table", data)

# conn.close()
