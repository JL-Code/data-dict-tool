import sys
import pkg_resources
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
import pandas as pd
import json
import xlwings as xw


# 参考：https://www.bilibili.com/video/BV1wZ4y1G7Ur?from=search&seid=10558608980613499134&spm_id_from=333.337.0.0
# https://github.com/horychen/emachinery/tree/pypi-tut-video
# 打包命令1：pyinstaller -F -w --add-data "./view;./view"  .\main.py
# 打包命令2：pyinstaller -D -w --add-data "./view;./view"  .\main.py

class ExcelWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        path = "view/execl.ui"
        filepath = pkg_resources.resource_filename(__name__, path)
        try:
            self.ui = loadUi(filepath, self)
        except ModuleNotFoundError as e:
            print(str(e))
        except Exception as e:
            raise e
        self.ui.setWindowTitle("数据字典工具")
        self.ui.pushButton.clicked.connect(self.browse)

    def browse(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        # 过滤文件
        dialog.setNameFilter("Text files (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        file_names = []
        if dialog.exec():
            file_names = dialog.selectedFiles()
        dialog.close()
        if len(file_names) > 0:
            # 使用 json 库读取 json 文件
            with open(file_names[0], 'rb') as json_file:
                data = json.load(json_file)

            # 获取 xlwings 应用实例
            app = xw.App(visible=True, add_book=False)
            # 下面代码实现了将df中的column列作为index
            # df.set_index(["Column"], inplace=True)
            # 添加一个工作簿
            wb = app.books.add()

            catalog_name = '目录'
            prev = catalog_name
            catalog = wb.sheets.add(catalog_name)
            catalog_a1_address = catalog.range('A1').get_address()

            for key in data:
                df = pd.DataFrame(data[key])
                df.set_index(["序号"], inplace=True)
                # if prev == '':
                #     curr_sheet = wb.sheets.add(key)
                # else:
                #     curr_sheet = wb.sheets.add(key, after=prev)
                curr_sheet = wb.sheets.add(key, after=prev)

                curr_sheet.range('A1').add_hyperlink(catalog_a1_address, text_to_display="返回目录",
                                                     screen_tip=catalog_a1_address)
                curr_sheet.range('A2').value = df
                # sheet 工作表中所有列自动适应内容宽度
                curr_sheet.autofit()
                prev = key

        # try:
        #     fileName = QFileDialog.getOpenFileName(self,
        #                                            "Open Image", "C:\\Users\\codeme",
        #                                            "Image Files (*.png *.jpg *.bmp)")
        #     print(fileName)
        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExcelWidget()
    window.show()
    sys.exit(app.exec_())
