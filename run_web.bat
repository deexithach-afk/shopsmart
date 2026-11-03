@echo off
title ShopSmart - Localhost Web Server
echo ===================================================
echo    Starting ShopSmart on Localhost (Port 5000)...
echo ===================================================
echo.
echo Opening http://localhost:5000 in your browser...
start http://localhost:5000
python app.py
pause

