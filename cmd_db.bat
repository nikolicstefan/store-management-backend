@echo off

set cmd=%1
set target=%2

if "%cmd%"=="" (
    call :help
    exit /b 1
)

if "%cmd%"=="init" (
    call :init
    exit /b
)

if "%cmd%"=="migrate" (
    call :migrate %3 %4
    exit /b
)

if "%cmd%"=="upgrade" (
    call :upgrade
    exit /b
)

echo Invalid command: %cmd%
call :help
exit /b 1

:init
set usage=Usage: .\cmd_db.bat init auth
set invalid_target=Invalid target: %target%

if "%target%"=="" (
    echo %usage%
    exit /b 1
)

if not "%target%"=="auth" (
    echo %invalid_target%
    echo %usage%
    exit /b 1
)

docker compose exec %target% flask --app app.py db init
docker compose exec %target% flask --app app.py db migrate -m "Initial migration"
docker compose exec %target% flask --app app.py db upgrade
exit /b

:migrate
set flag=%1
set msg=%~2

set usage=Usage: .\cmd_db.bat migrate auth -m "Migration message"
set invalid_target=Invalid target: %target%
set invalid_flag=Invalid flag: %flag%

if "%target%"=="" (
    echo %usage%
    exit /b 1
)

if not "%target%"=="auth" (
    echo %invalid_target%
    echo %usage%
    exit /b 1
)

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

docker compose exec %target% flask --app app.py db migrate -m "%msg%"
docker compose exec %target% flask --app app.py db upgrade
exit /b

:upgrade
set usage=Usage: .\cmd_db.bat upgrade auth
set invalid_target=Invalid target: %target%

if "%target%"=="" (
    echo %usage%
    exit /b 1
)

if not "%target%"=="auth" (
    echo %invalid_target%
    echo %usage%
    exit /b 1
)

docker compose exec %target% flask --app app.py db upgrade
exit /b

:help
echo Usage: .\cmd_db.bat [command]
echo Commands:
echo   init auth                            Initialize migrations and apply the initial migration
echo   migrate auth -m "Migration message"  Create and apply a new migration
echo   upgrade auth                         Apply the latest migrations
exit /b 1
