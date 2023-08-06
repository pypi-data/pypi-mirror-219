from typing import Tuple, List

from playhouse.pool import PooledMySQLDatabase


# 定义数据库连接池
def manual_connect(database, user, password, host, port=3306, max_connections=8, stale_timeout=300, **kwargs):
    return PooledMySQLDatabase(
        database,
        user=user,
        password=password,
        host=host,
        port=port,
        max_connections=max_connections,
        stale_timeout=stale_timeout,
        **kwargs
    )


def init_config(database, user, password, host, port=3306):
    return {
        "database": database,
        # "engine": "peewee.MySQLDatabase",
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "charset": "utf8",
    }


# 定义通用增删改查函数
def create_record(db, model_class, **kwargs):
    with db.connection_context():
        with db.atomic():
            record = model_class.create(**kwargs)
            return record.id


def update_record(db, model_class, record_id, **kwargs):
    with db.connection_context():
        with db.atomic():
            query = model_class.update(**kwargs).where(model_class.id == record_id)
            return query.execute()


def delete_record(db, model_class, record_id):
    with db.connection_context():
        with db.atomic():
            query = model_class.delete().where(model_class.id == record_id)
            return query.execute()


def get_records(db, model_class, select_fields: Tuple = None, order_by=None, **where):
    """
    从mysql查询多条记录
    :param db:
    :param model_class:
    :param select_fields: 要查询的列名，默认查询所有。tuple类型，如: (User.name, User.email)
    :param order_by: 排序的根据。tuple类型，如: (User.name, User.email)
    :param where: 筛选条件，可以逐个传key=value的形式，如: User.name='a', User.email='b@example.com'
    :return:
    """
    with db.connection_context():
        with db.atomic():
            if select_fields is None:
                select_fields = tuple()
            query = model_class.select(*select_fields)
            for key, value in where.items():
                query = query.where(getattr(model_class, key) == value)
            if order_by is not None:
                query = query.order_by(*order_by)
            return list(query)


def get_first_record(db, model_class, select_fields=None, order_by=None, **where):
    records = get_records(db, model_class, select_fields, order_by, **where)
    if records is None or len(records) == 0:
        return None
    return records[0]
