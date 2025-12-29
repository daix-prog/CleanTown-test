import os
import nest_asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Применяем nest_asyncio для решения проблемы с циклом событий
nest_asyncio.apply()

# Токен вашего бота
TOKEN = '7772322757:AAGqaruN444_wQQ_LBmg0vzizpK2Z1v1os0'

# Путь к сетевой папке
NETWORK_FOLDER_PATH = r'\\DESKTOP-GMA3GVM\test'

async def save_photo(update: Update, context: CallbackContext) -> None:
    """Обрабатывает полученные фотографии и сохраняет их в сетевую папку."""
    # Получаем информацию о фотографии
    photo_file = await update.message.photo[-1].get_file()
    
    # Создаем уникальное имя файла
    file_extension = photo_file.file_path.split('.')[-1]
    file_name = f"{update.message.from_user.id}_{update.message.date.strftime('%Y%m%d_%H%M%S')}.{file_extension}"
    
    # Полный путь для сохранения
    file_path = os.path.join(NETWORK_FOLDER_PATH, file_name)
    
    # Скачиваем файл и сохраняем его в сетевую папку
    await photo_file.download_to_drive(file_path)
    
    await update.message.reply_text(f"Фото сохранено как {file_name}")

async def main() -> None:
    """Запускает бота."""
    # Инициализируем бота
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчик для фото сообщений
    application.add_handler(MessageHandler(filters.PHOTO, save_photo))
    
    # Запускаем бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())