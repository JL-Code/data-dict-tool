import pandas as pd
import json

if __name__ == '__main__':
    # df = pd.DataFrame({
    #     "序号": 1,
    #     "字段名称": "ID",
    #     "中文名称": "主键",
    #     "字段类型": "VARCHAR(36)",
    #     "长度（字符）": 36,
    #     "长度（数值）": '',
    #     "精度（数值）": '',
    #     "是否主键": "是",
    #     "是否必须": "是",
    #     "备注": "主键"
    # })

    data1 = {'one': [1., 2., 3., 4.], 'two': [4., 3., 2., 1.]}
    data2 = {'one': [1], 'two': [2]}

    # 列表字典
    list_dict_data = [{
        "序号": 26,
        "字段名称": "PROPOSER_ID",
        "中文名称": "申请人ID",
        "字段类型": "VARCHAR(36)",
        "长度（字符）": 36,
        "长度（数值）": "",
        "精度（数值）": "",
        "是否主键": "否",
        "是否必须": "是",
        "备注": "申请人ID"
    }]

    # 使用 json 库读取 json 文件
    with open("./data/data.json") as json_file:
        list_dict_data1 = json.load(json_file)

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    df3 = pd.DataFrame(list_dict_data)
    df4 = pd.DataFrame(list_dict_data1)

    # print(df1)
    # print(df2)
    # print(df3)
    # print(df4)
