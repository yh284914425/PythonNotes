#!/usr/bin/env python3
"""
测试边界情况和错误处理
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from python_import_mechanism import python_import_simulation

def test_error_handling():
    """测试错误处理"""
    print("🧪 测试1: 错误处理")
    print("="*50)
    
    # 测试导入不存在的模块
    try:
        result = python_import_simulation('nonexistent_module')
        print(f"❌ 应该失败但成功了: {result}")
    except ImportError as e:
        print(f"✅ 正确处理不存在的模块: {e}")
    except Exception as e:
        print(f"⚠️ 意外的异常类型: {type(e).__name__}: {e}")

def test_builtin_module_fresh():
    """测试内置模块的新逻辑（清除缓存后）"""
    print("\n🧪 测试2: 内置模块处理（清除缓存）")
    print("="*50)
    
    # 清除 os 模块的缓存（如果存在）
    if 'os' in sys.modules:
        del sys.modules['os']
        print("🧹 清除了 os 模块缓存")
    
    try:
        result = python_import_simulation('os')
        print(f"✅ 内置模块导入成功: {result}")
        print(f"模块名: {result.__name__}")
        print(f"模块类型: {type(result)}")
    except Exception as e:
        print(f"❌ 内置模块导入失败: {e}")
        import traceback
        traceback.print_exc()

def test_deep_nesting():
    """测试深层嵌套的包结构"""
    print("\n🧪 测试3: 深层嵌套包结构")
    print("="*50)
    
    # 清理缓存
    modules_to_clean = ['test_a', 'test_a.b', 'test_a.b.c']
    for mod in modules_to_clean:
        if mod in sys.modules:
            del sys.modules[mod]
    
    try:
        result = python_import_simulation('test_a.b.c')
        print(f"✅ 深层嵌套导入成功: {result}")
        print(f"返回模块名: {result.__name__}")
        
        # 检查所有层级都被正确缓存
        for mod_name in ['test_a', 'test_a.b', 'test_a.b.c']:
            if mod_name in sys.modules:
                print(f"✅ {mod_name}: 已正确缓存")
            else:
                print(f"❌ {mod_name}: 缓存缺失")
                
    except Exception as e:
        print(f"❌ 深层嵌套导入失败: {e}")
        import traceback
        traceback.print_exc()

def test_parent_module_error():
    """测试父包导入失败的情况"""
    print("\n🧪 测试4: 父包导入失败处理")
    print("="*50)
    
    # 清理缓存
    if 'nonexistent' in sys.modules:
        del sys.modules['nonexistent']
    if 'nonexistent.child' in sys.modules:
        del sys.modules['nonexistent.child']
    
    try:
        result = python_import_simulation('nonexistent.child')
        print(f"❌ 应该失败但成功了: {result}")
    except ImportError as e:
        print(f"✅ 正确处理父包不存在: {e}")
    except KeyError as e:
        print(f"❌ KeyError 异常（可能是 sys.modules 访问问题）: {e}")
    except Exception as e:
        print(f"⚠️ 意外的异常类型: {type(e).__name__}: {e}")

def test_circular_import_protection():
    """测试循环导入保护"""
    print("\n🧪 测试5: 循环导入保护")
    print("="*50)
    
    # 这个测试比较复杂，需要创建循环导入的模块
    # 暂时跳过，因为需要创建特殊的测试文件
    print("⏭️ 跳过循环导入测试（需要特殊的测试文件）")

def test_fromlist_edge_cases():
    """测试 fromlist 的边界情况"""
    print("\n🧪 测试6: fromlist 边界情况")
    print("="*50)
    
    try:
        # 测试空的 fromlist
        result = python_import_simulation('test_package', fromlist=[])
        print(f"✅ 空 fromlist 处理成功: {result.__name__}")
        
        # 测试不存在的 fromlist 项
        result = python_import_simulation('test_package', fromlist=['nonexistent_item'])
        print(f"✅ 不存在的 fromlist 项处理成功: {result.__name__}")
        
    except Exception as e:
        print(f"❌ fromlist 边界情况失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 边界情况和错误处理测试")
    print("="*60)
    
    test_error_handling()
    test_builtin_module_fresh()
    test_deep_nesting()
    test_parent_module_error()
    test_circular_import_protection()
    test_fromlist_edge_cases()
    
    print("\n🏁 边界情况测试完成")
    print("="*60)
