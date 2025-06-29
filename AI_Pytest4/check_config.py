#!/usr/bin/env python3
"""
科大讯飞星火大模型配置检查工具

这个脚本帮助诊断API配置问题，特别是AppIdNoAuthError错误

使用方法：
    python check_config.py

作者：AI助手
"""

import os
from dotenv import load_dotenv

def check_config():
    """检查配置并提供详细建议"""
    print("🔍 科大讯飞星火大模型配置检查")
    print("=" * 50)
    
    # 加载环境变量
    load_dotenv()
    
    # 检查.env文件
    env_file_exists = os.path.exists('.env')
    print(f"📁 .env文件: {'✅ 存在' if env_file_exists else '❌ 不存在'}")
    
    if not env_file_exists:
        print("💡 建议：复制 .env.example 为 .env 并填入您的API凭证")
        return False
    
    # 检查协议配置
    protocol = os.getenv("API_PROTOCOL", "HTTP").upper()
    print(f"\n📡 API协议: {protocol}")

    # 检查环境变量
    appid = os.getenv("SPARK_APPID")
    apikey = os.getenv("SPARK_APIKEY")
    apisecret = os.getenv("SPARK_APISECRET")
    http_password = os.getenv("SPARK_HTTP_API_PASSWORD")

    print(f"\n🔑 API凭证检查:")

    if protocol == "HTTP":
        print(f"   SPARK_HTTP_API_PASSWORD: {'✅ 已设置' if http_password else '❌ 未设置'}")
        if http_password:
            print(f"   HTTP APIpassword: {http_password[:8]}...")
        print(f"\n💡 HTTP协议说明:")
        print(f"   - 推荐使用HTTP协议，更稳定")
        print(f"   - 支持X1模型的完整功能")
        print(f"   - 需要在控制台获取APIpassword")
    else:
        print(f"   SPARK_APPID: {'✅ 已设置' if appid else '❌ 未设置'}")
        print(f"   SPARK_APIKEY: {'✅ 已设置' if apikey else '❌ 未设置'}")
        print(f"   SPARK_APISECRET: {'✅ 已设置' if apisecret else '❌ 未设置'}")
        if appid:
            print(f"   当前APPID: {appid}")
        print(f"\n💡 WebSocket协议说明:")
        print(f"   - 备用协议，兼容性较好")
        print(f"   - 可能不支持最新的X1模型功能")
    
    # 检查凭证格式
    issues = []
    
    if appid:
        if len(appid) != 8:
            issues.append("APPID长度不正确（应该是8位字符）")
        if not appid.isalnum():
            issues.append("APPID格式不正确（应该只包含字母和数字）")
    
    if apikey:
        if len(apikey) < 20:
            issues.append("APIKEY长度可能不正确")
    
    if apisecret:
        if len(apisecret) < 20:
            issues.append("APISECRET长度可能不正确")
    
    if issues:
        print(f"\n⚠️  发现的问题:")
        for issue in issues:
            print(f"   • {issue}")
    
    # 针对AppIdNoAuthError的特殊检查
    print(f"\n🚨 AppIdNoAuthError错误排查:")
    print(f"   当前错误通常由以下原因造成：")
    print(f"   1. 应用未通过审核")
    print(f"   2. 未开通星火认知大模型服务")
    print(f"   3. APPID不正确")
    print(f"   4. 账号未实名认证")
    print(f"   5. 服务已过期或余额不足")
    
    print(f"\n📋 解决步骤:")
    print(f"   1. 登录讯飞开放平台: https://www.xfyun.cn/")
    print(f"   2. 进入控制台 → 我的应用")
    print(f"   3. 检查应用状态（是否已审核通过）")
    print(f"   4. 检查服务管理 → 星火认知大模型（是否已开通）")
    print(f"   5. 确认账号已实名认证")
    print(f"   6. 检查服务余额或免费额度")
    
    # 根据协议检查配置完整性
    if protocol == "HTTP":
        if http_password:
            print(f"\n✅ HTTP协议配置完整")
            return True
        else:
            print(f"\n❌ HTTP协议配置不完整，缺少 SPARK_HTTP_API_PASSWORD")
            print(f"📋 获取步骤:")
            print(f"   1. 访问 https://console.xfyun.cn/services/bmx1")
            print(f"   2. 开通X1模型服务")
            print(f"   3. 获取APIpassword")
            print(f"   4. 设置环境变量 SPARK_HTTP_API_PASSWORD")
            return False
    else:
        if appid and apikey and apisecret:
            print(f"\n✅ WebSocket协议配置完整")
            return True
        else:
            print(f"\n❌ WebSocket协议配置不完整")
            return False

def show_platform_guide():
    """显示平台操作指南"""
    print(f"\n📖 讯飞开放平台操作指南:")
    print(f"=" * 50)
    print(f"1. 访问: https://www.xfyun.cn/")
    print(f"2. 注册/登录账号")
    print(f"3. 完成实名认证（如果还没有）")
    print(f"4. 进入控制台")
    print(f"5. 创建应用:")
    print(f"   - 点击'创建新应用'")
    print(f"   - 填写应用信息")
    print(f"   - 等待审核通过")
    print(f"6. 开通服务:")
    print(f"   - 进入应用详情")
    print(f"   - 点击'服务管理'")
    print(f"   - 找到'星火认知大模型'")
    print(f"   - 点击'开通'")
    print(f"7. 获取凭证:")
    print(f"   - 在应用详情页面")
    print(f"   - 找到'接口密钥'部分")
    print(f"   - 复制APPID、APIKey、APISecret")

def main():
    """主函数"""
    config_ok = check_config()
    
    if not config_ok:
        show_platform_guide()
        print(f"\n💡 配置完成后，运行以下命令测试:")
        print(f"   python test_api.py")
    else:
        print(f"\n🧪 建议运行API连接测试:")
        print(f"   python test_api.py")

if __name__ == "__main__":
    main()
