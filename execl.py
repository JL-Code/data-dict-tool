import pandas as pd
import json
import xlwings as xw

if __name__ == '__main__':

    # 使用 json 库读取 json 文件
    with open("./data/map.json") as json_file:
        data = json.load(json_file)

    # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)

    # 添加一个工作簿
    wb = app.books.add()
    prev = ''
    for key in data:
        df = pd.DataFrame(data[key])
        if prev == '':
            curr_sheet = wb.sheets.add(key)
        else:
            curr_sheet = wb.sheets.add(key, after=prev)
        curr_sheet.range('A2').value = df
        prev = key

    # 保存 excel
    wb.save("/Users/codeme/Library/Group Containers/UBF8T346G9.Office/数据字典.xlsx")

    app.quit()
