# Python Import 机制模拟实现

这个项目提供了一个详细的 Python import 机制模拟实现，展示了 Python 解释器在执行 `import` 语句时的完整内部流程。

## 🎯 项目目标

- **教育目的**: 帮助理解 Python import 的内部工作原理
- **可运行**: 实际可以执行并导入模块
- **详细日志**: 显示每个阶段的详细过程
- **准确模拟**: 遵循真实的 Python import 机制

## 🔧 核心功能

- ✅ **简单模块导入**: `import module`
- ✅ **包导入**: `import package`
- ✅ **子模块导入**: `import package.submodule`
- ✅ **from import**: `from package import item`
- ✅ **相对导入**: `from . import module`, `from .. import module`
- ✅ **内置模块**: `import sys`
- ✅ **标准库模块**: `import json`

## 🚀 使用方法

### 运行测试

```bash
python import-demo/run_tests.py
```

### 手动测试

```python
from python_import_mechanism import python_import_simulation

# 导入简单模块
module = python_import_simulation('test_simple_module')

# 导入包
package = python_import_simulation('test_package')

# 导入子模块
submodule = python_import_simulation('test_package.submodule')

# from import
module = python_import_simulation('test_package', fromlist=['package_function'])

# 相对导入
globals_dict = {'__package__': 'test_package'}
module = python_import_simulation('submodule', level=1, globals_dict=globals_dict)
```

## 🐍 Python 模块导入的完整流程

导入一个模块（例如 `import a.b.c` 或 `from a.b import c`）是一个复杂但精确的过程，可以分为以下六个核心阶段：

### 阶段一：模块名解析和规范化

这是导入过程的第一步，Python 解释器会解析 `import` 语句，确定要导入模块的**绝对名称**。

- **绝对导入** (`import a.b.c`):
    - 模块名就是 `a.b.c`。

- **相对导入** (`from . import c`):
    - Python 会使用当前模块的 `__package__` 属性来确定基础包。
    - 例如，如果在 `a.b` 包中执行 `from . import c`，绝对名称就是 `a.b.c`。
    - `from .. import d` 则会解析为 `a.d`。

### 阶段二：缓存检查 (`sys.modules`)

这是导入机制的核心优化，也是解决循环导入的关键。

- **`sys.modules`**: 这是一个全局字典，存储了所有已加载的模块。
- **检查缓存**: Python 会检查解析出的绝对名称是否已存在于 `sys.modules` 中。
    - **命中**: 如果存在，直接返回缓存中的模块对象，导入过程结束。
    - **未命中**: 继续下一步。

### 阶段三：模块查找 (Finding)

如果模块不在缓存中，Python 需要在文件系统中找到它。

- **`sys.meta_path`**: 这是一个查找器 (Finder) 列表，Python 会依次尝试它们。
    - `BuiltinImporter`: 查找内置模块（如 `sys`, `os`）。
    - `FrozenImporter`: 查找冻结模块（嵌入在可执行文件中的模块）。
    - `PathFinder`: 核心查找器，负责在 `sys.path` 中查找模块。

- **`PathFinder` 的工作流程**:
    1. **确定搜索路径**:
        - 如果是子模块（如 `a.b.c`），优先使用父包 `a.b` 的 `__path__` 属性。
        - 否则，使用全局的 `sys.path`。
    2. **在路径中查找**:
        - **包**: 查找名为 `c` 的目录，且包含 `__init__.py` 文件。
        - **模块**: 查找名为 `c.py` 的文件。
        - **扩展模块**: 查找 `c.so`, `c.pyd` 等。

- **模块规范 (Module Spec)**: 如果找到模块，查找器会返回一个 `ModuleSpec` 对象，其中包含模块的元信息（名称、路径、加载器等）。

### 阶段四：模块创建和加载 (Loading)

找到模块后，需要创建模块对象并准备执行。

1. **创建模块对象**:
    - 根据 `ModuleSpec` 创建一个空的模块对象。

2. **设置模块属性**:
    - 在模块代码执行**之前**，设置 `__name__`, `__file__`, `__package__` 等属性。

3. **提前放入缓存**:
    - **【核心机制】** 在执行模块代码前，将这个“不完整”的模块对象放入 `sys.modules` 缓存。
    - 这是解决循环导入的关键：如果在执行本模块时，有其他模块反过来导入本模块，它们会从缓存中获取到这个不完整的模块对象，而不是无限递归。

### 阶段五：模块执行 (Execution)

这是模块真正被“激活”的阶段。

- **执行代码**: 加载器 (Loader) 的 `exec_module` 方法会读取 `.py` 文件内容，并在模块的 `__dict__` 中执行。
- **填充命名空间**: 所有顶层代码（变量赋值、函数/类定义、其他 `import` 语句）都在此发生。
- **错误处理**: 如果执行失败，必须将之前放入缓存的“损坏”模块从 `sys.modules` 中移除。

### 阶段六：后处理和返回

最后一步是处理 `import` 语句的返回值。

- **子模块绑定**: 对于 `import a.b.c`，需要将子模块 `c` 绑定为父包 `b` 的属性（`b.c`），同时 `b` 也会被绑定为 `a` 的属性。

- **返回值**:
    - `import a.b.c`: 返回的是**顶层包 `a`**。
    - `from a.b import c`: 返回的是**模块 `a.b`**。

- **名称绑定**:
    - `import a.b.c`: 在当前命名空间中绑定 `a`。
    - `from a.b import c`: 在当前命名空间中绑定 `c`。

## 📋 参数详解

| Python 语句 | module_name | level | fromlist | current_package | 说明 |
|-------------|-------------|-------|----------|----------------|------|
| `import json` | `'json'` | `0` | `None` | `None` | 绝对导入模块 |
| `import os.path` | `'os.path'` | `0` | `None` | `None` | 绝对导入子模块 |
| `from json import dumps` | `'json'` | `0` | `['dumps']` | `None` | 绝对from import |
| `from json import *` | `'json'` | `0` | `['*']` | `None` | 星号导入 |
| `from . import func` | `''` | `1` | `['func']` | `'mypackage'` | 当前包导入 |
| `from .module import func` | `'module'` | `1` | `['func']` | `'mypackage'` | 当前包子模块导入 |
| `from .. import func` | `''` | `2` | `['func']` | `'parent.child'` | 父包导入 |
| `from ..sibling import func` | `'sibling'` | `2` | `['func']` | `'parent.child'` | 父包兄弟模块导入 |
