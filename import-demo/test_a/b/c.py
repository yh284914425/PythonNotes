# 目标模块 a.b.c
"""
这是模块 a.b.c
用于测试 import a.b.c 的递归调用过程
"""

print("🔥 正在加载模块 'a.b.c'")

# 模块级别的变量
module_c_version = "3.0.0"
module_c_data = "这是模块 a.b.c 的数据"

def function_in_c():
    """定义在模块 a.b.c 中的函数"""
    return "这是来自模块 a.b.c 的函数"

class ClassInC:
    """定义在模块 a.b.c 中的类"""
    def __init__(self, name="ClassInC"):
        self.name = name
        print(f"🏗️ 创建了 {self.name} 实例")
    
    def get_info(self):
        return f"这是 {self.name} 的信息，来自模块 a.b.c"

# 尝试相对导入
try:
    from .. import function_in_b
    print(f"✅ 成功从父包 a.b 导入函数: {function_in_b()}")
except ImportError as e:
    print(f"❌ 从父包 a.b 导入失败: {e}")

try:
    from ... import function_in_a
    print(f"✅ 成功从祖父包 a 导入函数: {function_in_a()}")
except ImportError as e:
    print(f"❌ 从祖父包 a 导入失败: {e}")

print(f"📦 模块 a.b.c 加载完成，版本: {module_c_version}")

# 模块加载时的计算
calculation_result = 10 + 20 + 30
print(f"🧮 模块加载时计算结果: {calculation_result}")
