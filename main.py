import aiogram
from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot,storage=MemoryStorage())

if __name__ == '__main__':
    from handlers import dp
    print('Бот запущен!')
    executor.start_polling(dp)
