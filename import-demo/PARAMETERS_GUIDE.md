# Python Import 参数详解

## 🎯 核心函数签名

```python
python_import_simulation(module_name, fromlist=None, level=0, globals_dict=None)
```

## 📋 参数详解

### 1. `module_name` (str)
**要导入的模块名**

| 导入类型 | 示例 | module_name 值 | 说明 |
|---------|------|---------------|------|
| 绝对导入模块 | `import json` | `'json'` | 直接模块名 |
| 绝对导入包 | `import test_package` | `'test_package'` | 包名 |
| 绝对导入子模块 | `import os.path` | `'os.path'` | 完整路径 |
| 相对导入当前包 | `from . import func` | `''` | 空字符串表示当前包 |
| 相对导入子模块 | `from .sub import func` | `'sub'` | 子模块名 |
| 相对导入父包 | `from .. import func` | `''` | 空字符串表示父包 |

### 2. `fromlist` (list or None)
**from语句中要导入的具体项目**

| 导入语句 | fromlist 值 | 说明 |
|---------|-------------|------|
| `import module` | `None` | 普通import |
| `from module import func` | `['func']` | 导入单个项目 |
| `from module import func, var` | `['func', 'var']` | 导入多个项目 |
| `from module import *` | `['*']` | 星号导入 |

### 3. `level` (int)
**相对导入的级别**

| level | 语法 | 含义 | 示例 |
|-------|------|------|------|
| `0` | 无点 | 绝对导入 | `import json` |
| `1` | `.` | 当前包 | `from . import func` |
| `2` | `..` | 父包 | `from .. import func` |
| `3` | `...` | 祖父包 | `from ... import func` |

### 4. `current_package` (str or None)
**当前模块所在的包路径**

| 当前位置 | current_package | 说明 |
|---------|----------------|------|
| 顶层模块 | `None` | 不在任何包内 |
| 包根目录 | `'mypackage'` | 在包的__init__.py中 |
| 子模块 | `'mypackage.submodule'` | 在包的子模块中 |
| 深层嵌套 | `'a.b.c.d'` | 在深层嵌套包中 |

## 🔍 实际场景映射

### 场景1: 在包的__init__.py中
```python
# 文件: mypackage/__init__.py
# current_package = 'mypackage'

from . import utils          # level=1, module_name='utils'
from .submodule import func  # level=1, module_name='submodule'
```

### 场景2: 在子模块中
```python
# 文件: mypackage/submodule.py  
# current_package = 'mypackage'

from . import utils          # level=1, module_name='utils' (兄弟模块)
from .. import parent_func   # level=2, module_name='' (父包)
```

### 场景3: 在深层嵌套中
```python
# 文件: mypackage/sub1/sub2/module.py
# current_package = 'mypackage.sub1.sub2'

from . import sibling        # level=1, 当前包 sub2
from .. import parent        # level=2, 父包 sub1  
from ... import grandparent  # level=3, 祖父包 mypackage
```

## 🧪 测试用例解析

### 基础相对导入
```python
{
    'desc': 'from . import package_function',
    'module_name': '',                    # 空字符串 = 当前包
    'level': 1,                          # 单点 = 当前包级别
    'fromlist': ['package_function'],    # 要导入的函数
    'current_package': 'test_package'    # 当前在test_package中
}
```
**等价于**: 在 `test_package` 包内执行 `from . import package_function`

### 子模块相对导入
```python
{
    'desc': 'from .submodule import submodule_function',
    'module_name': 'submodule',          # 当前包下的子模块
    'level': 1,                          # 单点 = 当前包级别
    'fromlist': ['submodule_function'],  # 要导入的函数
    'current_package': 'test_package'    # 当前在test_package中
}
```
**等价于**: 在 `test_package` 包内执行 `from .submodule import submodule_function`

### 父包相对导入
```python
{
    'desc': 'from .. import parent_function',
    'module_name': '',                   # 空字符串 = 父包
    'level': 2,                          # 双点 = 父包级别
    'fromlist': ['parent_function'],     # 要导入的函数
    'current_package': 'parent.child'    # 当前在child包中
}
```
**等价于**: 在 `parent.child` 包内执行 `from .. import parent_function`

## 💡 理解要点

1. **`module_name` 为空字符串**: 表示导入包本身，而不是包内的模块
2. **`level` 决定相对层级**: 点的数量对应level的值
3. **`current_package` 是基准**: 相对导入的计算基础
4. **`fromlist` 决定导入方式**: None表示import，列表表示from import

## ⚠️ 常见错误

1. **相对导入级别超出包层次**
   ```python
   # 错误: 在顶层包中使用双点导入
   current_package = 'mypackage'  # 只有一层
   level = 2                      # 要求两层 -> 错误!
   ```

2. **在非包环境中使用相对导入**
   ```python
   # 错误: 在普通模块中使用相对导入
   current_package = None  # 不在包中
   level = 1              # 相对导入 -> 错误!
   ```

3. **fromlist与导入语句不匹配**
   ```python
   # 错误: import语句使用fromlist
   # import json  应该是 fromlist=None
   fromlist = ['dumps']  # 错误!
   ```
