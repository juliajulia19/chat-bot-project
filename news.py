from aiogram import Bot, Dispatcher, executor, types






bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)