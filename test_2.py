import pandas as pd


def excel_to_nested_dict(file_path):
    """
    将Excel文件数据转换为嵌套字典结构。

    :param file_path: Excel文件路径
    :return: 转换后的嵌套字典数据
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 初始化结果字典
    data_dict = {}

    # 遍历每一行数据进行处理
    for index, row in df.iterrows():
        # 获取桥梁类别
        bridge_type = row['桥梁类别']

        # 初始化桥梁类别下的字典
        if bridge_type not in data_dict:
            data_dict[bridge_type] = {}

        # 初始化部件区域
        part = row['部位']
        data_dict[bridge_type][part] = data_dict[bridge_type].get(part, {})

        # 初始化构件名称
        component_name = row['构件名称']
        data_dict[bridge_type][part][component_name] = data_dict[bridge_type][part].get(component_name, {})

        # 初始化病害类型
        defect_type = row['病害类型']
        data_dict[bridge_type][part][component_name][defect_type] = {
            '最大标度': row['最大标度'],
            '构件ID': row['构件ID'],
            '标度1定性描述': row['标度1定性描述'],
            '标度1定量描述': row['标度1定量描述'],
            '标度2定性描述': row['标度2定性描述'],
            '标度2定量描述': row['标度2定量描述'],
            '标度3定性描述': row['标度3定性描述'],
            '标度3定量描述': row['标度3定量描述'],
            '标度4定性描述': row['标度4定性描述'],
            '标度4定量描述': row['标度4定量描述'],
            '标度5定性描述': row['标度5定性描述'],
            '标度5定量描述': row['标度5定量描述']
        }

    return data_dict


# 使用方法
print('s')
file_path = './res/病害数据.xlsx'
result_data = excel_to_nested_dict(file_path)
with open('./res/result.json', 'w') as f:
    import json
    f.write(json.dumps(result_data))
    print('ok')