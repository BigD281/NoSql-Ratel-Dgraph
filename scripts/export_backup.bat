@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================================
echo   EXPORT DU LIEU (RDF + JSON) VA BACKUP CSDL DO THI DGRAPH
echo ============================================================

set "BASE_DIR=%~dp0.."
set "DATA_DIR=%BASE_DIR%\dgraph-data"
set "BACKUP_DIR=%BASE_DIR%\backups"

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo.
echo [1/3] Goi API /admin cua Dgraph Alpha de Export du lieu ra dinh dang RDF...
curl.exe -s -X POST http://localhost:8080/admin -H "Content-Type: application/json" -d "{\"query\": \"mutation { export(input: { format: \\\"rdf\\\" }) { response { code message } exportedFiles } }\"}"
echo.

echo.
echo [2/3] Goi API /admin cua Dgraph Alpha de Export du lieu ra dinh dang JSON...
curl.exe -s -X POST http://localhost:8080/admin -H "Content-Type: application/json" -d "{\"query\": \"mutation { export(input: { format: \\\"json\\\" }) { response { code message } exportedFiles } }\"}"
echo.

echo.
echo [3/3] Sao luu cac file Export (.rdf.gz, .json.gz, .schema.gz) va Snapshot sang thu muc backups\...
if exist "%DATA_DIR%\export" (
    xcopy /E /I /Y "%DATA_DIR%\export" "%BACKUP_DIR%\export_latest" >nul
    echo [OK] Da sao luu ban Export moi nhat vao: %BACKUP_DIR%\export_latest
    dir /S /B "%BACKUP_DIR%\export_latest"
) else (
    echo [CANH BAO] Khong tim thay thu muc %DATA_DIR%\export
)

copy /Y "%BASE_DIR%\database\schema.dql" "%BACKUP_DIR%\schema_backup.dql" >nul
copy /Y "%BASE_DIR%\database\data.rdf" "%BACKUP_DIR%\data_backup.rdf" >nul
copy /Y "%BASE_DIR%\database\data.json" "%BACKUP_DIR%\data_backup.json" >nul
echo [HOAN TAT] Da luu day du ban sao luu tai thu muc: %BACKUP_DIR%
endlocal

