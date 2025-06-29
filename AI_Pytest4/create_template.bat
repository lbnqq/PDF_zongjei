@echo off
echo 正在创建年度总结模板文件...
echo.

REM 尝试不同的Python命令
python generate_template.py 2>nul
if %errorlevel% equ 0 goto success

python3 generate_template.py 2>nul
if %errorlevel% equ 0 goto success

py generate_template.py 2>nul
if %errorlevel% equ 0 goto success

py -3 generate_template.py 2>nul
if %errorlevel% equ 0 goto success

echo ❌ 未找到Python解释器或缺少依赖
echo.
echo 请按以下步骤手动创建模板：
echo 1. 打开Microsoft Word或WPS Office
echo 2. 创建新文档
echo 3. 复制 "模板内容.txt" 中的内容到Word文档
echo 4. 设置合适的格式（标题、字体等）
echo 5. 保存为 "年度总结模板.docx"
echo.
echo 或者安装Python依赖后重试：
echo pip install python-docx
goto end

:success
echo ✅ 模板文件创建成功！
echo 文件位置：年度总结模板.docx

:end
pause
