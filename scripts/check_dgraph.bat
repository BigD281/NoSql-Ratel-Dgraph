@echo off
chcp 65001 >nul
echo ============================================================
echo   KIEM TRA TRANG THAI DGRAPH ZERO, ALPHA VA RATEL
echo ============================================================

echo.
echo 1. Kiem tra tien trinh dang chay:
tasklist | findstr /I "dgraph"
if %errorlevel% neq 0 (
    echo [CANH BAO] Chua co tien trinh dgraph.exe hoac dgraph-ratel.exe nao dang chay!
)

echo.
echo 2. Kiem tra Dgraph Alpha Health (http://localhost:8080/health):
curl.exe -s http://localhost:8080/health
echo.

echo.
echo 3. Kiem tra Dgraph Zero State (http://localhost:6080/state):
curl.exe -s http://localhost:6080/state | powershell -NoProfile -Command "$input | Select-Object -First 5"
echo.

echo ============================================================

