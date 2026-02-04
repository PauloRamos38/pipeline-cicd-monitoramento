@echo off
REM Inicia o servidor GO LIVE Dashboard
REM Este script abre o GO_LIVE.html em um servidor HTTP local

echo.
echo ==========================================
echo  GO LIVE Dashboard - Servidor Local
echo ==========================================
echo.

REM Detectar Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Python encontrado
    echo.
    echo Iniciando servidor em http://localhost:8080
    echo.
    python serve_golive.py
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✓ Python3 encontrado
        echo.
        echo Iniciando servidor em http://localhost:8080
        echo.
        python3 serve_golive.py
    ) else (
        echo.
        echo ❌ ERRO: Python não encontrado no sistema!
        echo.
        echo Instale Python em: https://www.python.org/downloads/
        echo.
        pause
    )
)
