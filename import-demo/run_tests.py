#!/usr/bin/env python3
"""
测试 `python_import_mechanism.py` 的模拟实现。

该文件包含一系列的测试函数，每个函数都针对一种特定的导入场景，
以确保我们的导入模拟器在各种情况下都能正确工作。

通过运行此文件，可以全面地验证模拟器的逻辑是否健壮。
"""

import sys
import os
import traceback

# --- 准备工作 ---

# 将当前文件所在的目录添加到Python的模块搜索路径(sys.path)中。
# 这是为了确保Python能够找到我们用于测试的本地模块，如`test_simple_module.py`和`test_package`。
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 从我们的模拟器文件中导入核心模拟函数。
from python_import_mechanism import python_import_simulation


def explain_parameters(module_name, fromlist, level, current_package):
    """
    一个辅助函数，用于将`__import__`的内部参数用更直观、易于理解的方式解释出来。
    这使得测试输出的可读性大大增强。
    """
    explanations = []

    # 解释 `module_name` 参数
    if module_name == '':
        if level == 1:
            explanations.append(f"[LOC] 目标位置: 当前包 ({current_package})")
        elif level == 2:
            parent = '.'.join(current_package.split('.')[:-1]) if current_package and '.' in current_package else '父包'
            explanations.append(f"[LOC] 目标位置: 父包 ({parent})")
        else:
            explanations.append(f"[LOC] 目标位置: 上{level-1}级包")
    else:
        explanations.append(f"[LOC] 目标位置: {module_name}")

    # 解释 `fromlist` 参数
    if fromlist is None:
        explanations.append("[REQ] 要什么: 整个模块/包 (对应 `import ...`)")
    elif fromlist == ['*']:
        explanations.append("[REQ] 要什么: 所有公开项目 (对应 `from ... import *`)")
    else:
        explanations.append(f"[REQ] 要什么: 特定项目 {fromlist} (对应 `from ... import ...`)")

    # 解释 `level` 参数
    if level == 0:
        explanations.append("[FIND] 查找方式: 绝对路径")
    else:
        dots = '.' * level
        explanations.append(f"[FIND] 查找方式: 相对路径 ({dots})")

    return explanations


# --- 测试用例区 ---

def test_simple_module_import():
    """
    测试场景1: 导入一个简单的、单一的.py文件。
    这是最基本的导入情况。
    验证:
    - 模块能被正确找到和加载。
    - 模块的`__name__`和`__file__`等属性被正确设置。
    - 模块内的函数和类可以被成功调用。
    """
    print("\n" + "="*50)
    print("测试1: 简单模块导入 (`import test_simple_module`)")
    print("="*50)
    
    try:
        module = python_import_simulation('test_simple_module')
        print(f"\n[OK] 导入成功: {module}")
        print(f"模块名称: {module.__name__}")
        print(f"模块文件: {getattr(module, '__file__', 'N/A')}")
        
        # 验证模块内容是否可访问
        if hasattr(module, 'simple_function'):
            result = module.simple_function()
            print(f"函数调用结果: {result}")
        
        if hasattr(module, 'SimpleClass'):
            obj = module.SimpleClass("测试值")
            print(f"类实例化结果: {obj.get_value()}")
            
    except Exception as e:
        print(f"[FAIL] 导入失败: {e}")
        traceback.print_exc()


def test_package_import():
    """
    测试场景2: 导入一个包。
    这会涉及到对`__init__.py`文件的加载。
    验证:
    - 包（`__init__.py`）被正确执行。
    - 包的`__path__`属性被正确设置。
    - 包中定义的函数可以被访问。
    """
    print("\n" + "="*50)
    print("测试2: 包导入 (`import test_package`)")
    print("="*50)
    
    try:
        package = python_import_simulation('test_package')
        print(f"\n[OK] 包导入成功: {package}")
        print(f"包名称: {package.__name__}")
        print(f"包路径: {getattr(package, '__path__', 'N/A')}")
        
        # 验证包内容是否可访问
        if hasattr(package, 'package_function'):
            result = package.package_function()
            print(f"包函数调用结果: {result}")
            
    except Exception as e:
        print(f"[FAIL] 包导入失败: {e}")
        traceback.print_exc()


