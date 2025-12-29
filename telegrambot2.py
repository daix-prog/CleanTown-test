import os
import threading
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Токен вашего бота
TOKEN = '7637030225:AAETim8J5UZHzlRzPOgqb59V95J9yBOKK_g'

# Путь к сетевой папке
NETWORK_FOLDER_PATH = r'\\DESKTOP-GMA3GVM\test2'

# Функция для сохранения фото (асинхронная)
async def save_photo_async(update: Update, context: CallbackContext):
    try:
        # Получаем информацию о фотографии
        photo_file = await update.message.photo[-1].get_file()
        
        # Создаем уникальное имя файла
        file_extension = photo_file.file_path.split('.')[-1]
        file_name = f"{update.message.from_user.id}_{update.message.date.strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        
        # Полный путь для сохранения
        file_path = os.path.join(NETWORK_FOLDER_PATH, file_name)
        
        # Скачиваем файл и сохраняем его в сетевую папку
        await photo_file.download_to_drive(file_path)
        
        # Отправляем ответ пользователю
        await update.message.reply_text(f"Фото сохранено как {file_name}")
    except Exception as e:
        print(f"Ошибка при сохранении фото: {e}")
        await update.message.reply_text("Произошла ошибка при сохранении фото.")

# Обертка для вызова асинхронной функции из синхронного кода
def save_photo_wrapper(update: Update, context: CallbackContext):
    # Запускаем асинхронную функцию в отдельном потоке
    threading.Thread(target=lambda: asyncio.run(save_photo_async(update, context))).start()

# Основная функция для запуска бота
def main():
    # Инициализируем бота
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчик для фото сообщений
    application.add_handler(MessageHandler(filters.PHOTO, save_photo_wrapper))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    import asyncio
    main()