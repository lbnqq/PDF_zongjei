#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科大讯飞星火大模型API连接测试脚本

这个脚本用于测试API配置是否正确，以及连接是否正常

使用方法：
    python test_api.py

作者：AI助手
"""

import os
import sys
from dotenv import load_dotenv

# 设置输出编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def test_environment():
    """测试环境配置"""
    print("🔍 检查环境配置...")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查必要的环境变量
    required_vars = ['SPARK_APPID', 'SPARK_APIKEY', 'SPARK_APISECRET']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: 未设置")
        else:
            # 只显示前几个字符，保护隐私
            masked_value = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var}: {masked_value}")
    
    if missing_vars:
        print(f"\n❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请在.env文件中配置这些变量")
        return False
    
    print("✅ 环境变量配置检查通过")
    return True

def test_api_connection():
    """测试API连接"""
    print("\n🌐 测试API连接...")

    try:
        # 获取协议类型
        protocol = os.getenv("API_PROTOCOL", "HTTP").upper()
        print(f"📡 使用协议: {protocol}")

        if protocol == "HTTP":
            # 测试HTTP协议
            from spark_http_client import SparkHTTPClient

            api_password = os.getenv("SPARK_HTTP_API_PASSWORD")
            base_url = os.getenv("SPARK_HTTP_BASE_URL", "https://spark-api-open.xf-yun.com/v2")
            model = os.getenv("SPARK_MODEL", "x1")

            if not api_password:
                print("❌ 缺少HTTP协议配置: SPARK_HTTP_API_PASSWORD")
                print("请在控制台 https://console.xfyun.cn/services/bmx1 获取APIpassword")
                return False

            print(f"🔗 HTTP配置: {base_url}, 模型: {model}")
            client = SparkHTTPClient(api_password, base_url, model)

        else:
            # 测试WebSocket协议
            from app import SparkWebSocketClient, APPID, APIKey, APISecret, SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH

            print(f"🔗 WebSocket配置: {SPARK_HOST}{SPARK_API_PATH}, 域名: {SPARK_DOMAIN}")
            client = SparkWebSocketClient(
                APPID, APIKey, APISecret,
                SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH
            )
        
        # 发送一个简单的测试请求
        test_input = "今年我完成了一个重要项目，学习了新技术，明年计划继续提升。"
        print(f"📝 发送测试内容: {test_input}")
        
        # 发送请求
        response = client.send_request(test_input)
        
        print(f"✅ 收到响应，长度: {len(response)} 字符")
        print(f"📄 响应内容预览: {response[:200]}...")
        
        # 尝试解析JSON
        import json
        try:
            # 清理可能的markdown格式
            clean_response = response.strip()
            if clean_response.startswith("```json") and clean_response.endswith("```"):
                clean_response = clean_response[7:-3].strip()
            
            parsed_data = json.loads(clean_response)
            print("✅ JSON解析成功")
            print("📋 解析结果字段:")
            for key in parsed_data.keys():
                print(f"   • {key}")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response}")
            return False
            
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🤖 科大讯飞星火大模型API连接测试")
    print("=" * 50)
    
    # 测试环境配置
    if not test_environment():
        print("\n❌ 环境配置测试失败，请检查配置后重试")
        sys.exit(1)
    
    # 测试API连接
    if not test_api_connection():
        print("\n❌ API连接测试失败")
        print("可能的原因：")
        print("1. API凭证不正确")
        print("2. 网络连接问题")
        print("3. API服务暂时不可用")
        print("4. 请求格式不正确")
        sys.exit(1)
    
    print("\n🎉 所有测试通过！API配置正确，连接正常")
    print("现在可以正常使用AI智能年度总结生成器了")

if __name__ == "__main__":
    main()
