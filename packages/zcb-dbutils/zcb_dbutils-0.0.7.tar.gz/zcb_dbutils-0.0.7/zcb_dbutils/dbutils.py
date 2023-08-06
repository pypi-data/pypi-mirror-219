# -*- coding: utf-8 -*-
# @Author: zhangcb
# @Date:   2020-03-31 09:10:04
# @Last Modified by:   zhangcb
# @Last Modified time: 2020-03-31 10:26:03

import pymysql
import logging


class DBConnection:

    def __init__(self, host, port, user, password, database, charset='utf8'):
        self.database = database
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def exec_sql_file(self, file):
        fd = open(file, 'r', encoding='utf-8')
        sql = fd.read()
        fd.close()
        sqlCommands = sql.split(";\n")

        for command in sqlCommands:
            try:
                self.cursor.execute(command)
                self.conn.commit()
            except Exception as e:
                logging.info(e, exc_info=True, stack_info=True)
                return False
        return True

    def insert(self, sql, args=None):
        """
        插入一条，返回自增ID
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.lastrowid
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def update(self, sql, args=None):
        """
        更新，返回影响行数
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.rowcount
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def delete(self, sql, args=None):
        """
        删除，返回影响行数
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.rowcount
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def exec_sql(self, command):
        """
        执行一条语句语句
        :param command:
        :return:
        """
        try:
            self.cursor.execute(command)
            return True
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return False

    def batch_exec(self, command, args=[]):
        """
        批量执行，依赖args的数量
        :param args:
        :param command:
        :return:
        """
        try:
            self.cursor.executemany(command, args)
            return True
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return False

    def fetch_one(self, sql, args=None):
        """
        查询一行数据，如果有多个结果，也只取第一行
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def fetch_list(self, sql, args=None):
        """
        查询结果为二维数组
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            ret = []
            for item in result:
                values = list(item.values())
                ret.append(values)
            return ret
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def fetch_column_by_index(self, sql, args=None, index=0):
        """
        查询结果取第index个字段的值，返回数组
        :param sql:
        :param args:
        :param index:
        :return:
        """
        try:
            r = self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            ret = []
            for item in result:
                values = list(item.values())
                ret.append(values[index])
            return ret
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
            return None

    def fetch_rows(self, sql, args=None):
        """
        查询对象数组的结果
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logging.info(e, exc_info=True, stack_info=True)
        return None

    def showtable(self, database, table_name):
        """
        获取表创建的信息，返回对象数组 [{'field':'字段名称','type_name':'字段类型 varchar, bigint','comment':'字段说明','type':'字段类型全称 varchar(32)'}]
        :param database:
        :param table_name:
        :return:
        """
        with self.conn.cursor() as cursor:
            sqllist = '''
                    select aa.COLUMN_NAME,
                    aa.DATA_TYPE,aa.COLUMN_COMMENT, cc.TABLE_COMMENT, aa.COLUMN_TYPE
                    from information_schema.`COLUMNS` aa LEFT JOIN 
                    (select DISTINCT bb.TABLE_SCHEMA,bb.TABLE_NAME,bb.TABLE_COMMENT 
                    from information_schema.`TABLES` bb ) cc  
                    ON (aa.TABLE_SCHEMA=cc.TABLE_SCHEMA and aa.TABLE_NAME = cc.TABLE_NAME )
                    where aa.TABLE_SCHEMA = '%s' and aa.TABLE_NAME = '%s';
                    ''' % (database, table_name)
            cursor.execute(sqllist)
            result = cursor.fetchall()
            td = [
                {
                    'field': i[0],
                    'type_name': i[1],
                    'type': i[4],
                    'comment': i[2],
                } for i in result
            ]
        return td

    def show_table_index(self, database, table_name):
        """
        获取表索引列表 返回 [{'id':0,'name':'idx_xxx','type':'','fields':'field1,field2'}]
        :param database:
        :param table_name:
        :return:
        """
        with self.conn.cursor() as cursor:
            sqllist = '''
            select aa.INDEX_ID, aa.`NAME`,aa.TYPE,group_concat(cc.`NAME` order by cc.POS) from information_schema.INNODB_INDEXES aa left JOIN information_schema.`INNODB_TABLES` bb on aa.TABLE_ID = bb.TABLE_ID left join information_schema.INNODB_FIELDS cc on aa.INDEX_ID = cc.INDEX_ID where aa.TYPE != 1 and bb.`NAME` = '%s/%s' group by cc.INDEX_ID order by cc.POS;
            ''' % (database, table_name)
            cursor.execute(sqllist)
            result = cursor.fetchall()
            td = [
                {
                    'id': i[0],
                    'name': i[1],
                    'type': i[2],
                    'fields': i[3]
                } for i in result
            ]
        return td
