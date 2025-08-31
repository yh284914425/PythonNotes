"""
Python Import机制详细模拟实现
================================

本文档通过一个可运行的Python脚本，详细模拟了Python解释器在执行`import`语句时的
完整内部流程。旨在帮助开发者深入理解Python模块导入的每一个环节。

核心功能:
- 模拟从缓存加载、模块查找、加载到执行的全过程。
- 支持绝对导入、相对导入、包导入、子模块导入等多种场景。
- 详细的控制台输出，实时追踪导入的每一个步骤和决策。
- 包含对关键概念（如sys.modules, sys.meta_path, ModuleSpec, Loader）的模拟和解释。

如何使用:
可以直接运行此文件查看标准库的导入演示，或通过`run_tests.py`运行更全面的测试用例。

"""

import sys
import os
from types import ModuleType
import importlib.machinery

# --- 模拟实现区 ---

def python_import_simulation(module_name, fromlist=None, level=0, globals_dict=None):
    """
    模拟Python内建的`__import__`函数的行为，逐步展示模块导入的全过程。

    这是整个模拟的核心函数，它严格遵循Python官方定义的导入协议(PEP 302)。

    Args:
        module_name (str):
            要导入的模块/包的名称。**此参数不包含相对导入的点标记**。
            例如 `from .foo import bar` 中，`module_name` 是 `'foo'` 而不是 `'.foo'`。

        fromlist (list, optional):
            模拟`from ... import ...`语句。
            - `None` (默认): 对应`import module`语句。
            - `['item']`: 对应`from module import item`。
            - `['*']`: 对应`from module import *`。

        level (int, optional):
            相对导入的点数级别，由解释器根据点标记设置。
            - `0` (默认): 绝对导入。
            - `1`: 单点相对导入 (`from . import ...`)。
            - `2`: 双点相对导入 (`from .. import ...`)。

        globals_dict (dict, optional):
            调用`__import__`处的模块的全局命名空间。
            主要用于相对导入，以确定当前模块所在的包。

    ---
    ### 参数映射关系表

    下表展示了不同的`import`语句如何被“预解析”并映射到此函数的参数：

    | 示例导入语句                      | `module_name` 的值 | `fromlist` 的值      | `level` 的值 |
    | :-------------------------------- | :----------------- | :------------------- | :----------- |
    | **绝对导入**                      |                    |                      |              |
    | `import pkg`                      | `'pkg'`            | `None`               | `0`          |
    | `import pkg.mod`                  | `'pkg.mod'`        | `None`               | `0`          |
    | `from pkg import mod`             | `'pkg'`            | `['mod']`            | `0`          |
    | `from pkg.mod import func`        | `'pkg.mod'`        | `['func']`           | `0`          |
    | `from pkg import *`               | `'pkg'`            | `['*']`              | `0`          |
    | **相对导入** (假设在`a.b`包内) |                    |                      |              |
    | `from . import mod`               | `''` (空字符串)    | `['mod']`            | `1`          |
    | `from .mod import func`            | `'mod'`            | `['func']`           | `1`          |
    | `from .. import sibling`          | `''` (空字符串)    | `['sibling']`        | `2`          |
    | `from ..sibling import func`       | `'sibling'`        | `['func']`           | `2`          |
    ---
    ### 递归视角 (Recursive Perspective)

    本质上，导入过程是一个在模块依赖关系树上进行深度优先遍历的递归算法。
    `python_import_simulation` 函数通过调用自身来模拟这个过程。

    **递归的“基准情形”（停止点）:**
    1.  **缓存命中**: 函数最优先检查`sys.modules`缓存。如果模块已在缓存中，
        则直接返回，递归结束。这是最重要的停止条件，避免了重复加载和无限循环。
    2.  **找到叶子模块**: 成功加载一个没有子模块的实体（如内置模块、单个 .py文件）
        后，当前递归路径也自然结束。

    **递归的“递推步骤”（调用自身）:**
    1.  **层层深入 (加载父包)**: 当导入`a.b.c`时，函数会暂停当前任务，
        先递归调用自身去加载`a`，然后再次递归调用自身去加载`a.b`。
        这个过程确保了子模块的“容器”被依次创建，就像剥洋葱一样，层层深入。

    2.  **横向扩展 (处理`fromlist`)**: 当处理`from os import path`时，
        函数首先加载`os`包。在`handle_fromlist`辅助函数中，它发现`path`
        不是`os`的现有属性，于是会推断`path`可能是一个子模块，并发起一次
        新的递归调用来加载`os.path`。这个过程就像是按图索骥，根据线索
        去查找并加载新的、之前未知的模块。
    ---

    Returns:
        ModuleType:
            成功导入的模块对象。

    Raises:
        ImportError: 当模块找不到、加载失败或发生其他导入相关的错误时抛出。
    """

    print(f"\n[->] 开始导入: '{module_name}'")
    print(f"   参数: fromlist={fromlist}, level={level}")

    # ========================================================================
    # 阶段1: 模块名解析和规范化 (Parsing and Normalization)
    # 目标: 确定要导入模块的“绝对名称”。
    # ========================================================================
    print("\n[1] 阶段1: 模块名解析")

    # 1.1 处理相对导入 (level > 0)
    # 如果是相对导入，需要将其转换为绝对模块名。
    if level > 0:
        # 相对导入必须在包内进行，因此需要知道当前模块属于哪个包。
        current_package = get_current_package(globals_dict)
        if not current_package:
            raise ImportError("相对导入只能在包内使用，因为需要知道当前包的上下文。")

        # 根据level计算基础包路径
        package_parts = current_package.split('.')
        if level > len(package_parts):
            raise ImportError("相对导入级别超出包层次结构。" )

        # level=1 ('.') -> 当前包; level=2 ('..') -> 父包
        if level == 1:
            base_package = current_package
        else:
            # 每多一个level，就从包路径末尾去掉一部分
            base_package = '.'.join(package_parts[:-level + 1])

        # 将相对名和基础包路径拼接成绝对名
        # 如果module_name为空 (例如 from . import xxx)，则目标就是base_package
        absolute_name = f"{base_package}.{module_name}" if module_name else base_package
        print(f"   相对导入转换: '{module_name}' -> '{absolute_name}'")
        module_name = absolute_name

    # 1.2 分解模块名为层次结构，便于后续逐级导入
    name_parts = module_name.split('.')
    print(f"   模块绝对名称: '{module_name}', 层次: {name_parts}")

    # ========================================================================
    # 阶段2: 缓存检查 (Cache Check)
    # 目标: 避免重复加载，提高性能，并解决循环导入问题。
    # ========================================================================
    print("\n[2] 阶段2: 检查模块缓存 (sys.modules)")

    # 2.1 `sys.modules`是所有已加载模块的“花名册”(一个字典)。
    # 如果模块名已在缓存中，直接返回缓存的模块对象。
    if module_name in sys.modules:
        cached_module = sys.modules[module_name]
        print(f"   [OK] 在缓存中找到: '{module_name}'")
        print(f"   缓存对象: {cached_module}")

        # 如果是`from import`，还需要进一步处理fromlist
        if fromlist:
            return handle_fromlist(cached_module, fromlist)
        return cached_module

    # 2.2 对于嵌套模块 (如 a.b.c)，必须先确保其父包 (a, a.b) 已被导入。
    parent_modules = []
    # 遍历除最后一节外的所有部分 (e.g., for 'a.b.c', process 'a' and 'a.b')
    for i in range(len(name_parts) - 1):
        parent_name = '.'.join(name_parts[:i + 1])
        if parent_name in sys.modules:
            parent_modules.append((parent_name, sys.modules[parent_name]))
            print(f"   [PKG] 父包已缓存: '{parent_name}'")
        else:
            # 如果父包不在缓存中，递归调用本函数来导入它。
            print(f"   [CACHE] 需要先导入父包: '{parent_name}'")
            try:
                python_import_simulation(parent_name)  # 导入父包
                # 检查递归调用是否真的成功了
                parent_module = sys.modules.get(parent_name)
                if parent_module is None:
                    raise ImportError(f"递归导入父包 '{parent_name}' 失败：模块未在缓存中")
                parent_modules.append((parent_name, parent_module))
            except ImportError:
                # 递归导入失败，重新抛出更有意义的错误
                raise ImportError(f"无法导入 '{module_name}'：父包 '{parent_name}' 导入失败")

    # ========================================================================
    # 阶段3: 模块查找 (Finding)
    # 目标: 在文件系统中找到模块，并获取其“模块规范(Module Spec)”。
    # ========================================================================
    print("\n[3] 阶段3: 模块查找")

    module_spec = None

    # 3.1 模拟Python的`sys.meta_path`机制。
    # `sys.meta_path`是一个查找器(Finder)列表，Python会依次尝试它们。
    # 常见的查找器有 BuiltinImporter, FrozenImporter, PathFinder。
    
    # 首先检查是否是内置模块
    if module_name in sys.builtin_module_names:
        print(f"   [OK] 找到内置模块: '{module_name}'")
        # 内置模块的处理需要特殊逻辑
        return _handle_builtin_module(module_name)

    # 对于子模块，优先使用父包的搜索路径
    if len(name_parts) > 1 and parent_modules:
        print(f"   [SUBMODULE] 优先在父包路径中查找子模块")
        search_paths = determine_search_paths(name_parts, parent_modules)
        print(f"   在父包路径中搜索: {search_paths[:3]}...")
        module_spec = find_in_paths(module_name, search_paths)

        if module_spec:
            print(f"   [OK] 在父包路径中找到: '{module_spec.name}' at {module_spec.origin}")
        else:
            print(f"   [INFO] 父包路径中未找到，继续使用系统查找器")

    # 如果在父包路径中没找到，或者不是子模块，则使用系统查找器
    if not module_spec:
        # 模拟遍历`sys.meta_path`中的查找器
        for finder in sys.meta_path:
            finder_name = finder.__class__.__name__
            # print(f"   尝试查找器: {finder_name}") # 此处输出过于冗长，故注释
            try:
                # 每个查找器都有`find_spec`方法，尝试查找模块规范
                spec = finder.find_spec(module_name)
                if spec:
                    module_spec = spec
                    print(f"   [OK] 找到模块规范(Spec): '{spec.name}' at {spec.origin}")
                    break # 找到即停止
            except Exception as e:
                print(f"   [FAIL] 查找器 {finder_name} 失败: {e}")
                continue

    # 3.2 如果所有`meta_path`查找器都失败了，则回退到我们简化的路径查找。
    # 真实的Python在这里会由`PathFinder`处理`sys.path`。
    if not module_spec:
        # 确定搜索路径：优先用父包的`__path__`，否则用`sys.path`
        search_paths = determine_search_paths(name_parts, parent_modules)
        print(f"   在以下路径中搜索: {search_paths[:3]}...")
        module_spec = find_in_paths(module_name, search_paths)

    # 3.3 如果最终还是没找到，导入失败。
    if not module_spec:
        raise ImportError(f"No module named '{module_name}'")

    # ========================================================================
    # 阶段4: 模块创建和加载 (Loading)
    # 目标: 根据Spec创建模块对象，并准备执行。
    # ========================================================================
    print("\n[4] 阶段4: 模块创建和加载")

    # 4.1 创建一个空的模块对象
    # Spec中的加载器(loader)可能自定义了模块创建方法。
    if module_spec.loader is None:
        # 如果没有加载器，通常是命名空间包(Namespace Package)。
        module = create_namespace_module(module_spec)
    else:
        # 尝试让加载器创建模块
        module = module_spec.loader.create_module(module_spec)
        if module is None:
            # 如果加载器没有`create_module`或返回None，则使用默认方式创建。
            module = ModuleType(module_name)

    # 4.2 设置模块的基本属性，如__name__, __file__, __package__等。
    # 这一步在模块代码执行前完成，至关重要。
    setup_module_attributes(module, module_spec)
    print(f"   创建模块对象: {module}")
    print(f"   模块属性: __name__='{getattr(module, '__name__', None)}'")
    print(f"            __file__='{getattr(module, '__file__', None)}'")
    print(f"            __package__='{getattr(module, '__package__', None)}'")

    # 4.3 **【核心机制】** 在执行模块代码前，提前将模块放入缓存。
    # 这是Python解决循环导入问题的关键！
    # 如果在执行本模块代码时，有其他模块反过来导入本模块，
    # 它们将从`sys.modules`中获取到这个“不完整”的模块对象，而不是无限递归。
    sys.modules[module_name] = module
    print(f"   [CACHE] 提前缓存模块 (防止循环导入)")

    # ========================================================================
    # 阶段5: 模块执行 (Execution)
    # 目标: 运行模块的顶层代码，填充模块的命名空间。
    # ========================================================================
    print("\n[5] 阶段5: 模块执行")

    try:
        # 5.1 加载器(loader)的`exec_module`方法负责执行模块代码。
        if module_spec.loader and hasattr(module_spec.loader, 'exec_module'):
            print(f"   开始执行模块代码...")
            # `exec_module`会读取`.py`文件内容，并在`module`的`__dict__`中执行。
            # 所有顶层代码（变量赋值、函数/类定义、其他import语句）都在此发生。
            module_spec.loader.exec_module(module)
            print(f"   [OK] 模块执行完成")
        else:
            print(f"   [WARN] 无加载器或无执行方法，跳过执行。")

    except Exception as e:
        # 5.2 如果执行失败，必须将之前放入缓存的“损坏”模块移除。
        print(f"   [FAIL] 模块执行失败: {e}")
        if module_name in sys.modules:
            del sys.modules[module_name]
        raise ImportError(f"执行模块 '{module_name}' 时出错: {e}")

    # ========================================================================
    # 阶段6: 后处理和返回 (Post-processing)
    # 目标: 处理`fromlist`，并返回正确的对象给调用者。
    # ========================================================================
    print("\n[6] 阶段6: 后处理和返回")

    # 6.1 对于子模块导入(a.b.c)，需要将子模块(c)绑定为父包(b)的属性。
    if '.' in module_name:
        parent_name, _, submodule_name = module_name.rpartition('.')
        parent_module = sys.modules.get(parent_name)
        if parent_module:
            setattr(parent_module, submodule_name, module)
            print(f"   设置父包属性: {parent_name}.{submodule_name}")
        else:
            # 这种情况不应该发生，如果发生说明有bug
            raise ImportError(f"无法绑定子模块 '{submodule_name}' 到父包 '{parent_name}'：父包不在缓存中")

    # 6.2 处理`from module import item`语句
    if fromlist:
        print(f"   处理from import: {fromlist}")
        # `handle_fromlist`会确保`fromlist`中的每一项都存在，
        # 如果某项是子模块，会触发对该子模块的导入。
        return handle_fromlist(module, fromlist)

    # 6.3 对于`import a.b.c`，返回的是顶层包`a`。
    # 这是`import`语句的一个重要特性。
    if '.' in module_name:
        top_level_name = name_parts[0]
        result_module = sys.modules[top_level_name]
        print(f"   返回顶层包: '{top_level_name}'")
        return result_module

    # 6.4 对于`import a`，直接返回模块`a`。
    print(f"   [OK] 导入完成，返回模块: {module}")
    return module

