import xlwings as xw

if __name__ == '__main__':
    app = xw.App(spec="wpsoffice")
    wb = app.books[r"/Users/codeme/PycharmProjects/data-dict-tool/1.xlsx"]