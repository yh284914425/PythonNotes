# 07-发布到PyPI

## 🌐 PyPI简介

### 什么是PyPI？
PyPI（Python Package Index）是Python官方的第三方包仓库，是Python生态系统的核心组成部分。

### PyPI的重要性
```python
pypi_importance = {
    "中央仓库": "Python包的官方分发中心",
    "全球访问": "全世界开发者都可以访问",
    "自动安装": "pip默认从PyPI安装包",
    "版本管理": "支持多版本并存",
    "依赖解析": "自动处理包依赖关系",
    "社区驱动": "开源社区维护和使用"
}
```

### PyPI vs TestPyPI
```python
pypi_comparison = {
    "PyPI": {
        "用途": "正式发布生产环境包",
        "地址": "https://pypi.org/",
        "特点": "永久存储，不可删除版本",
        "用户": "全球Python开发者"
    },
    "TestPyPI": {
        "用途": "测试包发布流程",
        "地址": "https://test.pypi.org/",
        "特点": "测试环境，可以删除",
        "用户": "包开发者测试使用"
    }
}
```

## 🔐 账户准备

### 注册PyPI账户
```bash
# 1. 访问 https://pypi.org/account/register/
# 2. 填写用户名、邮箱、密码
# 3. 验证邮箱
# 4. 启用双因素认证（推荐）

# 同样注册TestPyPI账户
# 访问 https://test.pypi.org/account/register/
```

### API Token配置
```bash
# 1. 登录PyPI，进入Account settings
# 2. 创建API Token
# 3. 配置本地认证

# 方法1：使用.pypirc文件
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
EOF

# 设置文件权限
chmod 600 ~/.pypirc
```

### 环境变量配置
```bash
# 方法2：使用环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here

# 或者在.bashrc/.zshrc中添加
echo 'export TWINE_USERNAME=__token__' >> ~/.bashrc
echo 'export TWINE_PASSWORD=pypi-your-api-token-here' >> ~/.bashrc
```

## 📤 发布工具

### twine - 官方发布工具
```bash
# 安装twine
pip install twine

# 基本发布命令
twine upload dist/*

# 发布到TestPyPI
twine upload --repository testpypi dist/*

# 检查包
twine check dist/*

# 详细输出
twine upload --verbose dist/*

# 跳过已存在的文件
twine upload --skip-existing dist/*
```

### twine配置选项
```bash
# 指定仓库
twine upload --repository pypi dist/*
twine upload --repository testpypi dist/*

# 指定配置文件
twine upload --config-file ~/.pypirc dist/*

# 非交互模式
twine upload --non-interactive dist/*

# 证书验证
twine upload --cert /path/to/cert.pem dist/*
```

## 🚀 发布流程

### 完整发布流程
```bash
#!/bin/bash
# publish.sh - 完整发布脚本

set -e

echo "🔍 1. 代码质量检查..."
black --check src/ tests/
flake8 src/ tests/
mypy src/

echo "🧪 2. 运行测试..."
pytest tests/ --cov=src/ --cov-report=term-missing

echo "📋 3. 检查包清单..."
check-manifest

echo "🏗️ 4. 清理旧构建..."
rm -rf build/ dist/ *.egg-info/

echo "🏗️ 5. 构建包..."
python -m build

echo "🔍 6. 检查构建产物..."
twine check dist/*

echo "🧪 7. 测试发布到TestPyPI..."
twine upload --repository testpypi dist/*

echo "✅ 8. 测试安装..."
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ my-package

echo "🚀 9. 发布到PyPI..."
read -p "确认发布到PyPI? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    twine upload dist/*
    echo "✅ 发布成功！"
else
    echo "❌ 发布取消"
fi
```

### 版本发布策略
```python
release_strategy = {
    "开发版本": {
        "版本号": "1.0.0.dev1",
        "发布": "不发布到PyPI",
        "用途": "内部开发测试"
    },
    "预发布版本": {
        "版本号": "1.0.0a1, 1.0.0b1, 1.0.0rc1",
        "发布": "发布到PyPI",
        "用途": "社区测试反馈"
    },
    "正式版本": {
        "版本号": "1.0.0",
        "发布": "发布到PyPI",
        "用途": "生产环境使用"
    }
}
```

## 📋 发布前检查清单

### 必要检查项目
```python
pre_release_checklist = {
    "代码质量": [
        "✅ 代码格式化（black/autopep8）",
        "✅ 导入排序（isort）",
        "✅ 代码检查（flake8/pylint）",
        "✅ 类型检查（mypy）"
    ],
    "测试覆盖": [
        "✅ 单元测试通过",
        "✅ 集成测试通过",
        "✅ 测试覆盖率 > 80%",
        "✅ 文档测试通过"
    ],
    "文档完整": [
        "✅ README.md完整",
        "✅ CHANGELOG.md更新",
        "✅ API文档生成",
        "✅ 使用示例完整"
    ],
    "包配置": [
        "✅ pyproject.toml配置正确",
        "✅ 版本号更新",
        "✅ 依赖关系正确",
        "✅ 分类器准确"
    ],
    "构建验证": [
        "✅ 构建成功",
        "✅ 包内容正确",
        "✅ 安装测试通过",
        "✅ 功能测试通过"
    ]
}
```

