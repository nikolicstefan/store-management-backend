@echo off

set cmd=%1
set target=%2

set invalid_target=Invalid target: %target%

if "%cmd%"=="" (
    call :help
    exit /b 1
)

if "%cmd%"=="init" (
    set "usage=Usage: .\cmd_db.bat init [auth^|owner]"
    call :set_app
    if errorlevel 1 exit /b 1
    call :init
    exit /b
)

if "%cmd%"=="migrate" (
    set "usage=Usage: .\cmd_db.bat migrate [auth^|owner] -m "Migration message""
    call :set_app
    if errorlevel 1 exit /b 1
    call :migrate %3 %4
    exit /b
)

if "%cmd%"=="upgrade" (
    set "usage=Usage: .\cmd_db.bat upgrade [auth^|owner]"
    call :set_app
    if errorlevel 1 exit /b 1
    call :upgrade
    exit /b
)

echo Invalid command: %cmd%
call :help
exit /b 1

:set_app
if "%target%"=="auth" (
    set app=app.py
    exit /b 0
)

if "%target%"=="owner" (
    set app=owner.app
    exit /b 0
)

if not "%target%"=="" (
    echo %invalid_target%
)

echo %usage%
exit /b 1

:init
docker compose exec %target% flask --app %app% db init
docker compose exec %target% flask --app %app% db migrate -m "Initial migration"
docker compose exec %target% flask --app %app% db upgrade
exit /b

:migrate
set flag=%1
set msg=%~2

set invalid_flag=Invalid flag: %flag%

if "%flag%"=="" (
    echo %usage%
    exit /b 1
)

if not "%flag%"=="-m" (
    echo %invalid_flag%
    echo %usage%
    exit /b 1
)

if "%msg%"=="" (
    echo %usage%
    exit /b 1
)

docker compose exec %target% flask --app %app% db migrate -m "%msg%"
docker compose exec %target% flask --app %app% db upgrade
exit /b

:upgrade
docker compose exec %target% flask --app %app% db upgrade
exit /b

:help
echo Usage: .\cmd_db.bat [command]
echo Commands:
echo   init [auth^|owner]                               Initialize migrations and apply the initial migration
echo   migrate [auth^|owner] -m "Migration message"     Create and apply a new migration
echo   upgrade [auth^|owner]                            Apply the latest migrations
exit /b 1
