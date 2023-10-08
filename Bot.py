from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from main import register_handlers_parse, register_handlers_all_parse
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='5227226669:AAHOiopS89P1877pNXyNA1OFPQzz-qH4rUM')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def main():
    async def on_startup(_):
        print('Bot went online')

    register_handlers_parse(dp)
    register_handlers_all_parse(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == '__main__':
    main()
