@echo off

set bd=%1
set ostools=%2
set rd=%3
set plugdir=%4
for /F %%i in ("%4") do @set plugin=%%~nxi

call :banner 
echo Batch plugin example:
echo.
echo Plugin Name = %plugin%
echo Base Directory = %bd%
echo OS Tools Directory = %ostools%
echo ROM Directory = %rd%
echo Plugin Directory = %plugdir%
echo.
echo *** Add more plugins to /kitchen/tools/plugins ***
echo.
echo.

set /p reply=Would you like to see the contents of your ROM directory?  y/n
if %reply%==y (
    echo.
    cd /d %rd%
    dir /b

    echo.
    pause
)

:banner
cls
echo ------------------------------------------------------------
echo                      Batch plugin example
echo                            by SuperR
echo ------------------------------------------------------------
echo.
exit /b 0