# --- 辅助函数区 ---

def setup_module_attributes(module, spec):
    """
    根据模块规范(Spec)为新创建的模块对象设置标准属性。
    这个函数在模块代码执行前被调用。
    """
    module.__name__ = spec.name
    module.__spec__ = spec
    module.__loader__ = spec.loader
    
    if spec.origin:
        module.__file__ = spec.origin

    # `submodule_search_locations`是判断一个模块是否为包的关键。
    # 它的值会成为包的`__path__`属性。
    if spec.submodule_search_locations is not None:
        # --- 这是一个包 ---
        module.__path__ = spec.submodule_search_locations
        # 包的`__package__`属性等于其`__name__`。
        # 这使得在`__init__.py`中可以使用`from . import ...`
        module.__package__ = spec.name
    else:
        # --- 这是一个普通模块 ---
        if '.' in spec.name:
            # 包内模块的`__package__`是其父包的名称。
            module.__package__ = spec.name.rpartition('.')[0]
        else:
            # 顶层模块不属于任何包。
            module.__package__ = None

def _handle_builtin_module(module_name):
    """
    处理内置模块的特殊逻辑。
    内置模块不需要经过完整的导入流程，直接使用系统的导入机制。
    """
    print(f"   [BUILTIN] 使用系统机制导入内置模块: {module_name}")

    # 检查是否已经在缓存中
    if module_name in sys.modules:
        print(f"   [CACHE] 内置模块已在缓存中: {module_name}")
        return sys.modules[module_name]

    # 使用系统的内置导入器
    try:
        import importlib
        module = importlib.import_module(module_name)
        print(f"   [OK] 内置模块导入成功: {module}")
        return module
    except ImportError as e:
        raise ImportError(f"Failed to import builtin module '{module_name}': {e}")


