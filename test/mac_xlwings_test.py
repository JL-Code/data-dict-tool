import xlwings as xw
from xlwings import utils

# http://yueban.github.io/2019/04/07/xlwings-%E5%9C%A8-mac-%E7%8E%AF%E5%A2%83%E4%B8%8B%E7%9A%84%E5%87%A0%E4%B8%AA%E5%9D%91/

# 可以先将文件保存到 excel 程序有访问权限的路径下，然后将保存后的文件复制到目标目录。

# excel 程序有访问权限的路径一般为：
# /Users/username/Library/Group Containers/xxxxx.Office/MyExcelFolder/


if __name__ == '__main__':
    with xw.App(visible=True, add_book=False, spec="Microsoft Excel") as app:
        # book = xw.books['/Users/codeme/Library/Containers/com.microsoft.Excel/Data/Documents/books.xlsx']
        book = xw.books.add()  # 新建一个 workbook
        # book = xw.books['test1.xlsx']
        sheet = book.sheets['Sheet1']
        sheet.range('A1').value = 'Foo 1'
        print(utils.fspath(r"/Users/codeme/Downloads/macOS.xlsx"))
        # book.save("macOS.xlsx")  # 默认行为，文件保存到 /Users/codeme/Library/Containers/com.microsoft.Excel/Data/Documents 目录
        book.save(r"/Users/codeme/Downloads/macOS.xlsx")
