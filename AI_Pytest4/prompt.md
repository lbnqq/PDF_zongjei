好的，我将总结上述技术实现方案，并以一种更适合“Augment”这类AI代码生成工具的风格来编写提示词，使其能够直接生成项目的代码文件。

---

## Augment Prompt: AI 智能年度总结生成器

**项目目标：**
开发一个Web应用程序，用户可以输入文本或上传文件（`.txt` 或 `.docx`），AI（科大讯飞星火大模型）将自动分析内容，智能提取并填充到预设的WPS（`.docx`）年度总结模板中，最终生成可下载的`.docx`文档。

**核心功能点：**
1.  **用户输入处理：** 支持多行文本输入或上传 `.txt` / `.docx` 文件。
2.  **AI内容分析与提取：** 调用科大讯飞星火大模型，通过Prompt Engineering，将非结构化用户输入转化为结构化的年度总结关键信息（JSON格式）。
3.  **WPS Docx模板填充：** 使用`python-docx`库，加载预设模板，并根据AI提取的JSON数据智能填充到模板中的特定占位符位置。
4.  **Docx文件生成与下载：** 将填充后的文档保存为新的`.docx`文件，并提供给用户下载。
5.  **安全凭证管理：** AI模型API凭证通过环境变量加载。

**技术栈：**
*   **后端：** Python (Flask)
*   **AI集成：** `websocket-client` (for 科大讯飞星火 WebSocket API)
*   **文档处理：** `python-docx`
*   **前端：** HTML, CSS, JavaScript (Fetch API)

**项目文件结构：**

```
/ai_summary_generator
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
├── README.md
├── .env.example
└── 年度总结模板.docx  <-- 这个文件是用户预设的模板，Augment不需要生成其内容，但需知道其存在和占位符规则。
```

---

**请Augment按照以下文件内容生成项目代码：**

### **1. 文件: `README.md`**

```markdown
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

在讯飞开放平台（`www.xfyun.cn`）创建应用并获取 `APPID`、`APIKey`、`APISecret`。
然后，将这些凭证配置到项目的环境变量中。可以创建一个 `.env` 文件（在生产环境中推荐使用服务器环境变量）：

`.env` 文件示例:
```
SPARK_APPID="YOUR_XFYUN_APPID"
SPARK_APIKEY="YOUR_XFYUN_APIKEY"
SPARK_APISECRET="YOUR_XFYUN_APISECRET"
# 可选：指定模型版本对应的域名和路径，默认使用 v3.5
# SPARK_DOMAIN="generalv3.5"
# SPARK_HOST="spark-api.xf-yun.com"
# SPARK_API_PATH="/v3.5/chat"
```

**注意：** 生产环境请勿将敏感信息硬编码到代码中。

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

---
```

### **2. 文件: `.env.example`**

```dotenv
SPARK_APPID="YOUR_XFYUN_APPID"
SPARK_APIKEY="YOUR_XFYUN_APIKEY"
SPARK_APISECRET="YOUR_XFYUN_APISECRET"
# 可选配置项，一般无需修改，除非使用不同版本的星火模型
SPARK_DOMAIN="generalv3.5"
SPARK_HOST="spark-api.xf-yun.com"
SPARK_API_PATH="/v3.5/chat"
```

### **3. 文件: `requirements.txt`**

```
Flask==2.3.3
python-docx==1.1.0
websocket-client==1.7.0
python-dotenv==1.0.0 # 用于加载 .env 文件
```

### **4. 文件: `app.py`**

