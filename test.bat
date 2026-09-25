@echo off
rem ============================================
rem  OAS 开发测试环境（D:\Zun 源码版）
rem  双击打开后即可使用 python / git / adb
rem ============================================
set "_root=%~dp0"
set "_root=%_root:~0,-1%"
cd "%_root%"

color F0
title OAS Dev Test Console

set "_pyBin=%_root%\toolkit"
set "_GitBin=%_root%\toolkit\Git\mingw64\bin"
set "_adbBin=%_root%\toolkit\Lib\site-packages\adbutils\binaries"
set "PATH=%_pyBin%;%_pyBin%\Scripts;%_GitBin%;%_adbBin%;%PATH%"

echo.
echo  OAS 开发测试环境已就绪（python / git / adb 已加入 PATH）
echo.
echo  常用测试命令：
echo    python -c "import module.xxx"       检查某模块能否导入
echo    python -c "from deploy.config import DeployConfig; c=DeployConfig()"   检查配置
echo    python server.py                    启动后端服务（端口 22267/22268/22269）
echo    python gui.py                       启动 GUI
echo    git status                          查看当前改动
echo    git log --oneline -5                查看最近提交
echo.
cmd /Q /K
