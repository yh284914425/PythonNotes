# 中间包 a.b 的初始化文件
"""
这是包 a.b 的 __init__.py 文件
用于测试 import a.b.c 的递归调用过程
"""

print("🔥 正在初始化中间包 'a.b'")

# 包级别的变量
package_b_version = "2.0.0"
package_b_data = "这是包 a.b 的数据"

def function_in_b():
    """定义在包 a.b 中的函数"""
    return "这是来自包 a.b 的函数"

# 尝试访问父包
try:
    from .. import function_in_a
    print(f"✅ 成功从父包导入函数: {function_in_a()}")
except ImportError as e:
    print(f"❌ 从父包导入失败: {e}")

print(f"📦 包 a.b 初始化完成，版本: {package_b_version}")
