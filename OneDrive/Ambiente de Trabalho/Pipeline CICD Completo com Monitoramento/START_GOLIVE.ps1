#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Inicia o servidor GO LIVE Dashboard
.DESCRIPTION
    Script para iniciar o servidor HTTP local do GO LIVE Dashboard
    Abre automaticamente no navegador em http://localhost:8080
#>

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  GO LIVE Dashboard - Servidor Local" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Detectar Python
$pythonCmd = $null

# Tentar python3
try {
    $test = python3 --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python3"
        Write-Host "✓ Python3 encontrado" -ForegroundColor Green
    }
}
catch {
    # Tentar python
    try {
        $test = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "python"
            Write-Host "✓ Python encontrado" -ForegroundColor Green
        }
    }
    catch {
        Write-Host ""
        Write-Host "❌ ERRO: Python não encontrado no sistema!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Instale Python em: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

Write-Host ""
Write-Host "Iniciando servidor em http://localhost:8080" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Rodar o servidor
& $pythonCmd serve_golive.py
