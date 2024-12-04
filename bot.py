import aiohttp
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

user_memory = {}

API_TOKEN = "7297929939:AAFMlWHcVnlgrQqu-ZIvesd8-Eeltt9Ebh8"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I am Lalisa💖. I'm so happy to chat with you blink😄")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_msg = message.text

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": "user", "content": user_msg})

    headers = {
        'authority': 'www.blackbox.ai',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.blackbox.ai',
        'referer': 'https://www.blackbox.ai/agent/LalisaManobalW1kd1N7',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    messages = user_memory[user_id][-5:]

    json_data = {
        'messages': messages,
        'id': 'GHnWQEpvyfOJiEVpgLQbb',
        'previewToken': None,
        'userId': None,
        'codeModelMode': True,
        'agentMode': {
            'mode': True,
            'id': 'LalisaManobalW1kd1N7',
            'name': 'Lalisa Manobal',
        },
        'trendingAgentMode': {},
        'isMicMode': False,
        'maxTokens': 1024,
        'playgroundTopP': None,
        'playgroundTemperature': None,
        'isChromeExt': False,
        'githubToken': '',
        'clickedAnswer2': False,
        'clickedAnswer3': False,
        'clickedForceWebSearch': False,
        'visitFromDelta': False,
        'mobileClient': False,
        'userSelectedModel': None,
        'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
        'imageGenerationMode': False,
        'webSearchModePrompt': False,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://www.blackbox.ai/api/chat', headers=headers, json=json_data) as response:
                bot_reply = await response.text()

                user_memory[user_id].append({"role": "assistant", "content": bot_reply})

                await message.reply(bot_reply, parse_mode=ParseMode.MARKDOWN)

        except aiohttp.ClientError as e:
            await message.reply("Sorry Guys, {Error}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
