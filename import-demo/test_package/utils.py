# 测试工具模块
"""
这是 test_package 包中的 utils 子模块。
用于测试相对导入功能，特别是 `from .. import utils` 的场景。
"""

print("正在加载 test_package.utils")

# 工具函数
def utility_function():
    """一个工具函数，用于测试相对导入。"""
    return "这是来自 test_package.utils 的工具函数"

# 工具类
class UtilityClass:
    """一个工具类，用于测试相对导入。"""
    def __init__(self, name="UtilityClass"):
        self.name = name
    
    def get_info(self):
        return f"这是 {self.name} 实例"

# 模块级别的变量
utils_version = "1.0.0"
utils_data = {"type": "utility", "package": "test_package"}
