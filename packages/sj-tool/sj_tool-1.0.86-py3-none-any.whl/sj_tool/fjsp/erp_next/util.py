from decimal import Decimal
from typing import Tuple, List

import pymysql


def get_http_header():
    return {"Authorization": "token b35823535ff6d52:55fa707ca16e4c5"}


# 连接到MySQL数据库
def connect_erp_db():
    return pymysql.connect(host="192.168.50.73", user="root", password="123", database="_b396709c7d7b26c3")


def select_data_from_table(
    conn, table_name, columns="*", where_clause=None, where_params=None, to_dict=False, dict_key=None
):
    # 创建一个游标对象
    with conn.cursor() as cursor:
        column_str = str(columns)[1:-1].replace("'", "`") if columns != "*" else "*"

        # 执行查询语句
        query = f"SELECT {column_str} FROM `{table_name}`"
        if where_clause is not None:
            query += "  WHERE  " + where_clause
            cursor.execute(query, where_params)
        else:
            cursor.execute(query)

        if columns == "*":
            columns = [column[0] for column in cursor.description]

        # 获取查询结果
        query_result = cursor.fetchall()

        # 根据父表键来构建，方便直接使用
        if to_dict and dict_key is not None:
            result = {}
            for row in query_result:
                # 创建字典并与列名配对
                row_dict = {columns[i]: _decimal_to_float(value) for i, value in enumerate(row)}
                if row_dict[dict_key] not in result:
                    result[row_dict[dict_key]] = [row_dict]
                else:
                    result[row_dict[dict_key]].append(row_dict)
        else:
            result = []
            # 遍历结果
            for row in query_result:
                # 创建字典并与列名配对
                row_dict = {columns[i]: _decimal_to_float(value) for i, value in enumerate(row)}
                result.append(row_dict)
    return result


def update_table_record(conn, table_name, update_dict, condition):
    with conn.cursor() as cursor:
        # 构造SET子句
        set_clause = ", ".join([f"{col} = {value}" for col, value in update_dict.items()])
        # 构造SQL语句
        sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {condition}"

        # sql = "UPDATE `tabSales Order Item` SET locked = 1 WHERE name='00086916d5'"
        cursor.execute(sql)
        # 提交更改
        conn.commit()


def insert_table_records(conn, table_name, data: List[Tuple]):
    """
    往数据库插入多条记录
    :param conn:
    :param table_name: 表名
    :param data: 多条记录
    :return:
    """
    with conn.cursor() as cursor:
        for item in data:
            # 从字典中提取字段名和值
            keys = item.keys()
            values = item.values()

            # 创建一个新的记录
            sql = "INSERT INTO `{}` ({}) VALUES ({})".format(
                table_name, ", ".join(keys), ", ".join(["%s"] * len(values))
            )
            cursor.execute(sql, tuple(values))

    # 数据库连接对象表示了一个工作单元，任何从数据库获取的数据必须在一个事务中读取和修改。
    conn.commit()


def _decimal_to_float(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def format_date(d):
    return d.strftime("%y-%m-%d")


def format_datetime(d):
    return d.strftime("%y-%m-%d %H:%M:%S")
