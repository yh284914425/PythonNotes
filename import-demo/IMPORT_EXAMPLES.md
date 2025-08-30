# Python Import 语句与参数对照表

## 📋 完整对照表

| Python 语句 | module_name | level | fromlist | current_package | 说明 |
|-------------|-------------|-------|----------|----------------|------|
| `import json` | `'json'` | `0` | `None` | `None` | 绝对导入模块 |
| `import os.path` | `'os.path'` | `0` | `None` | `None` | 绝对导入子模块 |
| `from json import dumps` | `'json'` | `0` | `['dumps']` | `None` | 绝对from import |
| `from json import dumps, loads` | `'json'` | `0` | `['dumps', 'loads']` | `None` | 多项导入 |
| `from json import *` | `'json'` | `0` | `['*']` | `None` | 星号导入 |
| `from . import func` | `''` | `1` | `['func']` | `'mypackage'` | 当前包导入 |
| `from .module import func` | `'module'` | `1` | `['func']` | `'mypackage'` | 当前包子模块导入 |
| `from .. import func` | `''` | `2` | `['func']` | `'parent.child'` | 父包导入 |
| `from ..sibling import func` | `'sibling'` | `2` | `['func']` | `'parent.child'` | 父包兄弟模块导入 |
| `from ... import func` | `''` | `3` | `['func']` | `'a.b.c'` | 祖父包导入 |

## 🎯 实际测试用例

### 1. 绝对导入系列
```python
# import json
{
    'module_name': 'json',
    'level': 0,
    'fromlist': None,
    'current_package': None
}

# from json import dumps
{
    'module_name': 'json', 
    'level': 0,
    'fromlist': ['dumps'],
    'current_package': None
}

# from json import dumps, loads
{
    'module_name': 'json',
    'level': 0, 
    'fromlist': ['dumps', 'loads'],
    'current_package': None
}
```

### 2. 相对导入系列 (在 mypackage 包内)
```python
# from . import utils
{
    'module_name': '',              # 空字符串表示当前包
    'level': 1,                     # 单点
    'fromlist': ['utils'],
    'current_package': 'mypackage'
}

# from .submodule import func
{
    'module_name': 'submodule',     # 子模块名
    'level': 1,                     # 单点
    'fromlist': ['func'],
    'current_package': 'mypackage'
}
```

### 3. 多级相对导入 (在 parent.child 包内)
```python
# from .. import parent_func
{
    'module_name': '',              # 空字符串表示父包
    'level': 2,                     # 双点
    'fromlist': ['parent_func'],
    'current_package': 'parent.child'
}

# from ..sibling import func
{
    'module_name': 'sibling',       # 父包下的兄弟模块
    'level': 2,                     # 双点
    'fromlist': ['func'],
    'current_package': 'parent.child'
}
```

## 🔍 参数理解技巧

### level 参数规律
- `level = 点的数量`
- `0` = 无点 = 绝对导入
- `1` = 一个点 (`.`) = 当前包
- `2` = 两个点 (`..`) = 父包
- `3` = 三个点 (`...`) = 祖父包

### module_name 规律
- **绝对导入**: 完整模块路径 (`'json'`, `'os.path'`)
- **相对导入当前包**: 空字符串 (`''`)
- **相对导入子模块**: 子模块名 (`'submodule'`)

### fromlist 规律
- **import 语句**: `None`
- **from import 语句**: 列表 (`['item1', 'item2']`)
- **星号导入**: `['*']`

### current_package 规律
- **绝对导入**: `None` (不需要)
- **相对导入**: 当前模块所在包的完整路径

## 🧪 测试验证

你可以用这些参数组合来测试不同的导入场景：

```python
from python_import_mechanism import python_import_simulation

# 测试绝对导入
result = python_import_simulation('json', None, 0, None)

# 测试相对导入
globals_dict = {'__package__': 'test_package'}
result = python_import_simulation('', 1, ['package_function'], globals_dict)

# 测试from import
result = python_import_simulation('json', ['dumps'], 0, None)
```

## ⚠️ 常见错误对照

| 错误场景 | 错误参数 | 正确参数 | 说明 |
|---------|---------|---------|------|
| import语句用fromlist | `fromlist=['item']` | `fromlist=None` | import不需要fromlist |
| 相对导入无current_package | `current_package=None` | `current_package='pkg'` | 相对导入必须有包信息 |
| level超出包层次 | `level=3, current_package='pkg'` | `level=1` | 包层次不够 |
| 绝对导入用level | `level=1, module_name='json'` | `level=0` | 绝对导入level=0 |
