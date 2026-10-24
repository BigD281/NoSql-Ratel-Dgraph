@echo off
chcp 65001 >nul
echo ============================================================
echo   NAP DU LIEU MAU BANG DGRAPH LIVE LOADER (dgraph.exe live)
echo ============================================================

set "BASE_DIR=%~dp0.."
set "BIN_DIR=%BASE_DIR%\dgraph-bin"
set "DB_DIR=%BASE_DIR%\database"

"%BIN_DIR%\dgraph.exe" live -f "%DB_DIR%\data.rdf" -s "%DB_DIR%\schema.dql" --alpha localhost:9080 --zero localhost:5080

