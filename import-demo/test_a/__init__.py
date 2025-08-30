# 顶层包 a 的初始化文件
"""
这是包 a 的 __init__.py 文件
用于测试 import a.b.c 的递归调用过程
"""

print("🔥 正在初始化顶层包 'a'")

# 包级别的变量
package_a_version = "1.0.0"
package_a_data = "这是包 a 的数据"

def function_in_a():
    """定义在包 a 中的函数"""
    return "这是来自包 a 的函数"

# 包初始化时的一些操作
print(f"📦 包 a 初始化完成，版本: {package_a_version}")
