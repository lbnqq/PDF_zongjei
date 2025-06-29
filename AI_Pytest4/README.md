# AI 智能年度总结生成器

本项目是一个基于Flask的Web应用，利用科大讯飞星火大模型实现智能年度总结的自动生成。用户可以输入文本或上传文件，AI将分析内容并自动填充到预设的WPS（.docx）模板中。

## 功能特性

*   支持文本输入和 .txt/.docx 文件上传。
*   集成科大讯飞星火大模型进行内容分析和结构化提取。
*   根据AI提取的内容，自动填充到年度总结的 .docx 模板中。
*   生成可下载的个性化年度总结报告。

## 技术栈

*   **后端:** Python 3.8+, Flask, websocket-client, python-docx
*   **前端:** HTML, CSS, JavaScript
*   **AI服务:** 科大讯飞星火大模型 (SparkDesk v3.5)

## 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/ai_summary_generator.git
cd ai_summary_generator
```

### 2. 创建并激活虚拟环境 (推荐)

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置科大讯飞星火大模型凭证

#### 方法一：使用配置向导（推荐）
```bash
python setup_config.py
```
按照提示选择协议类型并输入API凭证。

#### 方法二：手动配置

**HTTP协议（推荐）：**
1. 访问 [科大讯飞控制台](https://console.xfyun.cn/services/bmx1)
2. 开通X1模型服务
3. 获取APIpassword
4. 创建`.env`文件：

```env
API_PROTOCOL="HTTP"
SPARK_HTTP_API_PASSWORD="YOUR_HTTP_API_PASSWORD"
SPARK_HTTP_BASE_URL="https://spark-api-open.xf-yun.com/v2"
SPARK_MODEL="x1"
```

**WebSocket协议（备用）：**
1. 在讯飞开放平台创建应用并获取凭证
2. 创建`.env`文件：

```env
API_PROTOCOL="WEBSOCKET"
SPARK_APPID="YOUR_XFYUN_APPID"
SPARK_APIKEY="YOUR_XFYUN_APIKEY"
SPARK_APISECRET="YOUR_XFYUN_APISECRET"
SPARK_DOMAIN="generalv3.5"
SPARK_HOST="spark-api.xf-yun.com"
SPARK_API_PATH="/v3.5/chat"
```

**注意：**
- HTTP协议支持最新的X1模型，功能更完整，推荐使用
- WebSocket协议作为备用选择，兼容性较好
- 生产环境请勿将敏感信息硬编码到代码中

### 5. 准备年度总结模板

确保在项目根目录存在一个名为 `年度总结模板.docx` 的文件。
该模板应包含以下占位符，以便AI填充：
*   `[[年度总结概述]]`
*   `[[主要成就与贡献]]`
*   `[[遇到的挑战及解决方案]]`
*   `[[个人成长与学习]]`
*   `[[未来展望与计划]]`
*   `[[您的姓名]]`
*   `[[报告日期]]`

示例：
```
# 年度工作总结报告

**年度总结概述：** [[年度总结概述]]

**主要成就与贡献：**
[[主要成就与贡献]]

**遇到的挑战及解决方案：**
[[遇到的挑战及解决方案]]

**个人成长与学习：**
[[个人成长与学习]]

**未来展望与计划：**
[[未来展望与计划]]

---
报告人：[[您的姓名]]
日期：[[报告日期]]
```

### 6. 运行应用

```bash
flask run --host=0.0.0.0 --port=5000
```

### 7. 访问应用

在浏览器中打开 `http://localhost:5000`

## 项目结构

```
/AI_Pytest4
├── app.py                    # Flask主应用文件
├── templates/
│   └── index.html           # 前端页面模板
├── requirements.txt         # Python依赖包列表
├── README.md               # 项目说明文档
├── .env.example            # 环境变量配置示例
└── 年度总结模板.docx        # Word模板文件（需要用户自行创建）
```

## 使用说明

1. 启动应用后，在浏览器中访问 `http://localhost:5000`
2. 在文本框中输入您的工作内容，或上传 .txt/.docx 文件
3. 点击"生成年度总结"按钮
4. 等待AI分析处理（通常需要几秒钟）
5. 处理完成后，点击下载链接获取生成的年度总结文档

## 注意事项

- 请确保网络连接正常，以便访问科大讯飞星火大模型API
- 上传的文件大小建议不超过10MB
- 生成的文档格式为 .docx，可用Microsoft Word或WPS打开
- 首次使用需要在科大讯飞开放平台注册并获取API凭证

## 故障排除

### 快速测试
如果遇到问题，首先运行测试脚本：
```bash
python test_api.py
```

### 常见问题
1. **"处理响应消息时出错: 'payload'"**
   - 检查API凭证配置
   - 验证网络连接
   - 查看详细错误日志

2. **"API凭证未配置"**
   - 确保.env文件存在且配置正确
   - 检查环境变量设置

3. **JSON解析错误**
   - 检查网络连接稳定性
   - 尝试减少输入内容长度

详细的故障排除指南请参考：`故障排除指南.md`

## 技术支持

如遇到问题，请检查：
1. 网络连接是否正常
2. API凭证是否正确配置
3. 年度总结模板文件是否存在
4. Python依赖包是否正确安装

获取帮助：
- 查看控制台详细日志
- 运行 `python test_api.py` 测试配置
- 参考 `故障排除指南.md` 文档
