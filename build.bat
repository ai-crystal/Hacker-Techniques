@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

set "PY=python"
where python >nul 2>nul
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else (
        where py >nul 2>nul
        if errorlevel 1 (
            echo [错误] 没有找到 Python，请安装 Python 3.10 以上版本并在安装时勾选 Add to PATH。
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

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=all"
if /i "%TARGET%"=="figures" goto :figures

echo ============================================
echo   黑客技术与安全原理 · 构建 %TARGET%
echo ============================================
echo.

%PY% books\build\build.py --book %TARGET%
if errorlevel 1 (
    echo.
    echo [失败] 构建没有完成，请查看上方报错。
    pause
    exit /b 1
)

%PY% books\build\gen_sidebars.py
echo.
echo 完成。PDF 在 output\ 目录，站点入口 index.html。
echo.
pause
exit /b 0

:figures
echo [1/1] 重画全系列插图……
for /d %%b in (books\beginner books\theory books\practice) do (
    for /d %%c in (%%b\code\ch*) do (
        if exist "%%c\figures.py" (
            %PY% "%%c\figures.py" >nul 2>nul
            if errorlevel 1 echo   [警告] %%c 绘图失败
        )
    )
)
echo 完成。
pause
exit /b 0
