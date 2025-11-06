@echo off
cd /d "%~dp0"
echo ========================================
echo Запуск Telegram бота для удаления фона
echo ========================================
echo.

if exist ".venv\Scripts\python.exe" (
    echo Проверка зависимостей в виртуальном окружении...
    .venv\Scripts\python.exe -m pip install -q -r requirements.txt 2>nul
    echo.
    echo Запуск бота...
    echo.
    .venv\Scripts\python.exe bot.py
) else (
    echo Проверка зависимостей...
    python -m pip install -q -r requirements.txt 2>nul
    echo.
    echo Запуск бота...
    echo.
    python bot.py
)

pause

