import json

file = r"E:\GFCFile\IDs.Json"

# 读取数据
with open(file, 'r') as f:
    example_list = json.load(f)

result_list = sorted(example_list, key=lambda dict1: dict1['EDOID'])

# 写入 JSON 数据
with open(file, 'w') as f:
    json.dump(result_list, f, indent=4)