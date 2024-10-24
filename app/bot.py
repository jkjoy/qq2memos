import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from fastapi import FastAPI

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 加载内置插件
nonebot.load_from_toml("pyproject.toml")  # 从 toml 文件加载插件

# 如果有额外的插件目录，可以这样加载
# nonebot.load_plugins("src/plugins")

# 定义 app 变量
app = nonebot.get_app()

if __name__ == "__main__":
    nonebot.run()