def determine_search_paths(name_parts, parent_modules):
    """
    确定用于查找模块的路径列表。
    - 如果是子模块，优先使用其父包的`__path__`属性。
    - 否则，使用全局的`sys.path`。
    """
    if parent_modules:
        parent_name, parent_module = parent_modules[-1]
        if hasattr(parent_module, '__path__') and parent_module.__path__:
            print(f"   使用父包 '{parent_name}' 的搜索路径")
            return parent_module.__path__
    return sys.path

def find_in_paths(module_name, search_paths):
    """
    一个简化的`PathFinder`，在指定路径中查找模块并创建Spec。
    """
    name_parts = module_name.split('.')
    module_basename = name_parts[-1]
    
    for path in search_paths:
        # 1. 尝试作为普通模块文件查找 (.py)
        py_file = os.path.join(path, module_basename + '.py')
        if os.path.isfile(py_file):
            print(f"   在路径中找到文件: {py_file}")
            return create_file_spec(module_name, py_file)
        
        # 2. 尝试作为包目录查找 (包含__init__.py)
        pkg_dir = os.path.join(path, module_basename)
        init_file = os.path.join(pkg_dir, '__init__.py')
        if os.path.isdir(pkg_dir) and os.path.isfile(init_file):
            print(f"   在路径中找到包: {pkg_dir}")
            return create_package_spec(module_name, init_file, [pkg_dir])
    
    return None

