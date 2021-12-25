# 单文件打包：
pyinstaller -F -w --add-data "./qt/view:./view" --add-data "./qt/execl_util.py:./" --add-data "./qt/sql_util.py:./" ./qt/main.py
