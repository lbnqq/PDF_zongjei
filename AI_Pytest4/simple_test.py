#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的API测试脚本

避免编码问题，直接测试API连接

使用方法：
    python simple_test.py

作者：AI助手
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """主函数"""
    print("API Connection Test")
    print("=" * 40)
    
    # 加载环境变量
    load_dotenv()
    
    # 检查协议类型
    protocol = os.getenv("API_PROTOCOL", "HTTP").upper()
    print(f"Protocol: {protocol}")
    
    if protocol == "HTTP":
        # 测试HTTP协议
        api_password = os.getenv("SPARK_HTTP_API_PASSWORD")
        if not api_password:
            print("ERROR: Missing SPARK_HTTP_API_PASSWORD")
            return False
        
        print(f"HTTP API Password: {api_password[:8]}...")
        
        try:
            from spark_http_client import SparkHTTPClient
            
            client = SparkHTTPClient(api_password)
            print("HTTP client created successfully")
            
            # 发送测试请求
            test_input = "Test input for API"
            print("Sending test request...")
            
            response = client.send_request(test_input)
            print(f"Response length: {len(response)} characters")
            print("SUCCESS: API connection test passed")
            return True
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False
    
    else:
        # 测试WebSocket协议
        appid = os.getenv("SPARK_APPID")
        apikey = os.getenv("SPARK_APIKEY")
        apisecret = os.getenv("SPARK_APISECRET")
        
        if not all([appid, apikey, apisecret]):
            print("ERROR: Missing WebSocket credentials")
            return False
        
        print(f"APPID: {appid}")
        print(f"APIKey: {apikey[:8]}...")
        
        try:
            from app import SparkWebSocketClient, SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH
            
            client = SparkWebSocketClient(
                appid, apikey, apisecret,
                SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH
            )
            print("WebSocket client created successfully")
            
            # 发送测试请求
            test_input = "Test input for API"
            print("Sending test request...")
            
            response = client.send_request(test_input)
            print(f"Response length: {len(response)} characters")
            print("SUCCESS: API connection test passed")
            return True
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