```python
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode, quote_plus
import ssl
import io
import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify, send_file, render_template
from docx import Document
from docx.shared import Inches # 虽然当前未直接使用，但考虑到Docx处理，可能会用到

# 加载 .env 文件中的环境变量
load_dotenv()

# --- 1. 配置您的星火大模型凭证 (从环境变量获取) ---
APPID = os.getenv("SPARK_APPID")
APISecret = os.getenv("SPARK_APISECRET")
APIKey = os.getenv("SPARK_APIKEY")

# --- 2. 星火大模型接口地址和版本 (从环境变量获取，或使用默认值) ---
SPARK_HOST = os.getenv("SPARK_HOST", "spark-api.xf-yun.com")
SPARK_DOMAIN = os.getenv("SPARK_DOMAIN", "generalv3.5") # 建议使用最新版本
SPARK_API_PATH = os.getenv("SPARK_API_PATH", "/v3.5/chat") # 根据 domain 调整路径
SPARK_URL = f"wss://{SPARK_HOST}{SPARK_API_PATH}"

# --- 3. 签名认证函数 ---
def generate_spark_auth_url(host, path, api_key, api_secret):
    """
    生成讯飞星火大模型的签名认证URL。
    参考文档: https://www.xfyun.cn/doc/spark/X1http.html#%E8%AE%A4%E8%AF%81%E6%B5%81%E7%A8%8B
    """
    # 当前时间，GMT格式
    now = datetime.datetime.now(datetime.timezone.utc)
    date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    # 构造待签名字符串
    signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"

    # 使用 HMAC-SHA256 签名
    signature_sha256 = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                hashlib.sha256).digest()
    signature_base64 = base64.b64encode(signature_sha256).decode('utf-8')

    # 构造 Authorization header
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_base64}"'
    authorization_base64 = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

    # 构造最终URL参数
    params = {
        "host": host,
        "date": date,
        "authorization": authorization_base64
    }
    return f"{SPARK_URL}?{urlencode(params)}"

# --- 4. WebSocket 连接和消息处理类 ---
class SparkWebSocketClient:
    def __init__(self, appid, api_key, api_secret, domain, host, api_path):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.domain = domain
        self.host = host
        self.api_path = api_path
        self.result_content = "" # 用于拼接AI的响应
        self.is_completed = False # 标记是否完成
        self.error_message = None # 用于存储错误信息

    def on_open(self, ws):
        # print("WebSocket连接已建立")
        # 构建请求参数
        message_json = {
            "header": {
                "app_id": self.appid,
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "temperature": 0.5, # 控制生成内容的随机性，0-1
                    "max_tokens": 4096, # 最大生成Token数
                    "top_k": 4, # 用于控制从k个最有可能的下一个词中随机选择
                }
            },
            "payload": {
                "message": {
                    "text": [
                        {"role": "system", "content": "你是一个专业的企业年度总结报告智能助手。你的任务是根据用户提供的原始工作内容，提炼并总结出年度总结报告的关键信息，并以结构化的JSON格式输出。确保内容真实、简洁、客观。如果某个部分信息不足，请留空或简要说明。对于列表形式的字段，请输出JSON数组。"},
                        {"role": "user", "content": self.user_input_prompt} # 用户输入和Prompt
                    ]
                }
            }
        }
        ws.send(json.dumps(message_json))

    def on_message(self, ws, message):
        response_data = json.loads(message)
        header = response_data['header']
        payload = response_data['payload']

        if header['code'] != 0:
            self.error_message = f"API请求失败，错误码: {header['code']}, 错误信息: {header['message']}"
            print(self.error_message)
            self.is_completed = True
            ws.close()
            return

        choices = payload['choices']
        status = choices['status'] # 0：开始；1：进行中；2：结束

        # 拼接AI生成的内容
        self.result_content += choices['text'][0]['content']

        if status == 2: # 响应结束
            # print("AI响应已完成")
            self.is_completed = True
            ws.close() # 关闭连接

    def on_error(self, ws, error):
        self.error_message = f"WebSocket错误: {error}"
        print(self.error_message)
        self.is_completed = True

    def on_close(self, ws, close_status_code, close_msg):
        # print(f"WebSocket连接已关闭. Status Code: {close_status_code}, Message: {close_msg}")
        self.is_completed = True # 确保即使异常关闭也能标记为完成

    def send_request(self, user_input_text):
        self.result_content = "" # 重置每次请求的结果
        self.is_completed = False
        self.error_message = None

        auth_url = generate_spark_auth_url(self.host, self.api_path, self.api_key, self.api_secret)
        self.user_input_prompt = self._create_spark_prompt(user_input_text) # 构造带JSON指令的Prompt

        # print(f"连接到: {auth_url}")
        ws = websocket.WebSocketApp(
            auth_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        # 运行WebSocket连接，直到完成或出错
        # cert_reqs=ssl.CERT_NONE 仅用于开发和调试，生产环境应移除或设置为ssl.CERT_REQUIRED
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}) 

        if self.error_message:
            raise Exception(self.error_message)

        return self.result_content

    def _create_spark_prompt(self, user_input_text):
        """
        构造给讯飞星火的Prompt，要求其输出JSON格式。
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

# --- 5. Flask 应用 ---
app = Flask(__name__, template_folder='templates') # 指定模板文件夹

# 初始化星火客户端
spark_client = SparkWebSocketClient(APPID, APIKey, APISecret, SPARK_DOMAIN, SPARK_HOST, SPARK_API_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    user_input = ""
    # 1. 获取用户输入
    if 'text_input' in request.form and request.form['text_input'].strip():
        user_input = request.form['text_input'].strip()
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        if file.filename.endswith('.txt'):
            try:
                user_input = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return jsonify({"error": "文件编码错误，请确保为UTF-8格式"}), 400
        elif file.filename.endswith('.docx'):
            try:
                doc = Document(file)
                for para in doc.paragraphs:
                    user_input += para.text + "\n"
                # 处理表格中的文本，如果模板中有需要提取的表格内容
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            user_input += cell.text + "\n"
            except Exception as e:
                return jsonify({"error": f"读取Docx文件失败: {str(e)}"}), 400
        else:
            return jsonify({"error": "不支持的文件类型，请上传 .txt 或 .docx 文件"}), 400
    else:
        return jsonify({"error": "请至少输入一些内容或上传一个文件"}), 400

    if not user_input.strip():
        return jsonify({"error": "输入内容为空，请提供有效信息"}), 400

    # 2. 调用星火大模型
    try:
        spark_json_str = spark_client.send_request(user_input)
        
        # 讯飞模型有时会生成markdown代码块，需要移除
        if spark_json_str.strip().startswith("```json") and spark_json_str.strip().endswith("```"):
            spark_json_str = spark_json_str.strip()[7:-3].strip()
        
        extracted_content = json.loads(spark_json_str)

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}, 原始响应: {spark_json_str}")
        return jsonify({"error": "AI模型返回内容格式错误，请稍后重试或优化输入"}), 500
    except Exception as e:
        print(f"调用星火大模型失败: {e}")
        return jsonify({"error": f"AI模型服务调用失败: {str(e)}"}), 500

    # 3. 加载并填充Docx模板
    try:
        template_path = '年度总结模板.docx'
        if not os.path.exists(template_path):
            return jsonify({"error": "年度总结模板文件不存在，请确保 '年度总结模板.docx' 在应用根目录"}), 500
            
        doc = Document(template_path)

        # 定义一个简单的填充函数
        def replace_placeholder(paragraph_or_run, placeholder, value):
            if isinstance(value, list):
                # 针对列表类型，将其转换为带项目符号的多行文本
                formatted_value = "\n".join([f"• {item}" for item in value if item and item.strip()])
                if not formatted_value: # 如果列表为空，则使用空字符串
                    formatted_value = ""
            else:
                formatted_value = str(value or '') # 确保value是非空字符串

            # 替换段落中的占位符
            if placeholder in paragraph_or_run.text:
                paragraph_or_run.text = paragraph_or_run.text.replace(placeholder, formatted_value)
            
            # 由于python-docx替换占位符可能导致格式丢失，
            # 也可以遍历runs进行替换，但较为复杂，MVP阶段先直接替换段落文本。
            # 更健壮的替换方式需要遍历paragraph.runs，识别并合并runs再替换，
            # 这里为了简洁，直接替换paragraph.text，可能会丢失部分格式。

        # 遍历所有段落进行替换
        for paragraph in doc.paragraphs:
            replace_placeholder(paragraph, '[[年度总结概述]]', extracted_content.get('年度总结概述'))
            replace_placeholder(paragraph, '[[主要成就与贡献]]', extracted_content.get('主要成就与贡献'))
            replace_placeholder(paragraph, '[[遇到的挑战及解决方案]]', extracted_content.get('遇到的挑战及解决方案'))
            replace_placeholder(paragraph, '[[个人成长与学习]]', extracted_content.get('个人成长与学习'))
            replace_placeholder(paragraph, '[[未来展望与计划]]', extracted_content.get('未来展望与计划'))
            replace_placeholder(paragraph, '[[您的姓名]]', extracted_content.get('姓名', '未填写')) # 提供默认值
            replace_placeholder(paragraph, '[[报告日期]]', extracted_content.get('报告日期', datetime.date.today().strftime('%Y年%m月%d日'))) # 提供默认值

        # 遍历所有表格的单元格进行替换（如果模板中有表格占位符）
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        replace_placeholder(paragraph, '[[您的姓名]]', extracted_content.get('姓名', '未填写'))
                        replace_placeholder(paragraph, '[[报告日期]]', extracted_content.get('报告日期', datetime.date.today().strftime('%Y年%m月%d日')))
                        # 可以添加更多表格内的特定占位符

        # 4. 生成内存中的Docx文件并返回
        byte_io = io.BytesIO()
        doc.save(byte_io)
        byte_io.seek(0) # 将指针移到文件开头

        # 构造下载文件名
        summary_name = extracted_content.get('姓名', '用户')
        summary_date = datetime.date.today().strftime('%Y%m%d')
        download_filename = f"{summary_name}-年度总结-{summary_date}.docx"

        return send_file(byte_io,
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         as_attachment=True,
                         download_name=download_filename)

    except Exception as e:
        print(f"文档处理或生成失败: {e}")
        return jsonify({"error": f"文档生成失败: {str(e)}"}), 500

if __name__ == '__main__':
    # ⚠️ 生产环境不要这样运行，请使用 Gunicorn/uWSGI 等 WSGI 服务器
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **5. 文件: `templates/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 智能填报年度总结</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f4f7f6; color: #333; }
        .container { max-width: 800px; margin: 0 auto; background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #007bff; margin-bottom: 30px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
        textarea { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; font-size: 16px; margin-bottom: 15px; min-height: 200px; resize: vertical; }
        input[type="file"] { margin-bottom: 15px; border: 1px solid #ccc; padding: 8px; border-radius: 5px; background-color: #f9f9f9; width: 100%; box-sizing: border-box; }
        button { background-color: #28a745; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 18px; display: block; width: 100%; transition: background-color 0.3s ease; }
        button:hover { background-color: #218838; }
        .result-section { margin-top: 30px; text-align: center; }
        .loading { display: none; color: #007bff; font-size: 1.1em; }
        .error { color: #dc3545; font-weight: bold; margin-top: 10px; display: none; }
        .download-link { display: none; margin-top: 20px; }
        .download-link a { background-color: #007bff; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-size: 1.1em; }
        .download-link a:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI 智能填报年度总结</h1>
        <form id="summaryForm">
            <p>请提供您的工作内容、项目进展、个人思考等，AI将为您提炼并填报年度总结。</p>
            <label for="textInput">手动输入内容：</label>
            <textarea id="textInput" name="text_input" placeholder="例如：今年我主要负责了A项目，完成了...；B项目遇到了...挑战，我通过...解决；学习了C技术，提升了...技能；明年的计划是..."></textarea>

            <label for="fileInput">或上传文件（仅支持 .txt 或 .docx 格式）：</label>
            <input type="file" id="fileInput" name="file" accept=".txt,.docx">

            <button type="submit">生成年度总结</button>
        </form>

        <div class="result-section">
            <p class="loading" id="loadingMessage">AI 正在努力分析中，请稍候...</p>
            <p class="error" id="errorMessage"></p>
            <div class="download-link" id="downloadLink">
                <a href="#" id="downloadBtn">点击下载生成的年度总结</a>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('summaryForm').addEventListener('submit', async function(event) {
            event.preventDefault(); // 阻止表单默认提交

            const textInput = document.getElementById('textInput').value;
            const fileInput = document.getElementById('fileInput').files[0];
            const loadingMessage = document.getElementById('loadingMessage');
            const errorMessage = document.getElementById('errorMessage');
            const downloadLink = document.getElementById('downloadLink');
            const downloadBtn = document.getElementById('downloadBtn');

            // 重置状态
            loadingMessage.style.display = 'none';
            errorMessage.style.display = 'none';
            downloadLink.style.display = 'none';
            errorMessage.textContent = '';
            downloadBtn.removeAttribute('download'); // 清除上次的下载文件名
            downloadBtn.href = '#';

            // 检查是否有输入
            if (!textInput.trim() && !fileInput) {
                errorMessage.textContent = '请至少输入一些内容或上传一个文件。';
                errorMessage.style.display = 'block';
                return;
            }

            loadingMessage.style.display = 'block';

            const formData = new FormData();
            if (fileInput) {
                formData.append('file', fileInput);
            } else {
                formData.append('text_input', textInput);
            }

            try {
                const response = await fetch('/generate_summary', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob(); // 获取二进制数据
                    const url = URL.createObjectURL(blob); // 创建一个临时的URL
                    downloadBtn.href = url;
                    
                    // 尝试从响应头获取文件名
                    const contentDisposition = response.headers.get('Content-Disposition');
                    if (contentDisposition) {
                        const filenameMatch = contentDisposition.match(/filename\*?=(?:UTF-8'')?([^;]+)/);
                        if (filenameMatch && filenameMatch[1]) {
                            let filename = decodeURIComponent(filenameMatch[1].replace(/%20/g, ' ')); // 解码文件名中的URI编码，并替换空格
                            filename = filename.replace(/^"|"$/g, ''); // 移除可能的引号
                            downloadBtn.download = filename; // 设置下载文件名
                        }
                    } else {
                        downloadBtn.download = '生成的年度总结.docx'; // 默认文件名
                    }
                    downloadLink.style.display = 'block';
                } else {
                    const errorData = await response.json();
                    errorMessage.textContent = errorData.error || '生成失败，请稍后重试。';
                    errorMessage.style.display = 'block';
                }
            } catch (error) {
                console.error('Fetch error:', error);
                errorMessage.textContent = '网络请求失败，请检查网络或联系管理员。';
                errorMessage.style.display = 'block';
            } finally {
                loadingMessage.style.display = 'none';
            }
        });
    </script>
</body>
</html>
```

---
**提示给Augment：**

*   请确保`app.py`中的所有占位符替换逻辑能够正确处理AI返回的**列表类型数据**，将其转换为带项目符号的多行字符串。
*   在`SparkWebSocketClient`类的`_create_spark_prompt`方法中，请务必保持给星火大模型的JSON输出格式指令的**严格性**，这是确保后续解析成功的关键。
*   `sslopt={"cert_reqs": ssl.CERT_NONE}`在`ws.run_forever()`中是为了方便开发，在生产环境部署时应移除或设置为`ssl.CERT_REQUIRED`。
*   `年度总结模板.docx`文件内容不需要你生成，但请在`app.py`中引用它的存在。
*   请确保所有必要的`import`语句都已包含。
*   请注意`.env.example`文件中变量的命名与`app.py`中`os.getenv()`调用匹配。