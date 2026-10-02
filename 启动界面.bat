@echo off
rem ============================================================
rem  启动 OAS 图形界面（双击即可）
rem  所有环境都在 D:\Zun 内，不依赖系统安装
rem ============================================================
setlocal

set "TOOLKIT=D:\Zun\toolkit"
set "REPO=D:\Zun\repos\OnmyojiAutoScript"
set "PY=%TOOLKIT%\Python310\python.exe"
set "GITROOT=D:\Zun\tools\PortableGit"
set "PSI=%TOOLKIT%\Python310\Lib\site-packages\PySide6"

rem Qt 加载 fluentuiplugin.dll 时按 PATH 找依赖，这两段必须有
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

rem gui.py 用当前目录找 app.qml，必须在项目根启动
cd /d "%REPO%"

echo.
echo   正在启动 OAS 图形界面...
echo     目录: %REPO%
echo     解释器: %PY%
echo.

"%PY%" gui.py

echo.
echo   GUI 已退出（退出码 %ERRORLEVEL%）
echo   若报错，把上面的信息截图发给 AI
pause
endlocal
