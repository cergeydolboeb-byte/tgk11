import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import json

TELEGRAM_TOKEN = ""
OPENROUTER_KEY = ""

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def ask_ai(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen/qwen3.6-plus",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        ) as response:
            data = await response.json()
            return data["choices"][0]["message"]["content"]

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("👋 Привет! Я AI-бот. Отправь мне сообщение!")

@dp.message()
async def handle(msg: types.Message):
    await bot.send_chat_action(msg.chat.id, "typing")
    try:
        answer = await ask_ai(msg.text)
        await msg.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await msg.answer("⚠️ Ошибка ИИ. Попробуйте позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
