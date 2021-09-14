# 单文件打包：
# pyinstaller -F -w --add-data "./qt/execl/view:./view"  ./qt/execl/main.py
# 单文件夹打包：
 pyinstaller -D -w --add-data "./qt/execl/view:./view" --add-data "./qt/execl/execl_util.py:./" --add-data "./qt/execl/sql_util.py:./"  ./qt/execl/main.py