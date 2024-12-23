# Импортируем необходимые библиотеки и модули
import aiogram # Основная библиотека для создания Telegram-ботов
from aiogram import Dispatcher, Bot, executor  # Импортируем классы для управления ботом
from aiogram.contrib.fsm_storage.memory import MemoryStorage # Для хранения состояний пользователей
# Подключаем конфигурационный файл с токеном API
from config import TOKEN_API 
# Создаем объект бота, передавая ему токен API
bot = Bot(TOKEN_API)
# Создаем диспетчер для обработки обновлений от Telegram
dp = Dispatcher(bot,storage=MemoryStorage())

if __name__ == '__main__':
    from handlers import dp
    print('Бот запущен!')
    executor.start_polling(dp)  # Запускаем бесконечный цикл опроса обновлений от Telegram
