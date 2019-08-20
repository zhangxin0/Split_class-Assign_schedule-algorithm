"""
Transfer data(source file) to Json
"""
from . import data as Data
import json

# 模拟Java端传入的数据
jsonObject = json.dumps(Data.Data(), default=lambda obj: obj.__dict__, indent=4)
# 解析数据
data_transfer = json.loads(jsonObject)
data = Data.Data()
data.__dict__ = data_transfer