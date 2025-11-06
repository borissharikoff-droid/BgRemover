@echo off
echo ========================================
echo Подготовка к push на GitHub
echo ========================================
cd /d "%~dp0"

echo.
echo Добавление всех файлов в git...
git add .

echo.
echo Создание коммита...
git commit -m "Add Telegram bot for background removal with all dependencies and scripts"

echo.
echo Добавление remote репозитория...
git remote remove origin 2>nul
git remote add origin https://github.com/borissharikoff-droid/BgRemover.git

echo.
echo Переименование ветки в main...
git branch -M main

echo.
echo Отправка на GitHub...
git push -u origin main

echo.
echo ========================================
echo Готово! Код отправлен на GitHub
echo ========================================
pause

