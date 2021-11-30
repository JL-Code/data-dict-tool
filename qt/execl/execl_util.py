import xlwings as xw
import pandas as pd
import logging

"""
    data 导出数据
    filepath 文件存放地址
"""


def build(data, filepath, spec):
    logging.debug("filepath:", filepath)
    try:
        # 获取 xlwings 应用实例 , 使用 with 确保 Execl 实例每次都被正常清理
        with xw.App(visible=False, add_book=False, spec=spec) as app:
            print(app.books)
            # 添加一个工作簿
            # wb = app.books[filepath]
            # wb = app.books.open(filepath)
            wb = app.books.add()
            catalog_name = '目录'
            prev = catalog_name
            catalog = wb.sheets.add(catalog_name)
            catalog_a1_address = catalog.range('A1').get_address()
            # 填充 catalog sheet 内容
            catalog_df = pd.DataFrame(data[catalog_name])
            catalog_df.set_index(["序号"], inplace=True)
            catalog.range('A1').value = catalog_df
            catalog.autofit()

            for key in data:
                if key == '目录':
                    continue

                df = pd.DataFrame(data[key])

                df.set_index(["序号"], inplace=True)

                curr_sheet = wb.sheets.add(key, after=prev)

                curr_sheet.range('A1').add_hyperlink(catalog_a1_address, text_to_display="返回目录",
                                                     screen_tip=catalog_a1_address)
                curr_sheet.range('A2').value = df
                # sheet 工作表中所有列自动适应内容宽度
                curr_sheet.autofit()
                prev = key

            """问题描述: https://github.com/xlwings/xlwings/issues/957"""
            """解决方案: https://github.com/xlwings/xlwings/pull/1372"""
            wb.save(filepath)

    except IOError as e:
        logging.debug("IOError:", e)
        print(e)
    except OSError as e:
        logging.error("OSError:", e)
        print(e)
