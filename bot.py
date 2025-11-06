import logging
import os
import tempfile

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from rembg import remove, new_session
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (берется из переменной окружения или .env файла)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8556536014:AAGfYWy7iv7vUJvEXwi90C34Yjh7SfPO4o4")

# Создаем сессию rembg для оптимизации производительности
# Инициализация сессии будет выполнена при первом использовании
rembg_session = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    try:
        await update.message.reply_text(
            "Привет! 👋\n\n"
            "Я бот для удаления фона с изображений.\n"
            "Просто отправь мне фото или изображение в виде документа, "
            "и я удалю с него фон и верну результат.\n\n"
            "Поддерживаемые форматы: PNG, JPG, JPEG, WEBP"
        )
        logger.info("Ответ на /start отправлен")
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа на /start: {e}", exc_info=True)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик фотографий"""
    global rembg_session
    try:
        # Инициализируем сессию при первом использовании
        if rembg_session is None:
            logger.info("Инициализация rembg сессии...")
            rembg_session = new_session()
            logger.info("rembg сессия инициализирована")
        
        # Отправляем сообщение о начале обработки
        processing_msg = await update.message.reply_text("🔄 Обрабатываю изображение...")
        
        # Получаем фото (берем самое большое качество)
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as input_file:
            input_path = input_file.name
            await file.download_to_drive(input_path)
        
        # Обрабатываем изображение
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data, session=rembg_session)
        
        # Сохраняем результат
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as output_file:
            output_path = output_file.name
            output_file.write(output_data)
        
        # Отправляем результат
        with open(output_path, 'rb') as result_file:
            await update.message.reply_document(
                document=result_file,
                filename='no_background.png',
                caption="✅ Фон успешно удален!"
            )
        
        # Удаляем временные файлы
        os.unlink(input_path)
        os.unlink(output_path)
        
        # Удаляем сообщение о обработке
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Произошла ошибка при обработке изображения: {str(e)}"
        )
        if 'processing_msg' in locals():
            await processing_msg.delete()


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик документов (изображений)"""
    global rembg_session
    try:
        # Инициализируем сессию при первом использовании
        if rembg_session is None:
            logger.info("Инициализация rembg сессии...")
            rembg_session = new_session()
            logger.info("rembg сессия инициализирована")
        
        document = update.message.document
        
        # Проверяем, что это изображение
        if not document.mime_type or not document.mime_type.startswith('image/'):
            await update.message.reply_text(
                "❌ Пожалуйста, отправьте изображение (PNG, JPG, JPEG, WEBP)"
            )
            return
        
        # Отправляем сообщение о начале обработки
        processing_msg = await update.message.reply_text("🔄 Обрабатываю изображение...")
        
        # Получаем файл
        file = await context.bot.get_file(document.file_id)
        
        # Определяем расширение из mime_type или имени файла
        ext = '.png'
        if document.mime_type:
            mime_to_ext = {
                'image/jpeg': '.jpg',
                'image/jpg': '.jpg',
                'image/png': '.png',
                'image/webp': '.webp'
            }
            ext = mime_to_ext.get(document.mime_type, '.png')
        
        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as input_file:
            input_path = input_file.name
            await file.download_to_drive(input_path)
        
        # Обрабатываем изображение
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data, session=rembg_session)
        
        # Сохраняем результат
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as output_file:
            output_path = output_file.name
            output_file.write(output_data)
        
        # Отправляем результат
        with open(output_path, 'rb') as result_file:
            await update.message.reply_document(
                document=result_file,
                filename='no_background.png',
                caption="✅ Фон успешно удален!"
            )
        
        # Удаляем временные файлы
        os.unlink(input_path)
        os.unlink(output_path)
        
        # Удаляем сообщение о обработке
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"Ошибка при обработке документа: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Произошла ошибка при обработке изображения: {str(e)}"
        )
        if 'processing_msg' in locals():
            await processing_msg.delete()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    await update.message.reply_text(
        "Пожалуйста, отправьте мне изображение (фото или документ), "
        "и я удалю с него фон."
    )


def main() -> None:
    """Запуск бота"""
    try:
        print("=" * 50)
        print("Запуск бота...")
        print("=" * 50)
        logger.info("Инициализация бота...")
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем обработчики
        print("Регистрация обработчиков...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Запускаем бота
        print("=" * 50)
        print("✅ Бот запущен и готов к работе!")
        print("Ожидание сообщений...")
        print("=" * 50)
        logger.info("Бот запущен и готов к работе!")
        logger.info("Ожидание сообщений...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        logger.error(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()

