from decimal import Decimal

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
    cursor = conn.cursor()

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

    # 关闭游标和数据库连接
    cursor.close()
    return result


def update_table(conn, table_name, update_dict, condition):
    cursor = None
    try:
        # 创建游标
        cursor = conn.cursor()
        # 构造SET子句
        # set_clause = ", ".join([f"{col} = %s" for col, value in update_dict.items()])
        set_clause = ", ".join([f"{col} = {value}" for col, value in update_dict.items()])
        # 构造SQL语句
        sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {condition}"
        # 执行SQL语句
        # cursor.execute(sql, tuple(update_dict.values()))

        # sql = "UPDATE `tabSales Order Item` SET locked = 1 WHERE name='00086916d5'"
        cursor.execute(sql)
        # 提交更改
        conn.commit()
    # except Exception as err:
    #     print(f"Something went wrong: {err}")
    finally:
        # 关闭游标和连接
        if cursor is not None:
            cursor.close()


def _decimal_to_float(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def format_date(d):
    return d.strftime("%y-%m-%d")


def format_datetime(d):
    return d.strftime("%y-%m-%d %H:%M:%S")
