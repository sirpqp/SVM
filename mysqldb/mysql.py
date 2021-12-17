import pymysql
from pymysql.connections import Connection
from pymysql.cursors import SSDictCursor, SSCursor, DictCursor


def sql_from_dict(item: dict, table: str, filter_keys=None):
    """根据 item 生成存储的 sql 语句和 args 并返回
    自动过滤值为空的字段（不含 0 ）
    :param item: item 对象
    :param table: 表名称
    :param filter_keys: 要过滤的键
    """
    fields, args = [], []
    filter_keys = filter_keys or ()

    for k, v in item.items():
        if k in filter_keys:
            continue
        if not v and v != 0:
            continue
        fields.append(k)
        args.append(v)

    # 格式化 keys -> (k1, k2, ...)
    fields = f"(`{'`, `'.join(fields)}`)"
    values = f"({', '.join('%s' for _ in args)})"

    return f'INSERT INTO {table} {fields} VALUES {values}', args


class MySqlClient(object):
    """基本的数据库处理类
    !!! 计划弃用，请使用 gyy.models.MySQLDatabase 实例代替
    """

    def __init__(self, db_configure=None, **kwargs):
        cfg = db_configure
        kwargs.setdefault('host', cfg.get('host'))
        kwargs.setdefault('port', cfg.get('port'))
        kwargs.setdefault('user', cfg.get('user'))
        kwargs.setdefault('password', cfg.get('password'))
        kwargs.setdefault('database', cfg.get('database'))
        kwargs.setdefault('cursorclass', DictCursor)
        self.conn = pymysql.connect(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def last_insert_id(self, cur):
        return cur.lastrowid

    def cursor(self, cursor=None):
        return self.conn.cursor(cursor)

    def execute(self, query, args=None, commit=True):
        with self.conn.cursor() as c:
            try:
                c.execute(query, args=args)
                if commit:
                    self.conn.commit()
                return c
            except:
                self.conn.rollback()
                raise

    def executemany(self, query, args, commit=True):
        with self.conn.cursor() as c:
            try:
                c.executemany(query, args=args)
                if commit:
                    self.conn.commit()
                return c
            except:
                self.conn.rollback()
                raise

    def runquery(self, query, args=None):
        with self.conn.cursor() as c:
            c.execute(query, args)
            return c.fetchall()

    def save_item(self, item: dict, table, filter_keys=None, commit=True):
        query, args = sql_from_dict(item, table, filter_keys)
        return self.execute(query, args=args, commit=commit)

    def close(self):
        self.conn.close()

