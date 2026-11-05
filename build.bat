@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

echo ============================================
echo   暗门 · 生成本地 PDF
echo ============================================
echo.

set "PY=python"
where python >nul 2>nul
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else (
        where py >nul 2>nul
        if errorlevel 1 (
            echo [错误] 没有找到 Python。请先安装 Python 3.10 以上版本，
            echo        安装时勾选 "Add Python to PATH"。
            echo.
            pause
            exit /b 1
        )
        set "PY=py -3"
    )
)

%PY% -c "import markdown, pymupdf, playwright, PIL" >nul 2>nul
if errorlevel 1 (
    echo [准备] 首次运行，正在安装依赖……
    %PY% -m pip install --upgrade pip >nul
    %PY% -m pip install markdown pymupdf pillow playwright
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络。
        pause
        exit /b 1
    )
)

echo [1/2] 重新绘制插图……
for /d %%d in (book\code\ch*) do (
    if exist "%%d\figures.py" (
        %PY% "%%d\figures.py" >nul 2>nul
        if errorlevel 1 echo   [警告] %%d 绘图失败，已跳过
    )
)

echo [2/2] 排版并生成 PDF……
%PY% book\build\build_pdf.py
if errorlevel 1 (
    echo.
    echo [失败] 构建没有完成，请查看上方报错。
    pause
    exit /b 1
)

echo.
echo 完成：output\dark-gate.pdf
echo.
pause
