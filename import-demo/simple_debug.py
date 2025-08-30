#!/usr/bin/env python3
"""
简单的递归导入调试脚本
专门观察 import test_a.b.c 的递归过程
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    print("🚀 开始调试递归导入过程")
    print("="*60)
    
    # 清理缓存
    modules_to_clean = ['test_a', 'test_a.b', 'test_a.b.c']
    for mod in modules_to_clean:
        if mod in sys.modules:
            del sys.modules[mod]
            print(f"🧹 清理缓存: {mod}")
    
    print("\n📋 即将执行: python_import_simulation('test_a.b.c')")
    print("📋 预期递归顺序:")
    print("   1. 导入 test_a")
    print("   2. 导入 test_a.b") 
    print("   3. 导入 test_a.b.c")
    print("   4. 返回顶层包 test_a")
    
    print("\n" + "="*60)
    print("🎬 开始执行...")
    print("="*60)
    
    try:
        from python_import_mechanism import python_import_simulation
        result = python_import_simulation('test_a.b.c')
        
        print("\n✅ 导入成功!")
        print(f"🎯 返回结果: {result}")
        print(f"📛 返回模块名: {result.__name__}")
        
        # 检查缓存
        print(f"\n📦 检查 sys.modules:")
        for mod_name in ['test_a', 'test_a.b', 'test_a.b.c']:
            if mod_name in sys.modules:
                print(f"   ✅ {mod_name}: 已缓存")
            else:
                print(f"   ❌ {mod_name}: 未找到")
                
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
