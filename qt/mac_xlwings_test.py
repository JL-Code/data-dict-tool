import xlwings as xw

if __name__ == '__main__':
    app = xw.App(spec="Microsoft Excel")
    wb = app.books.add()
    wb.save(r"/Users/codeme/Downloads/HJ费用预算系统数据字典.xlsx")
