@echo off
title Sistema Multiagente - Clases Multimedia
cd /d "%~dp0"
echo ===============================================================
echo   SISTEMA MULTIAGENTE PARA DISENO DE CLASES MULTIMEDIA
echo   Iniciando servidor local en http://127.0.0.1:8000
echo ===============================================================
echo.
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause

