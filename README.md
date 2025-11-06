# Telegram Bot для удаления фона с изображений

Бот для Telegram, который удаляет фон с изображений с помощью библиотеки rembg.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd bgremover
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` и добавьте токен бота:
```bash
cp env.example .env
# Отредактируйте .env и добавьте ваш BOT_TOKEN
```

Или установите переменную окружения:
```bash
# Windows (PowerShell)
$env:BOT_TOKEN="your_bot_token_here"

# Linux/Mac
export BOT_TOKEN="your_bot_token_here"
```

## Запуск

Запустите бота:
```bash
python bot.py
```

Или используйте батник (Windows):
```bash
start_bot.bat
```

## Использование

1. Найдите бота в Telegram
2. Отправьте команду `/start` для начала работы
3. Отправьте изображение (фото или документ)
4. Бот обработает изображение и вернет результат с удаленным фоном

## Поддерживаемые форматы

- PNG
- JPG/JPEG
- WEBP

## Технологии

- `python-telegram-bot` - библиотека для работы с Telegram Bot API
- `rembg` - библиотека для удаления фона с изображений

