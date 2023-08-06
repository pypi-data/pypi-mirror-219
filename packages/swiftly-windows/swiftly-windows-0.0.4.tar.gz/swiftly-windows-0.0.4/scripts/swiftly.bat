@echo off
REM Disable echo

REM Check if the first argument is 'init' or 'makeapp'
IF NOT "%~1"=="init" IF NOT "%~1"=="makeapp" (
    echo Invalid command.
    exit /b
)

IF "%~1"=="init" (
    REM Call the init function with the second argument as a parameter
    call:init "%~2"
    GOTO:EOF
)

IF "%~1"=="makeapp" (
    REM Call the makeapp function with the second argument as a parameter
    call:makeapp "%~2"
    GOTO:EOF
)

:init
    REM Call pip install
    call pip install swiftly-windows --upgrade > NUL
    echo installation done

    REM Check if parameter is empty
    IF "%~1"=="" (
        REM The commands in this block will execute if the parameter is empty

        call git fetch > NUL 2>&1

        for /f "delims=" %%a in ('git status -uno') do set "git_status=%%a"

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import pull_changes; print(pull_changes('%git_status%'))"') do set "pull_changes=%%a"

        IF "%pull_changes%"=="True" (
            call git pull > NUL
            echo git changes pulled
        ) ELSE (
            echo git up to date
        )

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import get_project_name; print(get_project_name())"') do set "PROJECT_NAME=%%a"
        echo  Project '%PROJECT_NAME%' ready

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import get_venv_location; print(get_venv_location())"') do set "venv_location=%%a"
        call %venv_location%\Scripts\activate
        set "PROJECT_VENV_LOCATION=%venv_location%"

        call pip install swiftly-windows --upgrade > NUL 2>&1
        echo  Virtual environment activated

        for /f "delims=" %%a in ('pip freeze') do set "available_packages=%%a"
        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import check_new_packages; print(check_new_packages('%available_packages%'))"') do set "new_packages=%%a"

        IF "%new_packages%"=="True" (
            call pip install -r requirements.txt > NUL
            echo  New packages installed
        ) ELSE (
            echo  All packages already installed
        )

        call pip install --upgrade pip > NUL 2>&1

        call pip install swiftly-windows --upgrade > NUL 2>&1
        echo  All checks completed swiftly
    ) ELSE (
        REM The commands in this block will execute if the parameter is not empty

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import is_repo; print(is_repo('%~1'))"') do set "is_github_repo=%%a"

        IF "%is_github_repo%"=="True" (
            for /f "delims=" %%a in ('git clone %~1 2^>^&1') do set "git_clone=%%a"
            for /f "delims=" %%a in ('python -c "from swiftly_windows.init import clone_successful; print(clone_successful('%git_clone%'))"') do set "clone_successful=%%a"

            IF "%clone_successful%"=="True" (
                echo  Git repository cloned
            ) ELSE (
                echo  %clone_successful% fail
                echo Do you want to create a new project? (y/n)
                set /p user_input="> "
                set user_input=%user_input:~0,1%
                IF /I NOT "%user_input%"=="y" (
                    exit /b 1
                )
            )
        )

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import initialise; print(initialise('%~1'))"') do set "venv_location=%%a"
        call %venv_location%\Scripts\activate
        set "PROJECT_VENV_LOCATION=%venv_location%"

        cd /D %venv_location%
        cd ..

        call pip install swiftly-windows --upgrade > NUL 2>&1

        for /f "delims=" %%a in ('python -c "from swiftly_windows.init import get_project_name; print(get_project_name())"') do set "PROJECT_NAME=%%a"
        echo  Project '%PROJECT_NAME%' ready

        call pip install --upgrade pip > NUL 2>&1

        call pip install -r requirements.txt > NUL
        echo Requirements installed

        call pip install swiftly-windows --upgrade > NUL 2>&1
        echo  All checks completed swiftly
    )

    echo ✨ Project '%PROJECT_NAME%' initiated successfully :)

:makeapp
    REM Call Python function with arguments
    python -c "from swiftly_windows.makeapp import makeapp; makeapp('%~1', '%PROJECT_VENV_LOCATION%')" > NUL
    TIMEOUT /T 1 /NOBREAK > NUL
    echo ✓ App '%~1' created successfully