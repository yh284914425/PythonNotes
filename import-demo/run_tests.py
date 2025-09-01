#!/usr/bin/env python3
"""
测试 `python_import_mechanism.py` 的模拟实现。
该文件采用数据驱动的方式，定义了一系列的测试用例，
然后通过一个统一的运行器来执行和验证。
"""

import sys
import os
import traceback

# --- 准备工作 ---

# 将当前文件所在的目录添加到Python的模块搜索路径(sys.path)中。
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 从我们的模拟器文件中导入核心模拟函数。
from python_import_mechanism import python_import_simulation

# --- 测试用例定义 ---

# 验证函数
def validate_simple_module(module):
    assert module.__name__ == 'test_simple_module'
    assert hasattr(module, 'simple_function')
    print(f"  模块内容验证: {module.simple_function()}")

def validate_package(package):
    assert package.__name__ == 'test_package'
    assert hasattr(package, 'package_function')
    print(f"  包内容验证: {package.package_function()}")

def validate_submodule(top_package):
    assert top_package.__name__ == 'test_package'
    submodule = sys.modules.get('test_package.submodule')
    assert submodule is not None
    assert hasattr(submodule, 'submodule_function')
    print(f"  子模块内容验证: {submodule.submodule_function()}")

def validate_from_import(module):
    assert module.__name__ == 'test_package'
    assert hasattr(module, 'package_function')

def validate_sys_module(module):
    assert module.__name__ == 'sys'

def validate_json_module(module):
    assert module.__name__ == 'json'

def validate_relative_import(module):
    assert module.__name__ == 'test_package'

TEST_CASES = [
    {
        'desc': '1. 简单模块导入: import test_simple_module',
        'params': {'module_name': 'test_simple_module'},
        'validator': validate_simple_module
    },
    {
        'desc': '2. 包导入: import test_package',
        'params': {'module_name': 'test_package'},
        'validator': validate_package
    },
    {
        'desc': '3. 子模块导入: import test_package.submodule',
        'params': {'module_name': 'test_package.submodule'},
        'validator': validate_submodule
    },
    {
        'desc': '4. from ... import: from test_package import package_function',
        'params': {'module_name': 'test_package', 'fromlist': ['package_function']},
        'validator': validate_from_import
    },
    {
        'desc': '5. 内置模块: import sys',
        'params': {'module_name': 'sys'},
        'validator': validate_sys_module
    },
    {
        'desc': '6. 标准库: import json',
        'params': {'module_name': 'json'},
        'validator': validate_json_module
    },
    {
        'desc': '7. 相对导入: from . import submodule',
        'params': {'module_name': '', 'level': 1, 'fromlist': ['submodule'], 'globals_dict': {'__package__': 'test_package'}},
        'validator': validate_relative_import
    },
    {
        'desc': '8. 相对导入: from .. import utils',
        'params': {'module_name': '', 'level': 2, 'fromlist': ['utils'], 'globals_dict': {'__package__': 'test_package.submodule'}},
        'validator': validate_relative_import
    },
    {
        'desc': '9. 边界情况: from .. import nonexistent (预期失败)',
        'params': {'module_name': '', 'level': 2, 'fromlist': ['nonexistent'], 'globals_dict': {'__package__': 'test_package'}},
        'should_fail': True
    },
    {
        'desc': '10. 星号导入: from test_package import *',
        'params': {'module_name': 'test_package', 'fromlist': ['*']},
        'validator': lambda m: m.__name__ == 'test_package'
    }
]

# --- 测试运行器 ---

if __name__ == "__main__":
    print("Python Import 机制模拟实现测试")
    print("="*60)

    all_passed = True
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n--- {case['desc']} ---")

        try:
            # 清理缓存，确保每次测试都是独立的
            if 'test_simple_module' in sys.modules: del sys.modules['test_simple_module']
            if 'test_package.submodule' in sys.modules: del sys.modules['test_package.submodule']
            if 'test_package' in sys.modules: del sys.modules['test_package']

            result = python_import_simulation(**case['params'])

            if case.get('should_fail'):
                print(f"  [FAIL] 预期失败但成功了")
                all_passed = False
            else:
                if case.get('validator'):
                    case['validator'](result)
                print(f"  [PASS] 成功")

        except Exception as e:
            if case.get('should_fail'):
                print(f"  [PASS] 预期失败: {e}")
            else:
                print(f"  [FAIL] 意外失败: {e}")
                traceback.print_exc()
                all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试用例通过!")
    else:
        print("❌ 部分测试用例失败")
    print("="*60)
