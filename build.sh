# TODO: 支持参数选择不同打包方式
# 获取构建模式，默认为单文件 -F 构建，支持 -F、-D
build_mode=${1:-"-F"}
# 构建前清除旧制品
if [ -d "./dist" ]; then
    rm -rf ./dist
fi
pyinstaller "$build_mode" -w -i ./logo.ico --add-data "./qt/view:./qt/view" --add-data "./qt/execl_util_openpyxl.py:./qt" --add-data "./qt/sql_util.py:./qt" ./data_dict.py
# 单文件打包：
#pyinstaller -F -w -i ./logo.ico --add-data "./qt/view:./qt/view" --add-data "./qt/execl_util_openpyxl.py:./qt" --add-data "./qt/sql_util.py:./qt" ./data_dict.py
# 单文件夹打包：
#pyinstaller -D -w -i ./logo.ico --add-data "./qt/view:./qt/view" --add-data "./qt/execl_util.py:./qt" --add-data "./qt/sql_util.py:./qt" ./data_dict.py
