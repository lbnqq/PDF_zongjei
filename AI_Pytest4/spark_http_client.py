#!/usr/bin/env python3
"""
科大讯飞星火大模型HTTP客户端

根据官方文档 https://www.xfyun.cn/doc/spark/X1http.html 实现
支持X1模型的HTTP API调用

作者：AI助手
日期：2025年
"""

import os
import json
import requests
from typing import Dict, Any, Optional

class SparkHTTPClient:
    """
    科大讯飞星火大模型HTTP客户端类
    
    这个类封装了与星火大模型X1的HTTP通信逻辑，包括：
    - HTTP请求构造和发送
    - 响应处理和解析
    - 错误处理
    """
    
    def __init__(self, api_password: str, base_url: str = None, model: str = "x1"):
        """
        初始化HTTP客户端
        
        参数:
            api_password: HTTP协议的APIpassword
            base_url: API基础URL
            model: 模型名称
        """
        self.api_password = api_password
        self.base_url = base_url or "https://spark-api-open.xf-yun.com/v2"
        self.model = model
        self.endpoint = "/chat/completions"
        
        # 检查必要参数
        if not self.api_password:
            raise ValueError("API password is required for HTTP protocol")
    
    def send_request(self, user_input_text: str) -> str:
        """
        发送请求到星火大模型并获取响应
        
        参数:
            user_input_text: 用户输入的原始文本
            
        返回:
            AI生成的JSON格式响应内容
        """
        print(f"📝 用户输入长度: {len(user_input_text)} 字符")
        
        # 构造请求URL
        url = f"{self.base_url}{self.endpoint}"
        print(f"🔗 请求URL: {url}")
        
        # 构造请求头
        headers = {
            "Authorization": f"Bearer {self.api_password}",
            "Content-Type": "application/json"
        }
        
        # 构造提示词
        prompt = self._create_spark_prompt(user_input_text)
        
        # 构造请求体
        payload = {
            "model": self.model,
            "user": "user_123456",  # 用户唯一ID
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是一个专业的企业年度总结报告智能助手。"
                        "你的任务是根据用户提供的原始工作内容，"
                        "提炼并总结出年度总结报告的关键信息，"
                        "并以结构化的JSON格式输出。"
                        "确保内容真实、简洁、客观。"
                        "如果某个部分信息不足，请留空或简要说明。"
                        "对于列表形式的字段，请输出JSON数组。"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,  # 使用非流式响应
            "temperature": 0.5,
            "top_p": 0.95,
            "max_tokens": 4096
        }
        
        print(f"📋 请求体构造完成")
        
        try:
            # 发送HTTP请求
            print("🚀 发送HTTP请求...")
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=60  # 60秒超时
            )
            
            print(f"📡 收到响应，状态码: {response.status_code}")
            
            # 检查HTTP状态码
            if response.status_code != 200:
                error_msg = f"HTTP请求失败，状态码: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f", 错误详情: {error_detail}"
                except:
                    error_msg += f", 响应内容: {response.text}"
                raise Exception(error_msg)
            
            # 解析响应
            response_data = response.json()
            print(f"✅ 响应解析成功")
            
            # 检查API错误码
            if response_data.get('code', 0) != 0:
                error_code = response_data.get('code', '未知')
                error_msg = response_data.get('message', '未知错误')
                raise Exception(f"API请求失败，错误码: {error_code}, 错误信息: {error_msg}")
            
            # 提取响应内容
            if 'choices' not in response_data or not response_data['choices']:
                raise Exception("响应中缺少choices字段或为空")
            
            choice = response_data['choices'][0]
            if 'message' not in choice or 'content' not in choice['message']:
                raise Exception("响应格式错误，缺少message.content字段")
            
            content = choice['message']['content']
            print(f"📄 成功获取AI响应，长度: {len(content)} 字符")
            
            # 打印token使用情况
            if 'usage' in response_data:
                usage = response_data['usage']
                print(f"📊 Token使用情况:")
                print(f"   输入: {usage.get('prompt_tokens', 0)} tokens")
                print(f"   输出: {usage.get('completion_tokens', 0)} tokens")
                print(f"   总计: {usage.get('total_tokens', 0)} tokens")
            
            return content
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接或稍后重试")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误，请检查网络连接")
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP请求异常: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"响应JSON解析失败: {str(e)}")
        except Exception as e:
            if "API请求失败" in str(e) or "HTTP请求失败" in str(e):
                raise  # 重新抛出已知错误
            else:
                raise Exception(f"未知错误: {str(e)}")
    
    def _create_spark_prompt(self, user_input_text: str) -> str:
        """
        构造发送给星火大模型的提示词
        
        参数:
            user_input_text: 用户输入的原始文本
            
        返回:
            格式化的提示词字符串
        """
        prompt = f"""
请根据以下用户输入的文本内容，生成一份年度总结报告的关键信息。
如果某个字段没有对应内容，请使用空字符串或空列表。

用户输入内容：
『{user_input_text}』

请严格按照以下JSON格式输出，确保字段名称不变：
{{
  "年度总结概述": "根据上述内容，总结年度工作亮点、整体表现和主要成就，用一句话概括。",
  "主要成就与贡献": [
    "条目1：具体完成了什么，取得了什么成果",
    "条目2：...",
    "..."
  ],
  "遇到的挑战及解决方案": [
    "条目1：遇到了什么困难，如何解决的",
    "条目2：...",
    "..."
  ],
  "个人成长与学习": [
    "条目1：学习了什么新知识/技能，如何应用",
    "条目2：...",
    "..."
  ],
  "未来展望与计划": [
    "条目1：明年的主要工作目标",
    "条目2：...",
    "..."
  ],
  "姓名": "（请根据上下文推断或留空）",
  "报告日期": "（请根据上下文推断或填写当前日期，格式如：YYYY年MM月DD日）"
}}
"""
        return prompt


def create_spark_client():
    """
    根据环境变量配置创建合适的星火大模型客户端
    
    返回:
        配置好的客户端实例
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    # 获取协议类型
    protocol = os.getenv("API_PROTOCOL", "HTTP").upper()
    
    if protocol == "HTTP":
        # 使用HTTP协议
        api_password = os.getenv("SPARK_HTTP_API_PASSWORD")
        base_url = os.getenv("SPARK_HTTP_BASE_URL", "https://spark-api-open.xf-yun.com/v2")
        model = os.getenv("SPARK_MODEL", "x1")
        
        if not api_password:
            raise Exception(
                "HTTP协议需要配置 SPARK_HTTP_API_PASSWORD，"
                "请在控制台 https://console.xfyun.cn/services/bmx1 获取"
            )
        
        print(f"🔗 使用HTTP协议连接星火大模型X1")
        return SparkHTTPClient(api_password, base_url, model)
    
    else:
        # 使用WebSocket协议（原有实现）
        from app import SparkWebSocketClient, APPID, APIKey, APISecret, SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH
        
        print(f"🔗 使用WebSocket协议连接星火大模型")
        return SparkWebSocketClient(
            APPID, APIKey, APISecret, 
            SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH
        )
