#!/usr/bin/env python3
"""
调试 import a.b.c 的递归调用过程
专门用于观察和理解递归导入的详细流程
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from python_import_mechanism import python_import_simulation

def debug_import_a_b_c():
    """
    调试 import a.b.c 的完整递归过程
    """
    print("🚀" + "="*80)
    print("🔍 开始调试: import a.b.c 的递归调用过程")
    print("🚀" + "="*80)
    
    print("\n📋 预期的递归调用顺序:")
    print("1️⃣ python_import_simulation('test_a.b.c')")
    print("   ├── 🔄 递归调用: python_import_simulation('test_a')")
    print("   ├── 🔄 递归调用: python_import_simulation('test_a.b')")
    print("   └── 🎯 最终导入: 'test_a.b.c'")
    
    print("\n" + "="*80)
    print("🎬 开始实际执行...")
    print("="*80)
    
    try:
        # 清理可能存在的缓存
        modules_to_clean = ['test_a', 'test_a.b', 'test_a.b.c']
        for mod in modules_to_clean:
            if mod in sys.modules:
                del sys.modules[mod]
                print(f"🧹 清理缓存: {mod}")
        
        # 执行导入 (使用 test_a 作为包名)
        result = python_import_simulation('test_a.b.c')
        
        print("\n" + "="*80)
        print("✅ 导入完成！结果分析:")
        print("="*80)
        
        print(f"🎯 返回的模块: {result}")
        print(f"📛 模块名称: {result.__name__}")
        print(f"📁 模块文件: {getattr(result, '__file__', 'N/A')}")
        
        # 检查缓存中的模块
        print(f"\n📦 sys.modules 中的相关模块:")
        for mod_name in ['test_a', 'test_a.b', 'test_a.b.c']:
            if mod_name in sys.modules:
                mod = sys.modules[mod_name]
                print(f"   ✅ {mod_name}: {mod}")
            else:
                print(f"   ❌ {mod_name}: 未找到")
        
        # 测试模块功能
        print(f"\n🧪 功能测试:")
        
        # 测试顶层包 a
        if 'test_a' in sys.modules:
            a_module = sys.modules['test_a']
            if hasattr(a_module, 'function_in_a'):
                print(f"   📞 test_a.function_in_a(): {a_module.function_in_a()}")
        
        # 测试中间包 a.b
        if 'test_a.b' in sys.modules:
            ab_module = sys.modules['test_a.b']
            if hasattr(ab_module, 'function_in_b'):
                print(f"   📞 test_a.b.function_in_b(): {ab_module.function_in_b()}")
        
        # 测试目标模块 a.b.c
        if 'test_a.b.c' in sys.modules:
            abc_module = sys.modules['test_a.b.c']
            if hasattr(abc_module, 'function_in_c'):
                print(f"   📞 test_a.b.c.function_in_c(): {abc_module.function_in_c()}")
            if hasattr(abc_module, 'ClassInC'):
                obj = abc_module.ClassInC("测试实例")
                print(f"   🏗️ test_a.b.c.ClassInC 实例: {obj.get_info()}")
        
        # 验证包属性绑定
        print(f"\n🔗 包属性绑定检查:")
        if 'test_a' in sys.modules and hasattr(sys.modules['test_a'], 'b'):
            print(f"   ✅ test_a.b 已绑定到包 test_a")
            if hasattr(sys.modules['test_a'].b, 'c'):
                print(f"   ✅ test_a.b.c 已绑定到包 test_a.b")
            else:
                print(f"   ❌ test_a.b.c 未绑定到包 test_a.b")
        else:
            print(f"   ❌ test_a.b 未绑定到包 test_a")
            
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()

def debug_different_import_styles():
    """
    调试不同的导入方式
    """
    print("\n🚀" + "="*80)
    print("🔍 调试不同的导入方式")
    print("🚀" + "="*80)
    
    # 清理缓存
    modules_to_clean = ['test_a', 'test_a.b', 'test_a.b.c']
    for mod in modules_to_clean:
        if mod in sys.modules:
            del sys.modules[mod]
    
    test_cases = [
        {
            'name': 'import test_a.b.c',
            'module_name': 'test_a.b.c',
            'fromlist': None,
            'expected_return': 'test_a'
        },
        {
            'name': 'from test_a.b import c',
            'module_name': 'test_a.b',
            'fromlist': ['c'],
            'expected_return': 'test_a.b'
        },
        {
            'name': 'from test_a.b.c import function_in_c',
            'module_name': 'test_a.b.c',
            'fromlist': ['function_in_c'],
            'expected_return': 'test_a.b.c'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ 测试: {case['name']}")
        print("-" * 60)
        
        try:
            result = python_import_simulation(
                case['module_name'], 
                fromlist=case['fromlist']
            )
            print(f"✅ 成功! 返回: {result.__name__}")
            print(f"📝 期望返回: {case['expected_return']}")
            
            if result.__name__ == case['expected_return']:
                print("🎯 返回值符合预期!")
            else:
                print("⚠️ 返回值与预期不符!")
                
        except Exception as e:
            print(f"❌ 失败: {e}")

if __name__ == "__main__":
    # 主调试函数
    debug_import_a_b_c()
    
    # 不同导入方式的调试
    debug_different_import_styles()
    
    print("\n🏁" + "="*80)
    print("🔍 递归导入调试完成")
    print("🏁" + "="*80)
