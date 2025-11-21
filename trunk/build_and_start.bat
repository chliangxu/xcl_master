@echo off
chcp 65001 >nul

net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WorkingDirectory '%~dp0'"
    exit /b
)

cd /d "%~dp0"

echo ========================================
echo    CJGameStudio 一键构建与启动
echo ========================================
echo.
echo 当前目录: %CD%
echo.

echo [1/4] 清理上次构建缓存...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del /f /q "*.spec"
for /r %%i in (*.pyc) do @del /f /q "%%i" 2>nul
for /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i" 2>nul
echo 清理完成！
echo.

echo [2/4] 开始构建...
python build.py
if %errorlevel% neq 0 (
    echo.
    echo 构建失败！请检查错误信息。
    pause
    exit /b %errorlevel%
)
echo.

echo [3/4] 检查构建产物...
if not exist "dist\CJGameStudio.exe" (
    echo.
    echo 错误：找不到构建的 exe 文件！
    pause
    exit /b 1
)
echo 构建产物检查通过！
echo.

echo [4/4] 启动应用程序...
echo.
cd dist
start "" "CJGameStudio.exe"
cd ..

echo.
echo ========================================
echo    启动完成！
echo ========================================
echo.
echo 应用已在后台运行，可以关闭此窗口。
timeout /t 3 >nul
