@echo off

set mode=%1

if "%mode%"=="" (
    call :help
    exit /b 1
)

if "%mode%"=="help" (
    call .\venv\Scripts\activate
    cd test
    python main.py --help
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%mode%"=="no-blockchain" (
    call :no-blockchain %2
    exit /b %errorlevel%
)

if "%mode%"=="blockchain" (
    call :blockchain %2
    exit /b %errorlevel%
)

echo Invalid mode: %mode%
call :help
exit /b 1

:no-blockchain
set type=%1

if "%type%"=="authentication" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level0" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level0 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level1" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level2" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level3" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="all" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if not "%type%"=="" (
    echo Invalid type: %type%
)

echo Usage: .\cmd_test.bat no-blockchain [type]
echo Types:
echo   authentication           Run tests which grade endpoints of the authentication service
echo   level0                   Run tests which grade endpoints that update and search products
echo   level1                   Run tests which grade endpoints that create orders and retreive order information
echo   level2                   Run tests which grade endpoints regarding order pickup and delivery
echo   level3                   Run tests which grade endpoints provide owners with product and category
echo   all                      Run all tests
exit /b 1

:blockchain
set type=%1

if "%type%"=="level1" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level2" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="level3" (
    call .\venv\Scripts\activate
    cd test
    python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if "%type%"=="all" (
    call .\venv\Scripts\activate
    cd test
    python3 main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles  --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
    set result=%errorlevel%
    cd ..
    call deactivate
    exit /b %result%
)

if not "%type%"=="" (
    echo Invalid type: %type%
)

echo Usage: .\cmd_test.bat blockchain [type]
echo Types:
echo   level1                   Run tests which grade endpoints that create orders and retreive order information
echo   level2                   Run tests which grade endpoints regarding order pickup and delivery
echo   level3                   Run tests which grade endpoints provide owners with product and category
echo   all                      Run all tests
exit /b 1

:help
echo Usage: .\cmd_test.bat [mode]
echo Modes:
echo   help                     Show the help message
echo   no-blockchain [type]     Run grading tests without blockchain integration
echo   blockchain [type]        Run grading tests with blockchain integration
echo Types:
echo   authentication           Run tests which grade endpoints of the authentication service
echo   level0                   Run tests which grade endpoints that update and search products
echo   level1                   Run tests which grade endpoints that create orders and retreive order information
echo   level2                   Run tests which grade endpoints regarding order pickup and delivery
echo   level3                   Run tests which grade endpoints provide owners with product and category
echo   all                      Run all tests
exit /b 1