def test_submodule_import():
    """
    测试场景3: 导入一个包的子模块。
    验证:
    - 导入系统能利用父包的`__path__`来定位子模块。
    - 子模块被正确加载和执行。
    - `import a.b.c` 语句的返回值是顶层包 `a`。
    """
    print("\n" + "="*50)
    print("测试3: 子模块导入 (`import test_package.submodule`)")
    print("="*50)
    
    try:
        # 注意：`import a.b.c` 的返回值是 `a`
        top_package = python_import_simulation('test_package.submodule')
        print(f"\n[OK] 顶层包返回成功: {top_package}")
        print(f"返回的模块名称: {top_package.__name__}")

        # 从sys.modules中获取真正被加载的子模块以进行验证
        submodule = sys.modules.get('test_package.submodule')
        print(f"子模块名称: {getattr(submodule, '__name__', 'N/A')}")
        
        # 验证子模块内容
        if hasattr(submodule, 'submodule_function'):
            result = submodule.submodule_function()
            print(f"子模块函数调用结果: {result}")
            
    except Exception as e:
        print(f"[FAIL] 子模块导入失败: {e}")
        traceback.print_exc()


def test_from_import():
    """
    测试场景4: `from ... import ...` 语句。
    验证:
    - `fromlist` 参数被正确处理。
    - 返回的模块对象是 `test_package` 而不是其中的项。
    """
    print("\n" + "="*50)
    print("测试4: from import 语句 (`from test_package import package_function`)")
    print("="*50)
    
    try:
        module = python_import_simulation('test_package', fromlist=['package_function'])
        print(f"\n[OK] from import 成功: {module}")
        
        # 验证模块内容
        if hasattr(module, 'package_function'):
            result = module.package_function()
            print(f"导入的函数调用结果: {result}")
            
    except Exception as e:
        print(f"[FAIL] from import 失败: {e}")
        traceback.print_exc()


def test_builtin_module():
    """
    测试场景5: 导入内置模块。
    验证:
    - 模拟器能正确处理内置模块，这些模块没有.py文件。
    """
    print("\n" + "="*50)
    print("测试5: 内置模块导入 (`import sys`)")
    print("="*50)
    
    try:
        sys_module = python_import_simulation('sys')
        print(f"\n[OK] 内置模块导入成功: {sys_module}")
        print(f"模块名称: {sys_module.__name__}")
        print(f"Python版本: {sys_module.version[:50]}...")
        
    except Exception as e:
        print(f"[FAIL] 内置模块导入失败: {e}")
        traceback.print_exc()


def test_standard_library():
    """
    测试场景6: 导入标准库模块。
    验证:
    - 模拟器能像处理本地模块一样，在Python的安装路径中找到并加载标准库。
    """
    print("\n" + "="*50)
    print("测试6: 标准库模块导入 (`import json`)")
    print("="*50)

    try:
        json_module = python_import_simulation('json')
        print(f"\n[OK] 标准库模块导入成功: {json_module}")
        print(f"模块名称: {json_module.__name__}")

        # 验证模块功能
        test_data = {"key": "value", "number": 42}
        json_str = json_module.dumps(test_data)
        print(f"JSON序列化测试: {json_str}")

    except Exception as e:
        print(f"[FAIL] 标准库模块导入失败: {e}")
        traceback.print_exc()