def handle_fromlist(module, fromlist):
    """
    处理`from module import item1, item2`中的`fromlist`。
    """
    # 遍历`fromlist`中的每一项
    for item in fromlist:
        if item == '*':
            # 对于`from module import *`，导入`__all__`中定义的或所有非下划线开头的属性。
            # 注意：这并不会真的在当前命名空间创建变量，只是一个模拟过程。
            handle_star_import(module)
        else:
            # 检查`item`是否是`module`的一个属性。
            if not hasattr(module, item):
                # 如果不是，它可能是一个需要被导入的子模块。
                # 例如 `from os import path`，`path`是`os`的子模块。
                if hasattr(module, '__path__'): # 只有包才能有子模块
                    submodule_name = f"{module.__name__}.{item}"
                    try:
                        # 递归导入这个子模块
                        python_import_simulation(submodule_name)
                    except ImportError:
                        # 如果导入失败，说明它确实只是一个不存在的属性，而不是子模块。
                        # Python的真实行为会在这里抛出ImportError，但为了模拟简化，我们忽略。
                        pass
    return module

def handle_star_import(module):
    """处理`from module import *`"""
    if hasattr(module, '__all__'):
        items = module.__all__
    else:
        items = [name for name in dir(module) if not name.startswith('_')]
    print(f"   [*] 星号导入项目: {items}")
    return items

