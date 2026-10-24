@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================================
echo   KHOI DONG HE QUAN TRI CSDL DO THI DGRAPH VA GUI RATEL
echo   [Phien ban Windows Native v20.11.3 - Khong dung Docker]
echo ============================================================

set "BASE_DIR=%~dp0.."
set "BIN_DIR=%BASE_DIR%\dgraph-bin"
set "DATA_DIR=%BASE_DIR%\dgraph-data"

if not exist "%BIN_DIR%\dgraph.exe" (
    echo [LOI] Khong tim thay "%BIN_DIR%\dgraph.exe"!
    echo Vui long tai va giai nen dgraph-windows-amd64.zip vao thu muc:
    echo   %BIN_DIR%
    exit /b 1
)

if not exist "%DATA_DIR%\zw" mkdir "%DATA_DIR%\zw"
if not exist "%DATA_DIR%\p" mkdir "%DATA_DIR%\p"
if not exist "%DATA_DIR%\w" mkdir "%DATA_DIR%\w"

echo [1/3] Khoi dong Dgraph Zero [Cong 5080 / HTTP 6080]...
start "Dgraph Zero" /MIN /D "%DATA_DIR%" "%BIN_DIR%\dgraph.exe" zero --my=localhost:5080 --wal="%DATA_DIR%\zw"

ping 127.0.0.1 -n 4 >nul

echo [2/3] Khoi dong Dgraph Alpha [Cong 7080 / HTTP 8080 / gRPC 9080]...
start "Dgraph Alpha" /MIN /D "%DATA_DIR%" "%BIN_DIR%\dgraph.exe" alpha --my=localhost:7080 --zero=localhost:5080 --whitelist=0.0.0.0/0,localhost --cache_mb=1024 --postings="%DATA_DIR%\p" --wal="%DATA_DIR%\w"

ping 127.0.0.1 -n 6 >nul

if exist "%BIN_DIR%\dgraph-ratel.exe" (
    echo [3/3] Khoi dong giao dien GUI Dgraph Ratel [Cong 8000]...
    start "Dgraph Ratel GUI" /MIN /D "%DATA_DIR%" "%BIN_DIR%\dgraph-ratel.exe" -port 8000 -addr http://localhost:8080
    ping 127.0.0.1 -n 3 >nul
    echo.
    echo [HOAN TAT] Cac thanh phan da duoc khoi dong thanh cong:
    echo   - Dgraph Zero HTTP  : http://localhost:6080/state
    echo   - Dgraph Alpha HTTP : http://localhost:8080/health
    echo   - Dgraph Ratel GUI  : http://localhost:8000/?local
) else (
    echo [3/3] Khong tim thay dgraph-ratel.exe cuc bo, dung https://play.dgraph.io
)

echo.
echo De kiem tra trang thai, chay: scripts\check_dgraph.bat
echo De dung toan bo dich vu, chay: scripts\stop_dgraph.bat
endlocal
