@echo off
rem ============================================================
rem  启动 OAS 控制服务（给 OASX 前端连的接口）
rem  GUI 和这个可以同时跑，也可以只跑这一个
rem ============================================================
setlocal

set "TOOLKIT=D:\Zun\toolkit"
set "REPO=D:\Zun\repos\OnmyojiAutoScript"
set "PY=%TOOLKIT%\Python310\python.exe"
set "GITROOT=D:\Zun\tools\PortableGit"
set "PSI=%TOOLKIT%\Python310\Lib\site-packages\PySide6"

set "PATH=%PSI%;%REPO%\toolkit;%GITROOT%\cmd;%GITROOT%\mingw64\bin;%TOOLKIT%\Python310;%TOOLKIT%\Python310\Scripts;%PATH%"

set "PIP_CONFIG_FILE=%TOOLKIT%\pip.ini"
set "PIP_CACHE_DIR=%TOOLKIT%\pip-cache"
set "TMPDIR=%TOOLKIT%\tmp"
set "TEMP=%TOOLKIT%\tmp"
set "TMP=%TOOLKIT%\tmp"
set "GIT_CONFIG_GLOBAL=D:\Zun\repos\.gitconfig"
set "HTTP_PROXY=http://127.0.0.1:7897"
set "HTTPS_PROXY=http://127.0.0.1:7897"
set "NO_PROXY=127.0.0.1,localhost"
set "PYTHONUTF8=1"

cd /d "%REPO%"

echo.
echo   正在启动 OAS 控制服务...
echo     端口: 22288（默认）
echo     启动后用 OASX 前端连接 127.0.0.1:22288
echo     按 Ctrl+C 停止
echo.

"%PY%" server.py

echo.
echo   服务已退出（退出码 %ERRORLEVEL%）
pause
endlocal
