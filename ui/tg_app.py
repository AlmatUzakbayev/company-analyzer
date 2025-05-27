import asyncio
import json
import logging
import sys

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from analyzer.config import TELEGRAM_BOT_TOKEN
from analyzer.constants import ANALYZER_URL, START_MESSAGE

dp = Dispatcher()

bot = Bot(
    token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def send_message_chunks(chat_id: int, text: str, chunk_size: int = 4096) -> None:
    """Splits text into parts and sends them as separate messages.
    Args:
        chat_id (int): The ID of the chat to send the messages to.
        text (str): The text to be split and sent.
        chunk_size (int): The maximum size of each message chunk. Default is 4096 characters for Telegram.
    Returns:
        None
    """
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        await bot.send_message(chat_id, chunk)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Handle the /start command."""
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, START_MESSAGE)


@dp.message()
async def message_handler(message: Message) -> None:
    try:
        await bot.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(2)
        async with aiohttp.ClientSession() as session:
            data = {"query": message.text}
            async with session.post(ANALYZER_URL, json=data) as resp:
                if resp.status == 200:
                    response_data = await resp.json()
                    response_text = json.dumps(
                        response_data, indent=4, ensure_ascii=False
                    )
                    await send_message_chunks(message.chat.id, response_text)
                else:
                    await message.answer(f"Error: {resp.status}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")


async def main() -> None:
    await dp.start_polling(bot)


def main_wrapper():
    """Entry point for the application script"""
    asyncio.run(main())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main_wrapper()
