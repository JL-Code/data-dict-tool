import xlwings as xw
import pandas as pd
import logging

"""
    data 导出数据
    filepath 文件存放地址
"""


def build(data, filepath, spec):
    logging.debug("目标路径:", filepath)
    try:
        # 获取 xlwings 应用实例 , 使用 with 确保 Execl 实例每次都被正常清理
        with xw.App(add_book=False, visible=True, spec=spec) as app:
            # 如果为True, 让Excel程序变为最前台的应用，并且把焦点从Python切换到Excel
            app.activate(steal_focus=True)
            # book = app.books.add()
            catalog_name = '目录'
            prev = catalog_name
            print("创建 sheet ", catalog_name)
            xw.sheets.add(catalog_name)
            print("xw ", xw)
            print("app ", app)
            print("xw.sheets ", xw.sheets)
            catalog_a1_address = xw.sheets.active.range('A1').get_address()
            # 填充 catalog sheet 内容
            catalog_df = pd.DataFrame(data[catalog_name])
            catalog_df.set_index(["序号"], inplace=True)

            xw.sheets.active.range('A1').value = catalog_df
            xw.sheets.active.autofit()

            for key in data:
                if key == '目录':
                    continue
                df = pd.DataFrame(data[key])
                df.set_index(["序号"], inplace=True)
                print("创建 sheet ", key)
                # book.sheets.add(key, after=prev)
                xw.sheets.add(key, after=prev)
                curr_sheet = xw.sheets.active
                curr_sheet.range('A1').add_hyperlink(catalog_a1_address, text_to_display="返回目录",
                                                     screen_tip=catalog_a1_address)
                curr_sheet.range('A2').value = df
                # sheet 工作表中所有列自动适应内容宽度
                curr_sheet.autofit()
                prev = key

            """问题描述: https://github.com/xlwings/xlwings/issues/957"""
            """解决方案: https://github.com/xlwings/xlwings/pull/1372"""
            xw.books.active.save(filepath)

    except IOError as e:
        logging.debug("IOError:", e)
        print("IOError:", e)
