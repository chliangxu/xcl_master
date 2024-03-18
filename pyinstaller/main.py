from pathlib import Path
from demo1 import init
from json import load

init()
print("初始化数据完成，测试成功")
with open(Path("config/test.json"), "r") as f:
    data = load(f)


print("配置文件加载的数据为：", data)