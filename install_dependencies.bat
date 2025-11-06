@echo off
echo ========================================
echo Установка зависимостей для бота
echo ========================================
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo Использование виртуального окружения...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    echo ========================================
    echo Все зависимости установлены!
    echo ========================================
) else (
    echo Виртуальное окружение не найдено!
    echo Установка в системный Python...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
    echo ========================================
    echo Все зависимости установлены!
    echo ========================================
)

pause

