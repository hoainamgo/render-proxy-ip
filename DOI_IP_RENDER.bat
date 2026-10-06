@echo off
setlocal EnableDelayedExpansion
title CONG CU DOI IP RENDER SINGAPORE (1-CLICK)
color 0B

:MENU
cls
echo ================================================================
echo        CONG CU DOI IP SANG RENDER SINGAPORE (1-CLICK)
echo ================================================================
echo.
echo    [1] BAT DOI IP  - Chuyen toan bo may tinh sang IP Singapore
echo    [2] TAT DOI IP  - Khoi phuc lai IP Mang Goc
echo    [3] KIEM TRA IP - Xem dia chi IP va vi tri thuc te
echo    [4] Thoat
echo.
echo ================================================================
set "choice="
set /p choice="Nhap lua chon cua ban [1, 2, 3, 4]: "

if "%choice%"=="1" goto BAT_IP
if "%choice%"=="2" goto TAT_IP
if "%choice%"=="3" goto CHECK_IP
if "%choice%"=="4" goto THOAT
goto MENU

:BAT_IP
cls
echo [INFO] Dang khoi dong cau noi va doi IP he thong...
echo.
python "%~dp0render_proxy_service\local_bridge.py"
pause
goto MENU

:TAT_IP
cls
echo [INFO] Dang tat Proxy va khoi phuc IP mang goc...
python "%~dp0render_proxy_service\local_bridge.py" off
echo.
echo [DONE] Da khoi phuc mang goc thanh cong!
echo.
pause
goto MENU

:CHECK_IP
cls
echo [INFO] Dang kiem tra IP hien tai cua may tinh...
python "%~dp0render_proxy_service\local_bridge.py" check
echo.
pause
goto MENU

:THOAT
exit /b 0
