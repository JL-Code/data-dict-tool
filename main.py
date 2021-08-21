import xlwings as xw
import pandas as pd


# xlwings
# 对象模型
# app->book->sheet->range

def hello_xw():
    # 获取 xlwings 应用实例
    app = xw.App(visible=True, add_book=False)
    #  打开一个工作簿
    workbook = app.books.add()
    # 获取工作簿中的工作表
    sheet = workbook.sheets[0]
    df = pd.DataFrame(columns=['one', 'two'], data=[[1, 2], [3, 4]])
    sheet.range('A1').value = df
    # 保存 excel
    workbook.save('/Users/codeme/PycharmProjects/data-dict-tool/test.xlsx')
    # 退出应用
    # app.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hello_xw()
