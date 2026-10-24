@echo off
chcp 65001 >nul
echo ============================================================
echo   KHOI DONG UNG DUNG WEB DEMO: HR GRAPH 360 (PORT 5000)
echo ============================================================
set "BASE_DIR=%~dp0.."
start http://127.0.0.1:5000
python "%BASE_DIR%\app\server.py"

