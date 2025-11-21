@echo off
REM PathFinder Adventure - Launcher para Windows com Python 3.11
REM Este script executa o jogo usando Python 3.11 (versão estável)

echo.
echo ╔════════════════════════════════════════╗
echo ║   🧙 PathFinder Adventure Setup 🧙    ║
echo ║  Jogo de Grafos e Matemática Discreta ║
echo ║        Python 3.11 Estável            ║
echo ╚════════════════════════════════════════╝
echo.

echo Verificando Python 3.11...
py -3.11 --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 3.11 não encontrado!
    echo Por favor, instale Python 3.11 usando: winget install Python.Python.3.11
    pause
    exit /b 1
)

echo ✅ Python 3.11 encontrado!
echo.
echo Iniciando PathFinder Adventure...
echo.

REM Executar o jogo
py -3.11 main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erro ao executar o jogo!
    pause
    exit /b 1
)

echo.
echo ✅ Jogo finalizado com sucesso!
pause