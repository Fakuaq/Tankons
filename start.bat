@echo off

cd "C:\Users\pauli\PycharmProjects\final>"
call ".\venv\Scripts\activate"
start cmd /k "python main.py server"

cd "C:\Users\pauli\PycharmProjects\final>2"
call ".\venv\Scripts\activate"
start cmd /k "python main.py client"

cd "C:\Users\pauli\PycharmProjects\final>"
call ".\venv\Scripts\activate"
start cmd /k "python main.py client"

:loop
set /p input=""
if "%input%"=="" (
    taskkill /IM cmd.exe /T /F
    exit /B
) else (
    goto loop
)