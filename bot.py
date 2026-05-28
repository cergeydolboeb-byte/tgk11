# -*- coding: utf-8 -*-
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

TELEGRAM_BOT_TOKEN = "8317002212:AAF4ob2iP1VRMb9QXLHlN0Gv7pagAaFuaWM"
OPENROUTER_API_KEY = "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"

logging.basicConfig(level=logging.INFO)

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=60.0,
    max_retries=3
)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я AI-бот. Отправь мне сообщение!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = await client.chat.completions.create(
            model="qwen/qwen3.6-plus",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=500,
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "https://localhost",  # OpenRouter требует
                "X-Title": "Telegram Bot"
            }
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("⚠️ Ошибка. Попробуйте позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())