#!/usr/bin/env python3
"""
科大讯飞星火大模型配置向导

这个脚本帮助用户快速配置API凭证

使用方法：
    python setup_config.py

作者：AI助手
"""

import os
import shutil

def create_env_file():
    """创建.env配置文件"""
    print("🔧 科大讯飞星火大模型配置向导")
    print("=" * 50)
    
    # 检查是否已存在.env文件
    if os.path.exists('.env'):
        print("📁 发现已存在的.env文件")
        choice = input("是否要覆盖现有配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("❌ 配置已取消")
            return False
    
    print("\n📋 请选择API协议类型：")
    print("1. HTTP协议（推荐）- 支持X1模型，更稳定")
    print("2. WebSocket协议（备用）- 兼容性好，但功能有限")
    
    while True:
        choice = input("\n请选择 (1/2): ").strip()
        if choice in ['1', '2']:
            break
        print("❌ 请输入1或2")
    
    protocol = "HTTP" if choice == '1' else "WEBSOCKET"
    print(f"✅ 已选择: {protocol}协议")
    
    # 创建配置内容
    config_lines = [
        "# 科大讯飞星火大模型API配置",
        "# 自动生成的配置文件",
        "",
        f"# API协议类型",
        f"API_PROTOCOL=\"{protocol}\"",
        ""
    ]
    
    if protocol == "HTTP":
        print(f"\n📝 HTTP协议配置:")
        print(f"请访问 https://console.xfyun.cn/services/bmx1 获取APIpassword")
        
        api_password = input("请输入APIpassword: ").strip()
        if not api_password:
            print("❌ APIpassword不能为空")
            return False
        
        config_lines.extend([
            "# HTTP协议配置",
            f"SPARK_HTTP_API_PASSWORD=\"{api_password}\"",
            "SPARK_HTTP_BASE_URL=\"https://spark-api-open.xf-yun.com/v2\"",
            "SPARK_MODEL=\"x1\"",
            ""
        ])
        
    else:
        print(f"\n📝 WebSocket协议配置:")
        print(f"请在讯飞开放平台控制台获取以下信息:")
        
        appid = input("请输入APPID: ").strip()
        apikey = input("请输入APIKey: ").strip()
        apisecret = input("请输入APISecret: ").strip()
        
        if not all([appid, apikey, apisecret]):
            print("❌ 所有字段都不能为空")
            return False
        
        config_lines.extend([
            "# WebSocket协议配置",
            f"SPARK_APPID=\"{appid}\"",
            f"SPARK_APIKEY=\"{apikey}\"",
            f"SPARK_APISECRET=\"{apisecret}\"",
            "SPARK_DOMAIN=\"generalv3.5\"",
            "SPARK_HOST=\"spark-api.xf-yun.com\"",
            "SPARK_API_PATH=\"/v3.5/chat\"",
            ""
        ])
    
    # 写入配置文件
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write('\n'.join(config_lines))
        
        print(f"\n✅ 配置文件已创建: .env")
        print(f"🔒 请确保不要将.env文件提交到版本控制系统")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False

def test_configuration():
    """测试配置"""
    print(f"\n🧪 测试API配置...")

    try:
        import subprocess
        import sys

        # 设置正确的编码环境
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        # 使用当前Python解释器路径
        python_exe = sys.executable

        result = subprocess.run(
            [python_exe, 'simple_test.py'],
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace',
            env=env
        )

        if result.returncode == 0:
            print("✅ API配置测试通过！")
            print("测试输出:")
            print(result.stdout)
            return True
        else:
            print("❌ API配置测试失败")
            print("错误信息:")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print("输出信息:")
                print(result.stdout)
            return False

    except subprocess.TimeoutExpired:
        print("⏰ 测试超时，可能是网络问题")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ 编码错误: {e}")
        print("💡 建议直接运行: python test_api.py")
        return False
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        print("💡 建议直接运行: python test_api.py")
        return False

def main():
    """主函数"""
    print("🤖 欢迎使用AI智能年度总结生成器配置向导")
    
    # 创建配置文件
    if not create_env_file():
        return
    
    # 询问是否测试配置
    test_choice = input("\n是否立即测试配置？(Y/n): ").strip().lower()
    if test_choice != 'n':
        if test_configuration():
            print(f"\n🎉 配置完成！现在可以启动应用了:")
            print(f"   python start.py")
        else:
            print(f"\n⚠️  配置可能有问题，请检查:")
            print(f"   python check_config.py")
    else:
        print(f"\n💡 稍后可以手动测试配置:")
        print(f"   python test_api.py")
    
    print(f"\n📚 更多帮助:")
    print(f"   - 查看配置: python check_config.py")
    print(f"   - 故障排除: 查看 故障排除指南.md")
    print(f"   - 启动应用: python start.py")

if __name__ == "__main__":
    main()
