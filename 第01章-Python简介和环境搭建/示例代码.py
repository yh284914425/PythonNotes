#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第01章 - Python简介和环境搭建
示例代码文件

本文件包含第一章的所有示例代码
"""

# ============================================================================
# 1. 第一个Python程序
# ============================================================================

print("Hello, World!")
print("欢迎来到Python的世界！")

# ============================================================================
# 2. Python基本信息查看
# ============================================================================

import sys
import platform

print("\n" + "="*50)
print("Python环境信息")
print("="*50)

# Python版本信息
print(f"Python版本: {sys.version}")
print(f"Python版本信息: {sys.version_info}")

# 系统信息
print(f"操作系统: {platform.system()}")
print(f"系统版本: {platform.release()}")
print(f"处理器架构: {platform.machine()}")

# Python解释器路径
print(f"Python解释器路径: {sys.executable}")

# ============================================================================
# 3. 简单的交互式示例
# ============================================================================

print("\n" + "="*50)
print("简单的交互示例")
print("="*50)

# 简单的计算
print("2 + 3 =", 2 + 3)
print("10 * 5 =", 10 * 5)
print("20 / 4 =", 20 / 4)

# 字符串操作
name = "Python"
print(f"Hello, {name}!")
print(f"{name} 的长度是: {len(name)}")

# ============================================================================
# 4. Python之禅 (The Zen of Python)
# ============================================================================

print("\n" + "="*50)
print("Python之禅")
print("="*50)

import this  # 这会打印Python之禅

# ============================================================================
# 5. 简单的用户交互（注释掉，避免在自动运行时卡住）
# ============================================================================

# print("\n" + "="*50)
# print("用户交互示例")
# print("="*50)
# 
# # 获取用户输入
# user_name = input("请输入你的名字: ")
# print(f"你好, {user_name}! 欢迎学习Python!")

# ============================================================================
# 6. 环境检查函数
# ============================================================================

def check_python_environment():
    """检查Python环境的基本信息"""
    print("\n" + "="*50)
    print("Python环境检查")
    print("="*50)
    
    # 检查Python版本
    if sys.version_info >= (3, 6):
        print("✅ Python版本符合要求 (>= 3.6)")
    else:
        print("❌ Python版本过低，建议升级到3.6以上")
    
    # 检查常用模块
    modules_to_check = ['os', 'sys', 'datetime', 'json', 'math']
    
    print("\n检查常用模块:")
    for module_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - 可用")
        except ImportError:
            print(f"❌ {module_name} - 不可用")
    
    print("\n🎉 环境检查完成!")

# 运行环境检查
if __name__ == "__main__":
    check_python_environment()
