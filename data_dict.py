#! /usr/bin/python
# -*- coding: utf-8 -*-

import functools
import logging
import os.path
import sys

import pkg_resources
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi

from qt.execl_util_openpyxl import build
from qt.sql_util import create_db_conn, get_dataset


def get_table_metadata(cursor, table_schema, table_name_prefix):
    tables_sql = """SELECT @serial_num := @serial_num + 1 AS '序号',
           upper  (TABLE_NAME) as '表名称',
           IF(TRIM(TABLE_COMMENT) = '', TABLE_NAME, TABLE_COMMENT) AS '中文名称',
           ''               as '数据量',
           ''               as '平均日增量',
           ''               as '平均月增量',
           ''               as '平均年增量',
           ''               as '备注'
    FROM information_schema.TABLES,
         (SELECT @serial_num := 0) serial_num
    WHERE TABLE_SCHEMA = '%s'
      AND TABLE_NAME LIKE '%s'
    order by TABLE_NAME""" % (table_schema, table_name_prefix + "%")

    columns_sql = """SELECT c.ORDINAL_POSITION                 AS '序号',
           c.TABLE_NAME                       AS '数据表',
           IF(TRIM(t.TABLE_COMMENT) = '', t.TABLE_NAME, t.TABLE_COMMENT)                    AS '数据表中文名',
           upper(c.COLUMN_NAME)               AS '字段名称',
           c.COLUMN_COMMENT                   AS '中文名称',
           upper(c.COLUMN_TYPE)               AS '字段类型',
           c.CHARACTER_MAXIMUM_LENGTH         AS '长度（字符）',
           c.NUMERIC_PRECISION                AS '长度（数值）',
           c.NUMERIC_SCALE                    AS '精度（数值）',
           IF(c.COLUMN_KEY = 'PRI', '是', '否') AS '是否主键',
           IF(c.IS_NULLABLE = 'NO', '是', '否') AS '是否必须',
           c.column_comment                   AS '备注'
    FROM information_schema.COLUMNS c
             LEFT JOIN information_schema.TABLES t
                       on c.TABLE_NAME = t.TABLE_NAME and c.TABLE_SCHEMA = t.TABLE_SCHEMA
    WHERE c.TABLE_SCHEMA =
          (SELECT SCHEMA_NAME
           FROM information_schema.SCHEMATA
           WHERE SCHEMA_NAME = '%s')
      and c.TABLE_NAME LIKE '%s'
    ORDER BY c.TABLE_NAME""" % (table_schema, table_name_prefix + "%")

    tables = get_dataset(cursor, tables_sql)
    columns = get_dataset(cursor, columns_sql)

    return convert(tables, columns)


def convert(tables, columns):
    table_metadata = {'目录': tables}
    titles = list(map(lambda m: m['中文名称'], tables))

    for title in titles:
        # 提取对应表的字段列
        items = list(filter(lambda c: c['数据表中文名'] == title, columns))

        # 按照字段在表中的序号排序
        items = sorted(items, key=functools.cmp_to_key(lambda first, second: first['序号'] - second['序号']))

        # 移除数据表、数据表中文名字段
        for item in items:
            del item['数据表']
            del item['数据表中文名']
            # 从 list 中移除 item
            columns.remove(item)

        table_metadata[title] = items

    return table_metadata


class DictViewWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        path = "qt/view/dict_view.ui"
        filepath = pkg_resources.resource_filename(__name__, path)
        try:
            self.ui = loadUi(filepath, self)
        except ModuleNotFoundError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)
            raise e

        self.ui.setWindowTitle("数据字典工具")
        self.ui.le_host.setText('47.83.18.163')
        self.ui.le_port.setText('3307')
        self.ui.le_user.setText('root')
        self.ui.le_passwd.setText('12345678')
        self.ui.le_file.setText('数据字典.xlsx')
        self.ui.le_db.setText('bijiaqi_v2')
        self.ui.le_prefix.setText('')

        self.ui.pushButton.clicked.connect(self.click_btn)
        self.ui.chooseFile.clicked.connect(self.get_save_path)

    def click_btn(self):
        # 获取文件存储路径
        # filepath = self.browse()

        host = self.ui.le_host.text()
        port = self.ui.le_port.text()
        user = self.ui.le_user.text()
        passwd = self.ui.le_passwd.text()
        db = self.ui.le_db.text()
        filepath = self.ui.le_file.text()
        prefix = self.ui.le_prefix.text()
        charset = 'utf8'

        run(host, int(port), user, passwd, db, charset, filepath, prefix)

    # 通过 QFileDialog.getSaveFileName 获取保存路径
    def get_save_path(self):
        directory = QFileDialog.getSaveFileName(self, "文件保存路径", "./", "Excel Files (*.xls);;Excel Files (*.xlsx)")
        self.ui.le_file.setText(directory[0])


def run(host='47.83.18.163',
        port=3307,
        user='root',
        password='12345678',
        db='information_schema',
        charset='utf8',
        filepath="Microsoft Excel",
        prefix=''):
    """
    运行数据库操作。
    连接到数据库，获取表元数据，并根据这些元数据构建相应的文件。

    :param host: 数据库主机地址，默认为'47.83.18.163'
    :param port: 数据库端口，默认为3307
    :param user: 数据库用户名，默认为'root'
    :param password: 数据库密码，默认为'12345678'
    :param db: 连接的数据库名称，默认为'information_schema'
    :param charset: 数据库字符集，默认为'utf8'
    :param filepath: 导出数据的目标文件路径，默认为"Microsoft Excel"
    :param prefix: 表名前缀，默认为空字符串
    """
    result = create_db_conn(host, port, user, password, db, charset)
    conn = result[0]
    cursor = result[1]

    try:
        data = get_table_metadata(cursor, db, prefix)
        build(data, filepath)
        logging.info("build success")
    except BaseException as e:
        logging.error("run", e)
    finally:
        conn.close()


if __name__ == '__main__':
    # https://docs.python.org/zh-cn/3.8/library/logging.html
    # https://stackoverflow.com/questions/36046004/python-logging-working-on-windows-but-not-mac-os

    log_format = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
    date_fmt = "%m-%d %H:%M"
    # os.path.join(os.path.expanduser('~'), 'logs', 'data_dict.log'
    logging.basicConfig(filename="data_dict.log",
                        level=logging.INFO,
                        filemode="a",
                        encoding="utf-8",
                        format=log_format, datefmt=date_fmt)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_fmt))

    logger = logging.getLogger("app")
    logger.addHandler(stream_handler)

    app = QApplication(sys.argv)
    widget = DictViewWidget()
    widget.show()
    sys.exit(app.exec_())
