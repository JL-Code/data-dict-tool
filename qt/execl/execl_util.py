import xlwings as xw
import pandas as pd


def build(data):
    # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)

    # 添加一个工作簿
    wb = app.books.add()

    catalog_name = '目录'
    prev = catalog_name
    catalog = wb.sheets.add(catalog_name)
    catalog_a1_address = catalog.range('A1').get_address()

    for key in data:
        df = pd.DataFrame(data[key])
        df.set_index(["序号"], inplace=True)

        curr_sheet = wb.sheets.add(key, after=prev)

        curr_sheet.range('A1').add_hyperlink(catalog_a1_address, text_to_display="返回目录",
                                             screen_tip=catalog_a1_address)
        curr_sheet.range('A2').value = df
        # sheet 工作表中所有列自动适应内容宽度
        curr_sheet.autofit()
        prev = key
