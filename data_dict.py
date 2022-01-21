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
           TABLE_COMMENT    as '中文名称',
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
           t.TABLE_COMMENT                    AS '数据表中文名',
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
        self.ui.le_host.setText('192.168.1.32')
        self.ui.le_port.setText('3308')
        self.ui.le_user.setText('root')
        self.ui.le_passwd.setText('rootCqhz.2020')
        self.ui.le_file.setText('/Users/codeme/Downloads/HJ费用预算系统数据字典.xlsx')
        self.ui.le_db.setText('highzap_jerp_basic_app_integrated')
        self.ui.le_prefix.setText('ebs_')

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


def run(host='192.168.1.32',
        port=3308,
        user='root',
        password='rootCqhz.2020',
        db='information_schema',
        charset='utf8',
        filepath="Microsoft Excel",
        prefix='ebs_'):
    result = create_db_conn(host, port, user, password, db, charset)
    conn = result[0]
    cursor = result[1]

    try:
        data = get_table_metadata(cursor, db, prefix)
        build(data, filepath)
    except BaseException as e:
        logging.error(e)
    finally:
        conn.close()


if __name__ == '__main__':
    # https://docs.python.org/zh-cn/3.8/library/logging.html
    # https://stackoverflow.com/questions/36046004/python-logging-working-on-windows-but-not-mac-os

    log_format = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
    date_fmt = "%m-%d %H:%M"

    logging.basicConfig(filename=os.path.join(os.path.expanduser('~'), 'Library/logs', 'data_dict.log'),
                        level=logging.INFO,
                        filemode="a",
                        format=log_format, datefmt=date_fmt)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_fmt))

    logger = logging.getLogger("app")
    logger.addHandler(stream_handler)

    logger.info("information")
    logger.warning("warning")

    app = QApplication(sys.argv)
    widget = DictViewWidget()
    widget.show()
    sys.exit(app.exec_())
