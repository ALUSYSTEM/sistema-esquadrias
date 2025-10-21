@echo off
echo ========================================
echo Sistema de Esquadrias - ALUBRAS
echo ========================================
echo.
echo Iniciando servidor local...
echo.
echo O sistema sera aberto em: http://localhost:8000
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.

start http://localhost:8000
python -m http.server 8000
