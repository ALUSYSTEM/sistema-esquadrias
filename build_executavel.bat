@echo off
chcp 65001 >nul
echo ========================================
echo   Construindo Executável
echo   Sistema de Esquadrias
echo ========================================
echo.

echo [1/4] Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller não encontrado. Instalando...
    pip install pyinstaller==6.1.0
    if errorlevel 1 (
        echo ERRO: Não foi possível instalar o PyInstaller
        pause
        exit /b 1
    )
)
echo PyInstaller OK!
echo.

echo [2/4] Limpando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo Limpeza concluída!
echo.

echo [3/4] Construindo executável...
echo Isso pode levar alguns minutos...
python -m PyInstaller sistema_esquadrias.spec --clean
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao construir o executável
    pause
    exit /b 1
)
echo.

echo [4/4] Criando launcher...
echo @echo off > "dist\Sistema_Esquadrias\executar.bat"
echo chcp 65001 ^>nul >> "dist\Sistema_Esquadrias\executar.bat"
echo cls >> "dist\Sistema_Esquadrias\executar.bat"
echo echo ======================================== >> "dist\Sistema_Esquadrias\executar.bat"
echo echo    Sistema de Esquadrias >> "dist\Sistema_Esquadrias\executar.bat"
echo echo ======================================== >> "dist\Sistema_Esquadrias\executar.bat"
echo echo. >> "dist\Sistema_Esquadrias\executar.bat"
echo echo Iniciando sistema... >> "dist\Sistema_Esquadrias\executar.bat"
echo echo. >> "dist\Sistema_Esquadrias\executar.bat"
echo start http://localhost:5000 >> "dist\Sistema_Esquadrias\executar.bat"
echo Sistema_Esquadrias.exe >> "dist\Sistema_Esquadrias\executar.bat"
echo pause >> "dist\Sistema_Esquadrias\executar.bat"

echo.
echo ========================================
echo   EXECUTÁVEL CRIADO COM SUCESSO!
echo ========================================
echo.
echo Localização: dist\Sistema_Esquadrias\
echo.
echo Para executar:
echo 1. Vá para a pasta: dist\Sistema_Esquadrias
echo 2. Execute: executar.bat
echo.
echo Credenciais padrão:
echo    Usuário: admin
echo    Senha: admin123
echo.
echo ========================================
pause

