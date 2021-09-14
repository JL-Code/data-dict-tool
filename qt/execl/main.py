import functools
from sql_util import create_db_conn, get_dataset
from execl_util import build
import sys
import pkg_resources
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi


def run(host='192.168.1.32',
        port=3306,
        user='dev',
        password='Cqhz.2020',
        db='information_schema',
        charset='utf8',
        filepath=""):
    result = create_db_conn(host, port, user, password, db, charset)
    conn = result[0]
    cursor = result[1]

    try:
        data = get_table_metadata(cursor)
        build(data, filepath)
    except BaseException as e:
        print("exception:", e)
    finally:
        conn.close()


def get_table_metadata(cursor):
    tables_sql = """SELECT @serial_num := @serial_num + 1
                            AS '序号',
           upper
               (TABLE_NAME) as '表名称',
           TABLE_COMMENT    as '中文名称',
           ''               as '数据量',
           ''               as '平均日增量',
           ''               as '平均月增量',
           ''               as '平均年增量',
           ''               as '备注'
    FROM information_schema.TABLES,
         (SELECT @serial_num := 0) serial_num
    WHERE TABLE_SCHEMA = 'highzap_ebs_0715'
      AND TABLE_NAME LIKE 'ebs_%'
    order by TABLE_NAME;"""

    columns_sql = """SELECT c.ORDINAL_POSITION         AS '序号',
           c.TABLE_NAME                   AS '数据表',
           t.TABLE_COMMENT                AS '数据表中文名',
           upper
    (c.COLUMN_NAME)           AS '字段名称',
           c.COLUMN_COMMENT               AS '中文名称',
           upper
    (c.COLUMN_TYPE)           AS '字段类型',
           c.CHARACTER_MAXIMUM_LENGTH     AS '长度（字符）',
           c.NUMERIC_PRECISION            AS '长度（数值）',
           c.NUMERIC_SCALE                AS '精度（数值）',
           CASE

               WHEN c.COLUMN_KEY = 'PRI' THEN
                   '是'
               ELSE '否'
    END                        AS '是否主键',
           CASE

               WHEN c.IS_NULLABLE = 'NO' THEN
                   '是'
               ELSE '否'
    END                        AS '是否必须',
           c.column_comment               AS '备注'
    FROM information_schema.COLUMNS c
           left join information_schema.TABLES t on c.TABLE_NAME = t.TABLE_NAME and c.TABLE_SCHEMA=t.TABLE_SCHEMA
    WHERE c.TABLE_SCHEMA =
    (SELECT SCHEMA_NAME
           FROM information_schema.SCHEMATA
           WHERE SCHEMA_NAME = 'highzap_ebs_0715')
           and c.TABLE_NAME like 'ebs_%'
    ORDER BY c.TABLE_NAME;"""

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

        path = "view/dict_view.ui"
        filepath = pkg_resources.resource_filename(__name__, path)
        try:
            self.ui = loadUi(filepath, self)
        except ModuleNotFoundError as e:
            print(str(e))
        except Exception as e:
            raise e

        self.ui.setWindowTitle("数据字典工具")
        self.ui.le_host.setText('192.168.1.32')
        self.ui.le_port.setText('3306')
        self.ui.le_user.setText('dev')
        self.ui.le_passwd.setText('Cqhz.2020')
        self.ui.le_db.setText('information_schema')

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
        charset = 'utf8'

        run(host, int(port), user, passwd, db, charset, filepath)

    # 通过 QFileDialog.getSaveFileName 获取保存路径
    def get_save_path(self):
        directory = QFileDialog.getSaveFileName(self, "文件保存路径", "./", "所有文件 (*);")
        self.ui.le_file.setText(directory[0])

    # 文件浏览函数
    # 返回一个文件路径
    def browse(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        # 过滤文件
        dialog.setNameFilter("Text files (*.xlxs)")
        dialog.setViewMode(QFileDialog.Detail)
        file_names = []
        if dialog.exec():
            file_names = dialog.selectedFiles()
        dialog.close()

        if len(file_names) > 0:
            self.ui.le_file.setText(file_names[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DictViewWidget()
    widget.show()
    sys.exit(app.exec_())