def get_current_package(globals_dict=None):
    """
    从`globals()`字典中获取当前包的名称。
    这是进行相对导入计算的基础。
    """
    if globals_dict and '__package__' in globals_dict:
        package = globals_dict['__package__']
        if package:
            return package
    if globals_dict and '__name__' in globals_dict:
        name = globals_dict['__name__']
        if '.' in name:
            return name.rpartition('.')[0]
    return None

# --- 模拟加载器和Spec创建函数 ---

def create_file_spec(name, filepath):
    """为普通.py文件创建一个简化的模块规范(Spec)和加载器(Loader)。"""
    class FileLoader:
        def create_module(self, spec): return None # 使用默认创建
        def exec_module(self, module):
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            # 在模块的命名空间中执行代码
            exec(code, module.__dict__)

    return importlib.machinery.ModuleSpec(
        name=name,
        loader=FileLoader(),
        origin=filepath
    )

def create_package_spec(name, init_file, search_locations):
    """为包创建一个简化的模块规范(Spec)和加载器(Loader)。"""
    class PackageLoader:
        def create_module(self, spec):
            # spec 参数在这里不需要使用，返回 None 表示使用默认创建
            return None
        def exec_module(self, module):
            with open(init_file, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(code, module.__dict__)

    spec = importlib.machinery.ModuleSpec(
        name=name,
        loader=PackageLoader(),
        origin=init_file,
        is_package=True # 标记这是一个包
    )
    # 这是关键：设置子模块的搜索路径，它将成为包的`__path__`属性。
    spec.submodule_search_locations = search_locations
    return spec

def create_namespace_module(spec):
    """创建一个命名空间包的模块对象。"""
    module = ModuleType(spec.name)
    # 命名空间包没有`__file__`，但有`__path__`。
    module.__path__ = spec.submodule_search_locations
    module.__spec__ = spec
    module.__loader__ = None
    module.__package__ = spec.name
    return module

# --- 演示区 ---

if __name__ == "__main__":
    print("=" * 60)
    print("Python Import机制详细模拟演示")
    print("=" * 60)
    
    try:
        print("\n【演示1: 导入标准库模块 'json'】")
        json_module = python_import_simulation('json')

        print("\n【演示2: 导入包的子模块 'urllib.parse'】")
        parse_module = python_import_simulation('urllib.parse')

        print("\n【演示3: from 'os' import 'path'】")
        os_module = python_import_simulation('os', fromlist=['path'])

    except Exception as e:
        print(f"演示过程中出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("模拟演示完成")
    print("=" * 60)
