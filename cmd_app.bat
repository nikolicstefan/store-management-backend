@echo off

set cmd=%1

if "%cmd%"=="" (
    call :help
    exit /b 1
)

if "%cmd%"=="up" (
    docker compose up --build
    exit /b
)

if "%cmd%"=="down" (
    docker compose down
    exit /b
)

if "%cmd%"=="reset" (
    docker compose down -v
    docker compose up --build
    exit /b
)

echo Invalid command: %cmd%
call :help
exit /b 1

:help
echo Usage: .\cmd_app.bat [command]
echo Commands:
echo   up       Build and start the application
echo   down     Stop the application and remove containers, preserving volumes
echo   reset    Stop the application, remove containers and volumes, then rebuild and start the application
exit /b 1
