# 测试包的初始化文件
"""
这是`test_package`包的初始化文件。

当一个包被导入时（例如 `import test_package`），这个`__init__.py`文件会被自动执行。
它的内容构成了包的命名空间。

此文件用于:
- 验证包的加载和执行。
- 定义包级别的变量和函数。
- 定义`__all__`列表，用于测试`from test_package import *`的行为。
"""

# 当`test_package`被导入时，这行代码会被执行。
print("正在初始化 test_package")

# 包级别的变量，可以通过`test_package.package_version`访问。
package_version = "1.0.0"

# 包级别的函数，可以通过`test_package.package_function()`调用。
def package_function():
    """一个定义在包根级别的函数。"""
    return "这是包级别的函数"

# `__all__`是一个列表，定义了当执行`from test_package import *`时，
# 哪些名称应该被导入到当前命名空间。
# 这是一种控制包的公共API的方式。
__all__ = ['package_version', 'package_function']