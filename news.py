import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from rss_parser import RSSParser
from requests import get


logging.basicConfig(level=logging.DEBUG)


API_TOKEN = "5670646776:AAHnadzwDCqT_cRgSIGYADAdXjYhLY0OxQs"
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
@dp.message_handler(commands="start")
async def start(message: types.Message):
    habr_title = []
    while True:
        if len(habr_title) >= 20:
            habr_title = []
        rss_url = "https://lenta.ru/rss/news"
        xml = get(rss_url)

        parser = RSSParser(xml=xml.content, limit=3)
        feed = parser.parse()

        # пробегаемся по каждой новости в цикле
        for item in reversed(feed.feed):
            # проверяем есть ли заголовок новости в списке
            if not item.title in habr_title:
                habr_title.append(item.title)
                # отправляем сообщение
                await message.answer(f'{hbold(item.publish_date)}\n\n{hlink(item.title, item.link)}\n\n')

        time.sleep(100)











if __name__ == "__news__":
    # запускаем бота
    executor.start_polling(dp)