import xlwings as xw
import pandas as pd


# data 导出数据
# filepath 文件存放地址
def build(data, filepath):
    # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)

    # 添加一个工作簿
    wb = app.books.add()

    catalog_name = '目录'
    prev = catalog_name
    catalog = wb.sheets.add(catalog_name)
    catalog_a1_address = 'D:\\Workspace\\python-execl\\qt\\execl\\目录!$A$1'
    # catalog.range('A1').get_address()
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

    # 保存文件
    wb.save(filepath)
    # 关闭工作簿
    wb.close()
    # 退出Excel
    app.quit()
