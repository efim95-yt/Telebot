import asyncio
import requests
import feedparser
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "В8637839446:AAFhJJcqqWNVgwaFRk7zpSNw_ayCzIVsEXc"

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_news():
    url = "https://www.pravda.com.ua/rss/view_news/"
    feed = feedparser.parse(url)

    news_list = "🗞️ Последние новости:\n\n"

    if not feed.entries:
        return "⚠️ Не удалось загрузить новости"

    for i, entry in enumerate(feed.entries[:5]):
        news_list += f"{i+1}️⃣ {entry.title}\n"

    return news_list


def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.4647,
        "longitude": 35.0462,
        "current_weather": True
    }

    data = requests.get(url, params=params).json()

    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    return f"🌤️ Днепр:\nТемпература: {temp}°C\nВетер: {wind} км/ч"


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Дніпро Пост\n\n"
        "/news - новости\n"
        "/weather - погода"
    )


@dp.message(Command("news"))
async def news(message: types.Message):
    await message.answer(get_news())


@dp.message(Command("weather"))
async def weather(message: types.Message):
    await message.answer(get_weather())


async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
