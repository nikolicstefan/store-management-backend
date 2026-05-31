@echo off

set cmd=%1
set target=%2

set invalid_target=Invalid target: %target%

if "%cmd%"=="" (
    call :help
    exit /b 1
)

if "%cmd%"=="init" (
    set "usage=Usage: .\cmd_db.bat init [auth^|owner^|customer]"
    call :set_app
    if errorlevel 1 exit /b 1
    call :init
    exit /b 0
)

if "%cmd%"=="migrate" (
    set "usage=Usage: .\cmd_db.bat migrate [auth^|owner^|customer] -m "Migration message""
    call :set_app
    if errorlevel 1 exit /b 1
    call :migrate %3 %4
    exit /b 0
)

if "%cmd%"=="upgrade" (
    set "usage=Usage: .\cmd_db.bat upgrade [auth^|owner^|customer]"
    call :set_app
    if errorlevel 1 exit /b 1
    call :upgrade
    exit /b 0
)

if "%cmd%"=="dump" (
    set "usage=Usage: .\cmd_db.bat dump [auth^|store]"
    call :set_queries
    if errorlevel 1 exit /b 1
    call :dump
    exit /b 0
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

if "%target%"=="customer" (
    set app=customer.app
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
exit /b 0

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
exit /b 0

:upgrade
docker compose exec %target% flask --app %app% db upgrade
exit /b 0

:set_queries
set "queries=-c "select * from alembic_version;""

if "%target%"=="auth" (
    call :add_query users
    exit /b 0
)

if "%target%"=="store" (
    call :add_query products
    call :add_query categories
    call :add_query product_categories
    call :add_query orders
    call :add_query order_items
    exit /b 0
)

if not "%target%"=="" (
    echo %invalid_target%
)

echo %usage%
exit /b 1

:add_query
set "queries=%queries% -c "select * from %1;""
exit /b 0

:dump
docker exec -it iep-project-%target%-db-1 psql -U user -d %target% %queries%
exit /b 0

:help
echo Usage: .\cmd_db.bat [command]
echo Commands:
echo   init [auth^|owner^|customer]                               Initialize migrations and apply the initial migration
echo   migrate [auth^|owner^|customer] -m "Migration message"     Create and apply a new migration
echo   upgrade [auth^|owner^|customer]                            Apply the latest migrations
echo   dump [auth^|store]                                        Dump the current migration version and database contents
exit /b 1
