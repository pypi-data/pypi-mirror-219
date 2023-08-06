import pymysql
from twisted.internet.threads import deferToThread


class MySQLPipeline:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def _has_dict_item(self, table, item):
        where_strs = f"`unique_identity` = %s and `{item.unique_key}` = %s"
        where_value_list = [item.unique_identity, item.get(item.unique_key)]
        query = 'select %s from %s where %s' % (item.unique_key, table, where_strs)

        self.cursor.execute(query, tuple(where_value_list))
        rows = self.cursor.fetchone()

        if rows:
            return True
        else:
            return False

    def _insert_dict_item(self, table, item):
        data = dict(item)
        keys = ', '.join(f'`{data.keys()}`')
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

    def _update_dict_item(self, table, item):
        data = dict(item)
        set_strs = []
        set_values = []

        for param, value in data.items():
            set_strs.append(f'`{param}` = %s')
            set_values.append(value)

        where_strs = f"`unique_identity` = %s and `{item.unique_key}` = %s"
        where_value_list = [item.unique_identity, data.get(item.unique_key)]

        set_str = ', '.join(set_strs)
        sql = "update %s set %s where %s" % (table, set_str, where_strs)
        self.cursor.execute(sql, tuple(data.values()) + tuple(where_value_list))
        self.db.commit()

    def _process_item(self, item, spider):
        allowed_spiders = item.mysql_spiders
        allowed_tables = item.mysql_tables
        if allowed_spiders and spider.name in allowed_spiders:
            for allowed_table in allowed_tables:
                if item.unique_key and item.unique_identity:
                    if self._has_dict_item(allowed_table, item):
                        self._update_dict_item(allowed_table, item)
                    else:
                        self._insert_dict_item(allowed_table, item)
                else:
                    self._insert_dict_item(allowed_table, item)
        return item

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
