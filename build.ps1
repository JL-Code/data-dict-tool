# 单文件打包：
pyinstaller -F -w --add-data "./qt/view;./qt/view" --add-data "./qt/execl_util.py;./" --add-data "./qt/sql_util.py;./" ./data_dict.py
# 单文件夹打包：
#pyinstaller -D -w --add-data "./qt/view;./qt/view" --add-data "./qt/execl_util.py;./" --add-data "./qt/sql_util.py;./" ./data_dict.py
