# 简单的测试模块
"""
这是一个用于测试的简单、独立的Python模块。

它不属于任何包，代表了最基本的导入单元。
`run_tests.py`中的`test_simple_module_import`函数会使用此文件
来验证导入模拟器是否能正确处理单个.py文件的导入。

此模块包含:
- print语句: 用于在加载时提供反馈。
- 模块级别的变量。
- 一个简单的函数。
- 一个简单的类。
"""

# 当这个模块被导入时，这行代码会被执行，并打印到控制台。
print("正在加载 test_simple_module")

# 模块级别的变量
module_name = "test_simple_module"
module_version = "1.0"

# 模块级别的函数
def simple_function():
    """一个简单的函数，返回一个表示来源的字符串。"""
    return f"这是来自 {module_name} 的简单函数"

# 模块级别的类
class SimpleClass:
    """一个简单的类，用于测试模块内类的实例化和方法调用。"""
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        """返回初始化时传入的值。"""
        return self.value

# 模块加载时会执行的顶层代码
result = 10 + 20
print(f"模块加载时计算结果: {result}")