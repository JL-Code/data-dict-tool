import pandas as pd
import json
import xlwings as xw

if __name__ == '__main__':

    # 使用 json 库读取 json 文件
    with open("./data/data2.json") as json_file:
        data = json.load(json_file)

        # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)

    # 添加一个工作簿
    wb = app.books.add()

    for key in data:
        df = pd.DataFrame(data[key])
        curr_sheet = wb.sheets.add(key)
        curr_sheet.Range('A1').value = df

    # 保存 excel
    wb.save("test1.xlsx")
    # 退出工作簿
    wb.close()
    # 退出应用
    app.quit()

    # print(df1)
    # print(df2)
    # print(df3)
    # print(df4)
