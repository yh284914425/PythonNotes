#!/usr/bin/env python3
"""
验证修复效果的专门测试
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from python_import_mechanism import python_import_simulation

def test_submodule_path_validation():
    """测试子模块路径验证是否正确"""
    print("=" * 60)
    print("测试: 子模块路径验证")
    print("=" * 60)
    
    try:
        # 这应该导入正确的 test_package.utils，而不是系统的 utils
        result = python_import_simulation('test_package.utils')
        
        # 检查导入的模块是否正确
        utils_module = sys.modules.get('test_package.utils')
        if utils_module:
            print(f"\n✅ 成功导入: {utils_module}")
            print(f"模块文件: {getattr(utils_module, '__file__', 'N/A')}")
            
            # 验证这是我们创建的模块，而不是系统模块
            if hasattr(utils_module, 'utility_function'):
                result = utils_module.utility_function()
                print(f"工具函数调用结果: {result}")
                print("✅ 确认导入了正确的 test_package.utils 模块")
            else:
                print("❌ 导入了错误的模块（可能是系统的 utils）")
        else:
            print("❌ 模块未在 sys.modules 中找到")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_relative_import_with_utils():
    """测试相对导入是否使用正确的 utils 模块"""
    print("\n" + "=" * 60)
    print("测试: 相对导入使用正确的 utils 模块")
    print("=" * 60)
    
    try:
        # 模拟从 test_package.submodule 中进行相对导入
        mock_globals = {'__package__': 'test_package.submodule'}
        
        result = python_import_simulation(
            module_name='',
            fromlist=['utils'],
            level=2,  # from .. import utils
            globals_dict=mock_globals
        )
        
        print(f"✅ 相对导入成功: {result}")
        
        # 验证 utils 模块是否正确
        utils_module = sys.modules.get('test_package.utils')
        if utils_module and hasattr(utils_module, 'utility_function'):
            print("✅ 相对导入使用了正确的 test_package.utils 模块")
        else:
            print("❌ 相对导入使用了错误的模块")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("验证修复效果的专门测试")
    print("=" * 60)
    
    test_submodule_path_validation()
    test_relative_import_with_utils()
    
    print("\n" + "=" * 60)
    print("修复验证测试完成")
    print("=" * 60)
