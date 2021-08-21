import pandas as pd
import json
import xlwings as xw

if __name__ == '__main__':

    # 使用 json 库读取 json 文件
    with open("./data/map.json", 'rb') as json_file:
        data = json.load(json_file)

    # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)
    # 下面代码实现了将df中的column列作为index
    # df.set_index(["Column"], inplace=True)
    # 添加一个工作簿
    wb = app.books.add()
    prev = ''
    for key in data:
        df = pd.DataFrame(data[key])
        df.set_index(["序号"], inplace=True)
        if prev == '':
            curr_sheet = wb.sheets.add(key)
        else:
            curr_sheet = wb.sheets.add(key, after=prev)
        curr_sheet.range('A2').value = df
        prev = key

    # 保存 excel
    # wb.save("D:\\Workspace\\python-execl\\数据字典.xlsx")

    # app.quit()
