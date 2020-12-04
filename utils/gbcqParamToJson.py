import json

jsonStyleParamFile = r"F:\GBCQ_TMP\jsonStyleParam.txt"
jsonStyleParamNewFile = r"F:\GBCQ_TMP\jsonStyleParamNew.txt"

# 读取数据
with open(jsonStyleParamFile, mode='r', encoding='utf8') as f:
    data = json.load(f)

# 写入 JSON 数据
with open(jsonStyleParamFile, mode='w', encoding='utf8') as f:
    json.dump(data, f, indent=4)

# 读取数据
with open(jsonStyleParamNewFile, mode='r', encoding='utf8') as f:
    data = json.load(f)

# 写入 JSON 数据
with open(jsonStyleParamNewFile, mode='w', encoding='utf8') as f:
    json.dump(data, f, indent=4) 