#!/usr/bin/env python3
"""
检查包的 __path__ 属性
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    print("🔍 检查包的 __path__ 属性")
    print("="*50)
    
    # 清理缓存
    modules_to_clean = ['test_a', 'test_a.b', 'test_a.b.c']
    for mod in modules_to_clean:
        if mod in sys.modules:
            del sys.modules[mod]
    
    from python_import_mechanism import python_import_simulation
    
    # 导入 test_a.b
    print("1️⃣ 导入 test_a.b")
    result = python_import_simulation('test_a.b')
    
    # 检查 test_a.b 的 __path__ 属性
    print(f"\n📦 检查 test_a.b 模块:")
    if 'test_a.b' in sys.modules:
        test_a_b = sys.modules['test_a.b']
        print(f"   模块: {test_a_b}")
        print(f"   __name__: {test_a_b.__name__}")
        print(f"   __file__: {getattr(test_a_b, '__file__', 'N/A')}")
        print(f"   __package__: {getattr(test_a_b, '__package__', 'N/A')}")
        print(f"   __path__: {getattr(test_a_b, '__path__', 'N/A')}")
        
        if hasattr(test_a_b, '__path__'):
            print(f"   ✅ __path__ 存在: {test_a_b.__path__}")
        else:
            print(f"   ❌ __path__ 不存在")
    else:
        print("   ❌ test_a.b 不在 sys.modules 中")

if __name__ == "__main__":
    main()
