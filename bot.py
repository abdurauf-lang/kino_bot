import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
SUB_CHANNEL = "@kinolarr_makoni"
SUB_LINK = "https://t.me/kinolarr_makoni"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(SUB_CHANNEL, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kanalga obuna bo'lish", url=SUB_LINK)],
        [InlineKeyboardButton(text="Tekshirish", callback_data="check")],
    ])

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Salom! Kino kodini yuboring (masalan: 2).")

@dp.callback_query(F.data == "check")
async def check(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.answer()
        await call.message.answer("Rahmat! Endi kino kodini yuboring.")
    else:
        await call.answer("Siz hali obuna bo'lmagansiz!", show_alert=True)

@dp.message()
async def get_movie(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await message.answer(
            "Botdan foydalanish uchun kanalga obuna bo'ling:",
            reply_markup=sub_keyboard(),
        )
        return
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
