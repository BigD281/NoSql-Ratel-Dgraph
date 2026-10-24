@echo off
chcp 65001 >nul
echo ============================================================
echo   DUNG CAC TIEN TRINH DGRAPH VA RATEL TREN WINDOWS
echo ============================================================

taskkill /F /IM dgraph-ratel.exe 2>nul
if %errorlevel% equ 0 (
    echo [OK] Da dung dgraph-ratel.exe
) else (
    echo [INFO] dgraph-ratel.exe khong dang chay.
)

taskkill /F /IM dgraph.exe 2>nul
if %errorlevel% equ 0 (
    echo [OK] Da dung dgraph.exe (Zero va Alpha)
) else (
    echo [INFO] dgraph.exe khong dang chay.
)

echo [HOAN TAT] Da giai phong cac cong 5080, 6080, 7080, 8080, 9080, 8000.

