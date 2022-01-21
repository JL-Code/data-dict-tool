# 单文件打包：
#pyinstaller -F -w -i ./logo.ico --add-data "./qt/view:./qt/view" --add-data "./qt/execl_util_openpyxl.py:./qt" --add-data "./qt/sql_util.py:./qt" ./data_dict.py
# 单文件夹打包：
pyinstaller -D -w -i ./logo.ico --add-data "./qt/view:./qt/view" --add-data "./qt/execl_util.py:./qt" --add-data "./qt/sql_util.py:./qt" ./data_dict.py
