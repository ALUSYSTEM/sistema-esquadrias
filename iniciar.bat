@echo off
echo ========================================
echo    Sistema de Esquadrias - Iniciando
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo Dependencias OK!
echo.

echo Iniciando sistema...
echo.
echo ========================================
echo   Sistema rodando em: http://localhost:5000
echo   Usuario: admin
echo   Senha: admin123
echo ========================================
echo.
echo Pressione Ctrl+C para parar o sistema
echo.

python app.py

pause
