@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================================
echo   IMPORT VA RESTORE CSDL DO THI DGRAPH (KHONG DUNG DOCKER)
echo ============================================================

set "BASE_DIR=%~dp0.."
set "BIN_DIR=%BASE_DIR%\dgraph-bin"
set "DB_DIR=%BASE_DIR%\database"

echo.
echo [Cach 1] Khoi phuc Schema + Du lieu mau bang Python HTTP API (Nhanh & Chinh xac):
python "%DB_DIR%\seed_data.py"

echo.
echo ------------------------------------------------------------
echo [Ghi chu Cach 2 - Dung Dgraph Live Loader chinh thuc]:
echo   "%BIN_DIR%\dgraph.exe" live -f "%DB_DIR%\data.rdf" -s "%DB_DIR%\schema.dql" --alpha localhost:9080 --zero localhost:5080
echo ============================================================
endlocal

