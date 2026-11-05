import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Salom! Kino kodini yuboring (masalan: 2).")

@dp.message()
async def get_movie(message: types.Message):
    if not message.text or not message.text.isdigit():
        await message.answer("Iltimos, faqat kino kodini (raqam) yuboring.")
        return
    try:
        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=int(message.text),
            protect_content=True,
        )
    except Exception:
        await message.answer("Bunday kino topilmadi.")

async def health(request):
    return web.Response(text="OK")

async def run_web():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8000))).start()

async def main():
    await run_web()
    print("Bot ishga tushdi", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
