from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import logging

"""
    data 导出数据
    filepath 文件存放地址
    https://openpyxl.readthedocs.io/en/stable/pandas.html
"""


# TODO: sheet 列自动适应内容宽度 【1】
# TODO: sheet 序号文本居中 【3】
# TODO: 清理生成的空白 sheet 【2】
# TODO: 自定义表头样式 【3】
# TODO: 生成返回目录超链接 【3】
def build(data, filepath):
    logging.debug("目标路径: %s", filepath)
    try:
        wb = Workbook()
        catalog_name = "目录"
        print("创建 sheet ", catalog_name)
        ws_catalog_sheet = wb.create_sheet(title=catalog_name)
        # catalog_a1_address = ws_catalog["A1"]
        # 填充 catalog sheet 内容
        catalog_df = pd.DataFrame(data[catalog_name])
        # 单元格增加超链接 https://stackoverflow.com/questions/39077661/adding-hyperlinks-in-some-cells-openpyxl
        # '=HYPERLINK("{}", "{}")'.format(link, "Link Name")
        # e.g. ws.cell(row=1, column=1).value = '=HYPERLINK("{}", "{}")'.format(link, "Link Name")
        # 设置 dataframe 索引使用已存在的列
        # catalog_df.set_index(["序号"], inplace=True)
        rows = dataframe_to_rows(catalog_df, index=False, header=True)
        start_row_index = 0  # 0 是 header，数据行从 1 开始。
        for row in rows:
            if start_row_index != 0:
                print(row[1])
                print(row[2])
                row[1] = '=HYPERLINK("#{}!A1", "{}")'.format(row[2], row[1])
                print(row[1])
            ws_catalog_sheet.append(row)
            start_row_index += 1
        index = wb.get_index(ws_catalog_sheet) + 1
        for key in data:
            if key == "目录":
                continue
            df = pd.DataFrame(data[key])
            df.set_index(["序号"], inplace=True)
            print("创建 sheet ", key)
            curr_sheet = wb.create_sheet(title=key, index=index)
            # 填充返回目录信息
            cl_df = pd.DataFrame([{"序号": 0, "TEXT": '=HYPERLINK("#{}!A1", "{}")'.format(catalog_name, '返回目录')}])
            cl_df_rows = dataframe_to_rows(cl_df, index=False, header=False)
            for row in cl_df_rows:
                curr_sheet.append(row)
            # 填充数据字典信息
            rows = dataframe_to_rows(df, index=False, header=True)
            for row in rows:
                curr_sheet.append(row)
            index = wb.get_index(curr_sheet) + 1

        """问题描述: https://github.com/xlwings/xlwings/issues/957"""
        """解决方案: https://github.com/xlwings/xlwings/pull/1372"""
        wb.remove_sheet(wb.active)  # fix: 删除默认生成的空白 Sheet
        wb.save(filepath)

    except IOError as e:
        logging.debug("IOError:", e)
        print("IOError:", e)
