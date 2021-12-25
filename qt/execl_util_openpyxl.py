from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import logging

"""
    data 导出数据
    filepath 文件存放地址
    https://openpyxl.readthedocs.io/en/stable/pandas.html
"""


# TODO: sheet 工作表中所有列自动适应内容宽度
# TODO: sheet 序号文本居中
def build(data, filepath):
    logging.debug("目标路径:", filepath)
    try:
        wb = Workbook()
        # book = app.books.add()
        catalog_name = "目录"
        print("创建 sheet ", catalog_name)
        ws_catalog = wb.create_sheet(title=catalog_name)
        # catalog_a1_address = ws_catalog["A1"]
        # 填充 catalog sheet 内容
        catalog_df = pd.DataFrame(data[catalog_name])
        catalog_df.set_index(["序号"], inplace=True)
        for r in dataframe_to_rows(catalog_df, index=True, header=True):
            ws_catalog.append(r)

        index = wb.get_index(ws_catalog) + 1
        for key in data:
            if key == "目录":
                continue
            df = pd.DataFrame(data[key])
            df.set_index(["序号"], inplace=True)
            print("创建 sheet ", key)

            curr_sheet = wb.create_sheet(title=key, index=index)
            for r in dataframe_to_rows(df, index=True, header=True):
                curr_sheet.append(r)

            index = wb.get_index(curr_sheet) + 1

        """问题描述: https://github.com/xlwings/xlwings/issues/957"""
        """解决方案: https://github.com/xlwings/xlwings/pull/1372"""
        wb.save(filepath)

    except IOError as e:
        logging.debug("IOError:", e)
        print("IOError:", e)
