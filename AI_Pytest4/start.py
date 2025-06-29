#!/usr/bin/env python3
"""
AI 智能年度总结生成器 - 启动脚本

这个脚本提供了一个更友好的启动方式，包含：
1. 环境检查
2. 依赖验证
3. 配置检查
4. 启动应用

使用方法：
    python start.py

作者：AI助手
日期：2025年
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本是否符合要求"""
    print("🔍 检查Python版本...")
    if sys.version_info < (3, 8):
        print("❌ 错误：需要Python 3.8或更高版本")
        print(f"   当前版本：{sys.version}")
        return False
    print(f"✅ Python版本检查通过：{sys.version.split()[0]}")
    return True

def check_dependencies():
    """检查必要的依赖包是否已安装"""
    print("\n🔍 检查依赖包...")
    required_packages = [
        'flask',
        'python-docx', 
        'websocket-client',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ 缺少依赖包：{', '.join(missing_packages)}")
        print("请运行以下命令安装依赖：")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def check_template_file():
    """检查年度总结模板文件是否存在"""
    print("\n🔍 检查模板文件...")
    template_path = Path("年度总结模板.docx")
    
    if not template_path.exists():
        print("❌ 未找到年度总结模板文件")
        print("请确保在项目根目录创建 '年度总结模板.docx' 文件")
        print("参考 '模板文件说明.md' 了解如何创建模板")
        return False
    
    print("✅ 模板文件检查通过")
    return True

def check_env_config():
    """检查环境变量配置"""
    print("\n🔍 检查环境变量配置...")
    
    # 检查.env文件是否存在
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  未找到.env文件")
        print("请复制.env.example为.env并配置您的API凭证")
        print("或者直接设置系统环境变量")
    
    # 检查必要的环境变量
    required_env_vars = ['SPARK_APPID', 'SPARK_APIKEY', 'SPARK_APISECRET']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  缺少环境变量：{', '.join(missing_vars)}")
        print("请在.env文件中配置科大讯飞星火大模型的API凭证")
        print("或设置对应的系统环境变量")
        return False
    
    print("✅ 环境变量配置检查通过")
    return True

def start_application():
    """启动Flask应用"""
    print("\n🚀 启动AI智能年度总结生成器...")
    print("=" * 60)
    print("应用启动中，请稍候...")
    print("启动完成后，请在浏览器中访问：http://localhost:5000")
    print("按 Ctrl+C 停止应用")
    print("=" * 60)
    
    try:
        # 导入并运行Flask应用
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止")
    except Exception as e:
        print(f"\n❌ 启动失败：{e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🤖 AI 智能年度总结生成器")
    print("=" * 60)
    
    # 执行各项检查
    checks = [
        check_python_version,
        check_dependencies,
        check_template_file,
        check_env_config
    ]
    
    for check in checks:
        if not check():
            print(f"\n❌ 启动失败，请解决上述问题后重试")
            sys.exit(1)
    
    print("\n✅ 所有检查通过，准备启动应用...")
    
    # 启动应用
    start_application()

if __name__ == "__main__":
    main()