### 自动化检查脚本
```python
#!/usr/bin/env python3
# pre_release_check.py

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """运行命令并检查结果"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - 通过")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失败")
        print(f"错误: {e.stderr}")
        return False

def main():
    """执行发布前检查"""
    checks = [
        ("black --check src/ tests/", "代码格式检查"),
        ("isort --check-only src/ tests/", "导入排序检查"),
        ("flake8 src/ tests/", "代码质量检查"),
        ("mypy src/", "类型检查"),
        ("pytest tests/ --cov=src/", "测试和覆盖率"),
        ("check-manifest", "包清单检查"),
        ("python -m build", "包构建"),
        ("twine check dist/*", "构建产物检查"),
    ]
    
    failed_checks = []
    
    for cmd, desc in checks:
        if not run_command(cmd, desc):
            failed_checks.append(desc)
    
    if failed_checks:
        print(f"\n❌ {len(failed_checks)} 项检查失败:")
        for check in failed_checks:
            print(f"  - {check}")
        sys.exit(1)
    else:
        print(f"\n✅ 所有检查通过！可以发布。")

if __name__ == "__main__":
    main()
```

## 🔄 版本管理

### 语义化版本控制
```python
# 版本号格式：MAJOR.MINOR.PATCH
version_rules = {
    "MAJOR": "不兼容的API修改",
    "MINOR": "向后兼容的功能性新增",
    "PATCH": "向后兼容的问题修正"
}

# 预发布版本
pre_release_versions = {
    "alpha": "1.0.0a1 - 内部测试版本",
    "beta": "1.0.0b1 - 公开测试版本", 
    "rc": "1.0.0rc1 - 发布候选版本"
}
```

### 自动版本管理
```bash
# 使用bump2version管理版本
pip install bump2version

# 配置文件 .bumpversion.cfg
cat > .bumpversion.cfg << EOF
[bumpversion]
current_version = 1.0.0
commit = True
tag = True

[bumpversion:file:src/my_package/__init__.py]
[bumpversion:file:pyproject.toml]
EOF

# 版本升级
bump2version patch  # 1.0.0 -> 1.0.1
bump2version minor  # 1.0.1 -> 1.1.0
bump2version major  # 1.1.0 -> 2.0.0
```

## 🔧 CI/CD自动发布

### GitHub Actions发布
```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

### 发布工作流
```python
release_workflow = {
    "1. 开发完成": "功能开发和测试完成",
    "2. 版本更新": "更新版本号和CHANGELOG",
    "3. 创建标签": "git tag v1.0.0",
    "4. 推送标签": "git push origin v1.0.0", 
    "5. 创建Release": "在GitHub创建Release",
    "6. 自动构建": "CI/CD自动构建包",
    "7. 自动发布": "自动发布到PyPI",
    "8. 通知用户": "发送发布通知"
}
```

## 🎯 发布后管理

### 监控和维护
```python
post_release_tasks = {
    "下载监控": "监控包的下载量和使用情况",
    "问题反馈": "及时响应用户问题和bug报告",
    "版本维护": "定期发布bug修复和安全更新",
    "文档更新": "保持文档与代码同步",
    "社区互动": "参与社区讨论和贡献"
}
```

### 包的撤回和删除
```python
package_management = {
    "版本撤回": {
        "方法": "在PyPI项目页面撤回版本",
        "效果": "隐藏版本，但不删除文件",
        "用途": "发现严重问题时临时隐藏"
    },
    "版本删除": {
        "限制": "发布后72小时内可删除",
        "条件": "无其他包依赖该版本",
        "注意": "删除后版本号不能重用"
    }
}
```

## 🎯 本节小结

- **PyPI发布**：掌握向Python包索引发布包的完整流程
- **工具使用**：熟练使用twine等发布工具
- **质量保证**：发布前进行全面的质量检查
- **版本管理**：采用语义化版本控制策略
- **自动化**：使用CI/CD实现自动化发布

## 💡 关键要点

1. **测试先行**：先发布到TestPyPI进行测试
2. **质量检查**：发布前进行全面的代码和包检查
3. **版本策略**：采用语义化版本控制
4. **安全认证**：使用API Token而非密码
5. **自动化**：使用CI/CD实现自动化发布流程

## 📚 延伸阅读
- [PyPI官方文档](https://pypi.org/help/)
- [twine文档](https://twine.readthedocs.io/)
- [语义化版本控制](https://semver.org/)
- [Python包发布指南](https://packaging.python.org/tutorials/packaging-projects/)

---
**下一节预告**：08-常用第三方库 - 介绍Python生态系统中的重要第三方库
