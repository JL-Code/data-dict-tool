# 单文件夹打包：
pyinstaller -D -w --add-data "./view:./view" --add-data "./execl_util.py:./" --add-data "./sql_util.py:./" ./main.py
