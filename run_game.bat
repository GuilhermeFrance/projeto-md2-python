@echo off
REM PathFinder Adventure - Launcher para Windows
REM Este script instala as dependências e executa o jogo

echo.
echo ╔════════════════════════════════════════╗
echo ║   🧙 PathFinder Adventure Setup 🧙    ║
echo ║  Jogo de Grafos e Matemática Discreta ║
echo ╚════════════════════════════════════════╝
echo.

REM Verifica se py.exe está disponível
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não foi encontrado!
    echo.
    echo Por favor, instale Python em: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.
echo 📦 Instalando dependências...
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)

echo.
echo ✅ Dependências instaladas com sucesso!
echo.
echo 🎮 Iniciando PathFinder Adventure...
echo.

py main.py

pause
