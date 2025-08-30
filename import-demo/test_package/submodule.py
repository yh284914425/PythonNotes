# 测试子模块
"""
这是`test_package`包中的一个子模块。

它的存在是为了测试导入模拟器处理子模块导入（如 `import test_package.submodule`）
和相对导入（如 `from . import ...`）的能力。

此模块包含:
- 顶层print语句。
- 变量、函数和类。
- 一个相对导入语句，用于测试从子模块到其父包的导入。
"""

# 当这个子模块被导入时，这行代码会被执行。
print("正在加载 test_package.submodule")

# 子模块级别的变量
submodule_data = "子模块数据"

# 子模块级别的函数
def submodule_function():
    """一个定义在子模块中的函数。"""
    return "这是子模块的函数"

# 子模块级别的类
class SubmoduleClass:
    """一个定义在子模块中的类。"""
    def __init__(self):
        self.name = "SubmoduleClass实例"
    
    def method(self):
        return f"调用了 {self.name} 的方法"

# --- 相对导入测试 ---
# 这行代码测试了相对导入的核心功能。
# `from . import package_function` 表示:
# - `.` (level=1): 从当前包（`test_package`）开始查找。
# - `import package_function`: 寻找一个名为`package_function`的变量/函数/类或子模块。
# 在这里，它会成功地从父包的`__init__.py`中导入`package_function`函数。
print("尝试从子模块进行相对导入...")
from . import package_function
print(f"子模块中调用父包函数成功: {package_function()}")