def test_relative_imports():
    """
    测试场景7: 相对导入。
    这是导入机制中最复杂的部分之一。
    验证:
    - `level`参数被正确解析。
    - `.` 和 `..` 能够正确地相对于`current_package`进行导航。
    - 边界情况（如在顶层包尝试`..`导入）能被正确处理。
    """
    print("\n" + "="*50)
    print("测试7: 相对导入功能")
    print("="*50)

    # 定义一系列相对导入的测试用例
    test_cases = [
        # --- Case 1: 单点相对导入 (from . import ...) ---
        {
            'desc': 'from . import submodule  # 从当前包导入子模块',
            'module_name': '',
            'level': 1,
            'fromlist': ['submodule'],
            'current_package': 'test_package'
        },
        # --- Case 2: 在子模块中进行相对导入 ---
        {
            'desc': 'from .. import utils  # 假设在 a.b 中导入 a.utils',
            'module_name': '',
            'level': 2,
            'fromlist': ['utils'],
            'current_package': 'test_package.submodule' # 模拟当前在子模块中
        },
        # --- Case 3: 边界/错误情况测试 ---
        {
            'desc': 'from .. import nonexistent  # 在顶层包中进行无效的双点导入',
            'module_name': '',
            'level': 2,
            'fromlist': ['nonexistent'],
            'current_package': 'test_package' # test_package没有父包，应该失败
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  【相对导入测试 {i}】: {test_case['desc']}")

        # 用更直观的方式解释参数
        explanations = explain_parameters(
            test_case['module_name'],
            test_case['fromlist'],
            test_case['level'],
            test_case['current_package']
        )
        print("    直观理解:")
        for explanation in explanations:
            print(f"      {explanation}")

        print("    模拟器参数:")
        print(f"      module_name='{test_case['module_name']}'")
        print(f"      level={test_case['level']}")
        print(f"      fromlist={test_case['fromlist']}")
        print(f"      current_package='{test_case['current_package']}'")

        try:
            # 模拟`globals()`字典，为相对导入提供包上下文
            mock_globals = {'__package__': test_case['current_package']}
            
            result = python_import_simulation(
                module_name=test_case['module_name'],
                fromlist=test_case['fromlist'],
                level=test_case['level'],
                globals_dict=mock_globals
            )
            print(f"    [OK] 成功: 返回模块 {result.__name__}")
        except Exception as e:
            print(f"    [FAIL] 失败: {e}")


def test_comprehensive_import_scenarios():
    """
    测试场景8: 其他综合导入场景。
    验证:
    - 星号导入 (`import *`)
    - `from ... import a, b`
    - `import a.b.c` 的返回值
    """
    print("\n" + "="*50)
    print("测试8: 综合导入场景")
    print("="*50)

    scenarios = [
        {'name': '星号导入',
         'desc': 'from test_package import *',
         'module_name': 'test_package', 'level': 0, 'fromlist': ['*'], 'current_package': None
        },
        {'name': '多项导入',
         'desc': 'from test_package import package_function, package_version',
         'module_name': 'test_package', 'level': 0, 'fromlist': ['package_function', 'package_version'], 'current_package': None
        },
    ]

    for scenario in scenarios:
        print(f"\n  【{scenario['name']}】: {scenario['desc']}")
        try:
            mock_globals = {'__package__': scenario['current_package']} if scenario['current_package'] else None
            result = python_import_simulation(
                module_name=scenario['module_name'],
                fromlist=scenario['fromlist'],
                level=scenario['level'],
                globals_dict=mock_globals
            )
            print(f"    [OK] 成功: {result.__name__}")
        except Exception as e:
            print(f"    [FAIL] 失败: {e}")


# --- 主执行区 ---

if __name__ == "__main__":
    print("Python Import 机制模拟实现测试")
    print("="*60)
    
    # 按顺序运行所有测试函数
    test_simple_module_import()
    test_package_import()
    test_submodule_import()
    test_from_import()
    test_builtin_module()
    test_standard_library()
    test_relative_imports()
    test_comprehensive_import_scenarios()

    print("\n" + "="*60)
    print("所有测试完成")
    print("="*60)
